import argparse
import csv
import json
import os
import random
import re
import time
from datetime import datetime, timezone
from html import unescape
from html.parser import HTMLParser
from typing import Optional
from urllib import error, parse, request


DEFAULT_ENDPOINT = "https://stepup.openai.azure.com/openai/v1"
DEFAULT_DEPLOYMENT = "gpt-4.1-mini"


class HTMLTextExtractor(HTMLParser):
    def __init__(self) -> None:
        super().__init__()
        self._parts: list[str] = []
        self._skip_tag_stack: list[str] = []

    def handle_starttag(self, tag: str, attrs) -> None:
        if tag in {"script", "style", "noscript"}:
            self._skip_tag_stack.append(tag)

    def handle_endtag(self, tag: str) -> None:
        if self._skip_tag_stack and self._skip_tag_stack[-1] == tag:
            self._skip_tag_stack.pop()

    def handle_data(self, data: str) -> None:
        if not self._skip_tag_stack:
            cleaned = data.strip()
            if cleaned:
                self._parts.append(cleaned)

    def text(self) -> str:
        return " ".join(self._parts)


def jitter_sleep(min_seconds: float, max_seconds: float) -> None:
    time.sleep(random.uniform(min_seconds, max_seconds))


def log_message(log_file: str, message: str) -> None:
    ts = datetime.now(timezone.utc).isoformat()
    line = f"{ts} {message}"
    print(line)
    log_dir = os.path.dirname(log_file)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def fetch_website_text(url: str, timeout_seconds: int, max_chars: int) -> str:
    req = request.Request(
        url,
        headers={
            "User-Agent": (
                "Mozilla/5.0 (X11; Linux x86_64) "
                "AppleWebKit/537.36 (KHTML, like Gecko) "
                "Chrome/125.0.0.0 Safari/537.36"
            )
        },
    )
    with request.urlopen(req, timeout=timeout_seconds) as resp:
        raw = resp.read()

    html = raw.decode("utf-8", errors="replace")
    parser = HTMLTextExtractor()
    parser.feed(html)
    text = unescape(parser.text())
    text = re.sub(r"\s+", " ", text).strip()
    return text[:max_chars]


def build_prompt(site_url: str, site_text: str) -> str:
    return (
        "You extract contact details from webpage text.\n"
        "Call the provided function with extracted values.\n"
        "Rules:\n"
        "- Classify the site as personal trainer/PT studio or not.\n"
        "- Use classification='not_personal_trainer_or_pt_studio' when the site is not a personal trainer or PT studio website.\n"
        "- If classification='not_personal_trainer_or_pt_studio', emails and phones must both be empty lists.\n"
        "- Return all plausible business emails and phones.\n"
        "- If no email exists, return an empty emails list.\n"
        "- If no phone exists, return an empty phones list.\n"
        "- Prefer business contact details over unrelated ones.\n"
        "- Return normalized values when possible.\n\n"
        f"Website URL: {site_url}\n"
        f"Website visible text:\n{site_text}"
    )


def dedupe_keep_order(values: list[str]) -> list[str]:
    seen: set[str] = set()
    out: list[str] = []
    for value in values:
        key = value.lower()
        if key in seen:
            continue
        seen.add(key)
        out.append(value)
    return out


def normalize_str_list(value) -> list[str]:
    if value is None:
        return []
    if isinstance(value, str):
        parts = [value]
    elif isinstance(value, list):
        parts = [item for item in value if item is not None]
    else:
        parts = [value]

    normalized: list[str] = []
    for item in parts:
        text = str(item).strip()
        if text:
            normalized.append(text)
    return dedupe_keep_order(normalized)


def normalize_contact_object(payload: dict) -> dict:
    if not isinstance(payload, dict):
        raise ValueError("Function arguments are not a JSON object.")

    emails = normalize_str_list(payload.get("emails"))
    phones = normalize_str_list(payload.get("phones"))
    classification = str(payload.get("classification", "")).strip()
    allowed = {
        "personal_trainer_or_pt_studio",
        "not_personal_trainer_or_pt_studio",
    }
    if classification not in allowed:
        classification = "not_personal_trainer_or_pt_studio"
    if classification == "not_personal_trainer_or_pt_studio":
        emails = []
        phones = []

    return {
        "classification": classification,
        "emails": emails,
        "phones": phones,
    }


def extract_contact_from_response(response_json: dict) -> dict:
    # Primary path: function/tool call arguments.
    output = response_json.get("output", [])
    if isinstance(output, list):
        for item in output:
            if not isinstance(item, dict):
                continue
            if item.get("type") == "function_call":
                args_raw = item.get("arguments", "{}")
                if not isinstance(args_raw, str):
                    continue
                parsed = json.loads(args_raw)
                return normalize_contact_object(parsed)

    # Fallback path: parse text as JSON object.
    output_text = response_json.get("output_text")
    if isinstance(output_text, str) and output_text.strip():
        try:
            parsed = json.loads(output_text)
            return normalize_contact_object(parsed)
        except json.JSONDecodeError:
            match = re.search(r"\{.*\}", output_text, flags=re.DOTALL)
            if match:
                parsed = json.loads(match.group(0))
                return normalize_contact_object(parsed)

    raise ValueError("No valid function call or JSON contact payload found.")


def call_openai_responses_api(
    endpoint: str,
    api_key: str,
    deployment_name: str,
    prompt: str,
    timeout_seconds: int,
) -> dict:
    url = endpoint.rstrip("/") + "/responses"
    payload = {
        "model": deployment_name,
        "input": prompt,
        "temperature": 0,
        "tools": [
            {
                "type": "function",
                "name": "save_contact",
                "description": "Return extracted website contact details.",
                "parameters": {
                    "type": "object",
                    "additionalProperties": False,
                    "properties": {
                        "classification": {
                            "type": "string",
                            "enum": [
                                "personal_trainer_or_pt_studio",
                                "not_personal_trainer_or_pt_studio",
                            ],
                        },
                        "emails": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                        "phones": {
                            "type": "array",
                            "items": {"type": "string"},
                        },
                    },
                    "required": ["classification", "emails", "phones"],
                },
            }
        ],
        "tool_choice": {"type": "function", "name": "save_contact"},
    }
    data = json.dumps(payload).encode("utf-8")
    req = request.Request(
        url,
        data=data,
        method="POST",
        headers={
            "Content-Type": "application/json",
            "api-key": api_key,
            "Authorization": f"Bearer {api_key}",
        },
    )
    with request.urlopen(req, timeout=timeout_seconds) as resp:
        body = resp.read().decode("utf-8", errors="replace")
    return json.loads(body)


def extract_contacts_with_retry(
    endpoint: str,
    api_key: str,
    deployment_name: str,
    site_url: str,
    timeout_seconds: int,
    retries: int,
    base_delay_seconds: float,
) -> dict:
    website_text = fetch_website_text(
        url=site_url,
        timeout_seconds=timeout_seconds,
        max_chars=20_000,
    )

    if not website_text:
        return {
            "classification": "not_personal_trainer_or_pt_studio",
            "emails": [],
            "phones": [],
        }

    # Human-like pacing before model call.
    jitter_sleep(base_delay_seconds, base_delay_seconds + 2.0)

    prompt = build_prompt(site_url=site_url, site_text=website_text)
    last_error: Optional[Exception] = None

    for attempt in range(retries + 1):
        try:
            response_json = call_openai_responses_api(
                endpoint=endpoint,
                api_key=api_key,
                deployment_name=deployment_name,
                prompt=prompt,
                timeout_seconds=timeout_seconds,
            )
            return extract_contact_from_response(response_json)
        except (error.HTTPError, error.URLError, TimeoutError, ValueError) as exc:
            last_error = exc
            if attempt >= retries:
                break
            backoff = (2 ** attempt) * base_delay_seconds + random.uniform(0.3, 1.7)
            time.sleep(backoff)

    raise RuntimeError(f"Failed to extract contacts after retries: {last_error}")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Extract emails/phones from websites using Azure OpenAI Responses API."
    )
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument("--url", help="Single website URL to inspect.")
    source_group.add_argument(
        "--input-csv",
        default="",
        help="CSV file containing website URLs.",
    )
    parser.add_argument(
        "--url-column",
        default="website",
        help="Column name used when --input-csv is provided.",
    )
    parser.add_argument(
        "--output-json",
        default="",
        help="Output JSON file path for batch mode. Defaults to <input>_contacts.json.",
    )
    parser.add_argument(
        "--log-file",
        default="",
        help="Log file path. Defaults to <output_json>.log in batch mode.",
    )
    parser.add_argument(
        "--api-key",
        default="",
        help="Azure OpenAI API key. Can also come from AZURE_OPENAI_API_KEY.",
    )
    parser.add_argument(
        "--endpoint",
        default=DEFAULT_ENDPOINT,
        help=f"Azure OpenAI base endpoint (default: {DEFAULT_ENDPOINT})",
    )
    parser.add_argument(
        "--deployment-name",
        default=DEFAULT_DEPLOYMENT,
        help=f"Azure deployment/model name (default: {DEFAULT_DEPLOYMENT})",
    )
    parser.add_argument(
        "--timeout-seconds",
        type=int,
        default=30,
        help="HTTP timeout for webpage/API calls.",
    )
    parser.add_argument(
        "--retries",
        type=int,
        default=3,
        help="Retry count for transient failures.",
    )
    parser.add_argument(
        "--base-delay-seconds",
        type=float,
        default=1.7,
        help="Base delay used for jitter + exponential backoff.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    api_key = args.api_key.strip()
    if not api_key:
        api_key = os.getenv("AZURE_OPENAI_API_KEY", "").strip()

    if not api_key:
        raise ValueError(
            "Missing API key. Pass --api-key or set AZURE_OPENAI_API_KEY."
        )

    retries = max(0, args.retries)
    base_delay = max(0.1, args.base_delay_seconds)

    if args.url:
        result = extract_contacts_with_retry(
            endpoint=args.endpoint,
            api_key=api_key,
            deployment_name=args.deployment_name,
            site_url=args.url,
            timeout_seconds=args.timeout_seconds,
            retries=retries,
            base_delay_seconds=base_delay,
        )
        print(json.dumps(result, ensure_ascii=True))
        return

    input_csv = args.input_csv
    output_json = args.output_json.strip()
    if not output_json:
        stem, ext = os.path.splitext(input_csv)
        _ = ext  # keep variable for readability while deriving output path from input stem
        output_json = f"{stem}_contacts.json"
    log_file = args.log_file.strip() or f"{output_json}.log"


    with open(input_csv, "r", newline="", encoding="utf-8") as csv_in, open(
        output_json, "w", encoding="utf-8"
    ) as json_out:
        reader = csv.DictReader(csv_in)
        if not reader.fieldnames:
            raise ValueError("Input CSV has no headers.")
        if args.url_column not in reader.fieldnames:
            raise ValueError(
                f"Column '{args.url_column}' not found in CSV. "
                f"Headers: {', '.join(reader.fieldnames)}"
            )
        log_message(
            log_file,
            f"[INFO] Start batch input='{input_csv}' output='{output_json}'",
        )
        json_out.write("[\n")
        wrote_any_row = False

        processed_count = 0
        success_count = 0
        for row in reader:
            processed_count += 1
            site_url = (row.get(args.url_column) or "").strip()
            contact = {
                "classification": "not_personal_trainer_or_pt_studio",
                "emails": [],
                "phones": [],
            }
            status = "empty_url"
            if site_url:
                try:
                    contact = extract_contacts_with_retry(
                        endpoint=args.endpoint,
                        api_key=api_key,
                        deployment_name=args.deployment_name,
                        site_url=site_url,
                        timeout_seconds=args.timeout_seconds,
                        retries=retries,
                        base_delay_seconds=base_delay,
                    )
                    status = "ok"
                    success_count += 1
                except Exception as e:
                    log_message(
                        log_file,
                        f"[ERROR] index={processed_count} status={status} url='{site_url}' error='{e}'",
                    )
                    contact = {
                        "classification": "not_personal_trainer_or_pt_studio",
                        "emails": [],
                        "phones": [],
                    }
                    status = "error"
            row["classification"] = contact["classification"]
            row["emails"] = contact["emails"]
            # remove whitespaces from phones
            row["phones"] = [phone.replace(" ", "") for phone in contact["phones"]]

            row.pop("city", None)
            row.pop("email", None)
            row.pop("address", None)
            row.pop("maps_url", None)
            row.pop("scraped_at", None)

            phone_value = (row.get("phone") or "").replace(" ", "").strip()
            if phone_value and phone_value not in row["phones"]:
                row["phones"].append(phone_value)

            row.pop("phone", None)

            if row["classification"] == "not_personal_trainer_or_pt_studio":
                log_message(
                    log_file,
                    f"[SKIP] index={processed_count} status={status} url='{site_url}' "
                    f"classification={row['classification']}",
                )
            else:
                if wrote_any_row:
                    json_out.write(",\n")
                json_out.write(json.dumps(row, ensure_ascii=True, indent=2))
                json_out.flush()
                wrote_any_row = True
                log_message(
                    log_file,
                    f"[ROW] index={processed_count} status={status} url='{site_url}' "
                    f"classification={row['classification']} "
                    f"emails={len(row['emails'])} phones={len(row['phones'])}",
                )
            jitter_sleep(base_delay, base_delay + 1.3)
            
        if wrote_any_row:
            json_out.write("\n")
        json_out.write("]\n")
        json_out.flush()
        log_message(
            log_file,
            f"[DONE] processed={processed_count} success={success_count} "
            f"failed_or_empty={processed_count - success_count}",
        )

    print(output_json)


if __name__ == "__main__":
    main()
