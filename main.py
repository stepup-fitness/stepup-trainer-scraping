import argparse
import csv
import json
import math
import random
import re
import time
from dataclasses import asdict, dataclass
from datetime import datetime, timezone
from typing import List, Optional
import os
from urllib.parse import quote_plus, unquote, urlparse

from playwright.sync_api import TimeoutError as PlaywrightTimeoutError
from playwright.sync_api import sync_playwright


EMAIL_REGEX = re.compile(r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}")

COUNTRY_ALIASES = {
    "california": {"california", "californien", "californienne", "californien"},
    "oregon": {"oregon", "oreganois", "oreganoise", "oregonien"},
    "washington": {"washington", "washingtonais", "washingtonaise", "washingtonien"},
    "montana": {"montana", "montanais", "montanaise", "montanaien"},
    "idaho": {"idaho", "idahois", "idahoise", "idahoien"},
    "nevada": {"nevada", "nevadais", "nevadaise", "nevadaien"},
    "arizona": {"arizona", "arizonais", "arizonaise", "arizonien"},
    "utah": {"utah", "utahis", "utahise", "utahien"},
    "wyoming": {"wyoming", "wyomingis", "wyomingise", "wyomingien"},
    "colorado": {"colorado", "coloradois", "coloradoise", "coloradoien"},
    "new mexico": {"new mexico", "new mexicois", "new mexicoise", "new mexicien"},
    "texas": {"texas", "texasais", "texasaise", "texasien"},
    "oklahoma": {"oklahoma", "oklahomais", "oklahomaise", "oklahomaien"},
    "kansas": {"kansas", "kansasis", "kansasise", "kansasien"},
    "nebraska": {"nebraska", "nebraskais", "nebraskaise", "nebraskaien"},
    "south dakota": {"south dakota", "south dakotais", "south dakotaise", "south dakotaien"},
    "north dakota": {"north dakota", "north dakotais", "north dakotaise", "north dakotaien"},
    "minnesota": {"minnesota", "minnesotais", "minnesotaise", "minnesotaien"},
    "iowa": {"iowa", "iowais", "iowaise", "iowaien"},
    "missouri": {"missouri", "missouriis", "missouriise", "missouriien"},
    "arkansas": {"arkansas", "arkansasis", "arkansasise", "arkansasien"},
    "illinois": {"illinois", "illinoisais", "illinoisaise", "illinoisien"},
    "wisconsin": {"wisconsin", "wisconsinais", "wisconsinaise", "wisconsinien"},
    "michigan": {"michigan", "michiganais", "michiganaise", "michiganien"},
    "indiana": {"indiana", "indianais", "indianaise", "indianien"},
    "ohio": {"ohio", "ohioais", "ohioaise", "ohioien"},
    "kentucky": {"kentucky", "kentuckyis", "kentuckyise", "kentuckyien"},
    "tennessee": {"tennessee", "tennesseeis", "tennesseeise", "tennesseeien"},
    "mississippi": {"mississippi", "mississippiis", "mississippiise", "mississippiien"},
    "louisiana": {"louisiana", "louisianais", "louisianaise", "louisianaien"},
    "alabama": {"alabama", "alabamais", "alabamaise", "alabamaien"},
    "florida": {"florida", "floridais", "floridaise", "floridaien"},
    "georgia": {"georgia", "georgiais", "georgiaise", "georgiaien"},
    "south carolina": {"south carolina", "south carolinais", "south carolinaise", "south carolinaien"},
    "north carolina": {"north carolina", "north carolinais", "north carolinaise", "north carolinaien"},
    "virginia": {"virginia", "virginiais", "virginiaise", "virginiaien"},
    "west virginia": {"west virginia", "west virginiais", "west virginiaise", "west virginiaien"},
    "pennsylvania": {"pennsylvania", "pennsylvaniais", "pennsylvaniaise", "pennsylvaniaien"},
    "new york": {"new york", "new yorkais", "new yorkaise", "new yorkien"},
    "maryland": {"maryland", "marylandais", "marylandaise", "marylandien"},
    "delaware": {"delaware", "delawareis", "delawareise", "delawareien"},
    "new jersey": {"new jersey", "new jerseyais", "new jerseyaise", "new jerseyien"},
    "connecticut": {"connecticut", "connecticutis", "connecticutise", "connecticutien"},
    "rhode island": {"rhode island", "rhode islandis", "rhode islandise", "rhode islandien"},
    "massachusetts": {"massachusetts", "massachusettsis", "massachusettsise", "massachusettsien"},
    "vermont": {"vermont", "vermontis", "vermontise", "vermontien"},
    "new hampshire": {"new hampshire", "new hampshireis", "new hampshireise", "new hampshireien"},
    "maine": {"maine", "mainais", "mainaise", "mainien"},
    "canada": {"canada", "canadien", "canadienne", "canadien"},
    "australia": {"australia", "australien", "australienne", "australien"},
    "new zealand": {"new zealand", "nouvelle-zélande", "nouvel-zélandais", "nouvel-zélandaise"},
    "uk": {"uk", "britain", "british", "british"},
    "scotland": {"scotland", "écosse", "écossais", "écossaise"},
    "wales": {"wales", "pays de galles", "gallois", "galloise"},
    "northern ireland": {"northern ireland", "irlande du nord", "nord irlandais", "nord irlandaise"},
    "germany": {"germany", "allemagne", "allemand", "allemande"},
    "spain": {"spain", "espagne", "espagnol", "espagnole"},
    "italy": {"italy", "italie", "italien", "italienne"},
    "france": {"france", "française", "français", "français"},
    "netherlands": {"netherlands", "néerlandais", "néerlandaise", "néerlandais"},
    "sweden": {"sweden", "suède", "suédois", "suédoise"},
    "norway": {"norway", "norvège", "norvégien", "norvégienne"},
    "denmark": {"denmark", "danemark", "danois", "danoise"},
    "finland": {"finland", "finlande", "finlandais", "finlandaise"},
    "belgium": {"belgium", "belgique", "belgie", "belgien"},
    "switzerland": {"switzerland", "suisse", "suisse", "suisse"},
    "austria": {"austria", "autriche", "autrichien", "autrichienne"}
}


@dataclass
class TrainerLead:
    country: str
    city: str
    keyword: str
    business_name: str
    phone: str
    website: str
    email: str
    address: str
    maps_url: str
    scraped_at: str


@dataclass
class GridCell:
    center_lat: float
    center_lng: float
    size_km: float
    depth: int


def randomized_sleep(min_seconds: float = 0.8, max_seconds: float = 2.8) -> None:
    time.sleep(random.uniform(min_seconds, max_seconds))


def parse_proxy_url(proxy_url: str) -> dict:
    value = clean_text(proxy_url)
    if not value:
        raise ValueError("Empty proxy URL.")
    if "://" not in value:
        value = f"http://{value}"

    parsed = urlparse(value)
    if not parsed.scheme or not parsed.hostname or not parsed.port:
        raise ValueError(
            "Invalid proxy URL. Expected format like http://user:pass@host:port"
        )

    proxy_cfg = {"server": f"{parsed.scheme}://{parsed.hostname}:{parsed.port}"}
    if parsed.username:
        proxy_cfg["username"] = unquote(parsed.username)
    if parsed.password:
        proxy_cfg["password"] = unquote(parsed.password)
    return proxy_cfg


def load_proxy_pool_from_env() -> List[dict]:
    """
    Supports:
      - PROXY_URL=http://user:pass@host:port
      - PROXY_LIST=http://u:p@h1:1111;http://u:p@h2:2222
    """
    proxy_list_raw = clean_text(os.getenv("PROXY_LIST", ""))
    proxy_url_raw = clean_text(os.getenv("PROXY_URL", ""))
    if not proxy_list_raw and not proxy_url_raw:
        return []

    raw_values = (
        re.split(r"[,\n;]+", proxy_list_raw)
        if proxy_list_raw
        else [proxy_url_raw]
    )
    proxies: List[dict] = []
    for raw in raw_values:
        if not clean_text(raw):
            continue
        proxies.append(parse_proxy_url(raw))
    return proxies


def summarize_proxy(proxy_cfg: dict) -> str:
    return proxy_cfg.get("server", "unknown-proxy")


def choose_proxy_rotation_mode(args: argparse.Namespace, proxy_pool_size: int) -> str:
    """
    Modes:
      - run: one proxy for whole run
      - query: rotate before each query
      - bbox: rotate before each bbox
      - auto: bbox in grid mode, query otherwise
    """
    configured = clean_text(os.getenv("PROXY_ROTATION_MODE", "auto")).lower()
    if proxy_pool_size == 0:
        return "none"
    if configured not in {"auto", "run", "query", "bbox"}:
        raise ValueError("PROXY_ROTATION_MODE must be one of: auto, run, query, bbox")
    if configured == "auto":
        return "bbox" if args.grid_mode else "query"
    if configured == "bbox" and not args.grid_mode:
        return "query"
    return configured


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Scrape personal trainer contact data from Google Maps."
    )
    parser.add_argument(
        "--countries",
        required=True,
        help='Comma-separated countries, e.g. "France,Germany,Spain"',
    )
    parser.add_argument(
        "--cities",
        default="",
        help='Comma-separated city list used for every country (optional). Example: "Paris,Lyon"',
    )
    parser.add_argument(
        "--keywords",
        default="personal trainer,fitness coach",
        help='Comma-separated search keywords. Example: "personal trainer,fitness coach,coach sportif"',
    )
    parser.add_argument(
        "--max-results-per-query",
        type=int,
        default=120,
        help="Max listings to process per country+city+keyword search.",
    )
    parser.add_argument(
        "--headless",
        action=argparse.BooleanOptionalAction,
        default=os.environ.get("DISPLAY") is None,
        help=(
            "Run browser in headless mode (default: headless when DISPLAY is unset, e.g. SSH servers). "
            "Use --no-headless for a visible browser on your desktop."
        ),
    )
    parser.add_argument(
        "--output",
        default="trainer_leads.csv",
        help=(
            "Output CSV path. In grid mode with multiple --bboxes, each bbox is written to "
            "<dir>/<stem>_bbox_<n><ext> (e.g. Belgium/leads.csv -> Belgium/leads_bbox_1.csv). "
            "A single --bbox still uses this path as-is."
        ),
    )
    parser.add_argument(
        "--skip-email-crawl",
        action="store_true",
        help="Skip visiting websites to search for emails.",
    )
    parser.add_argument(
        "--grid-mode",
        action="store_true",
        help="Enable adaptive grid scraping mode (bbox required).",
    )
    parser.add_argument(
        "--bbox",
        default="",
        help="Bounding box for grid mode: min_lat,min_lng,max_lat,max_lng",
    )
    parser.add_argument(
        "--bboxes",
        default="",
        help=(
            "Multiple bounding boxes for grid mode, separated by ';'. "
            "Example: 'min_lat,min_lng,max_lat,max_lng;min_lat,min_lng,max_lat,max_lng'"
        ),
    )
    parser.add_argument(
        "--initial-cell-km",
        type=float,
        default=10.0,
        help="Initial cell size in km for grid mode.",
    )
    parser.add_argument(
        "--min-cell-km",
        type=float,
        default=2.0,
        help="Smallest allowed cell size in km.",
    )
    parser.add_argument(
        "--max-grid-depth",
        type=int,
        default=4,
        help="Max subdivision depth in grid mode.",
    )
    parser.add_argument(
        "--dead-zone-max",
        type=int,
        default=20,
        help="0..dead-zone-max results means sparse/dead cell.",
    )
    parser.add_argument(
        "--ok-zone-max",
        type=int,
        default=60,
        help="dead-zone-max+1..ok-zone-max means good coverage cell.",
    )
    parser.add_argument(
        "--maps-cap",
        type=int,
        default=120,
        help="Approximate Maps UI hard cap used to force subdivision.",
    )
    parser.add_argument(
        "--min-new-uniques-per-child",
        type=int,
        default=5,
        help="If child cell yields fewer new unique leads, stop deeper splits.",
    )
    parser.add_argument(
        "--delay-between-bboxes-min",
        type=float,
        default=0.0,
        help="Delay in minutes between consecutive bboxes (grid mode).",
    )
    parser.add_argument(
        "--resume",
        action="store_true",
        help="Resume from checkpoint and append to existing output CSV.",
    )
    parser.add_argument(
        "--checkpoint-file",
        default="",
        help="Checkpoint file path (JSONL). Defaults to <output>.checkpoint.jsonl",
    )
    parser.add_argument(
        "--log-file",
        default="",
        help="Log file path. Defaults to <output>.log",
    )
    return parser.parse_args()


def clean_text(value: Optional[str]) -> str:
    return (value or "").strip()


def get_country_city_pairs(countries: List[str], cities: List[str]) -> List[tuple[str, str]]:
    if not cities:
        return [(country, "") for country in countries]

    pairs: List[tuple[str, str]] = []
    for country in countries:
        for city in cities:
            pairs.append((country, city))
    return pairs


def parse_bbox(value: str) -> tuple[float, float, float, float]:
    parts = [p.strip() for p in value.split(",") if p.strip()]
    if len(parts) != 4:
        raise ValueError("bbox must be: min_lat,min_lng,max_lat,max_lng")
    min_lat, min_lng, max_lat, max_lng = (float(parts[0]), float(parts[1]), float(parts[2]), float(parts[3]))
    if min_lat >= max_lat or min_lng >= max_lng:
        raise ValueError("bbox coordinates are invalid.")
    return min_lat, min_lng, max_lat, max_lng


def parse_bboxes(values: str) -> List[tuple[float, float, float, float]]:
    chunks = [chunk.strip() for chunk in values.split(";") if chunk.strip()]
    if not chunks:
        return []
    return [parse_bbox(chunk) for chunk in chunks]


def output_path_for_grid_bbox(base_output: str, bbox_index: int) -> str:
    """Belgium/leads.csv + 1 -> results/Belgium/leads_bbox_1.csv"""
    directory, filename = os.path.split(base_output)
    stem, ext = os.path.splitext(filename)
    new_filename = f"{stem}_bbox_{bbox_index}{ext}"
    return os.path.join("results", directory, new_filename) if directory else new_filename


def grid_bbox_output_paths(base_output: str, num_bboxes: int) -> List[str]:
    if num_bboxes <= 1:
        return [base_output]
    return [output_path_for_grid_bbox(base_output, i) for i in range(1, num_bboxes + 1)]


def format_bbox(bbox: tuple[float, float, float, float]) -> str:
    return ",".join(f"{x:.6f}" for x in bbox)


def checkpoint_key(country: str, keyword: str, bbox: tuple[float, float, float, float]) -> str:
    return f"{country}|{keyword}|{format_bbox(bbox)}"


def default_checkpoint_file(output_path: str) -> str:
    return f"{output_path}.checkpoint.jsonl"


def default_log_file(output_path: str) -> str:
    return f"{output_path}.log"


def log_message(log_file: str, message: str) -> None:
    ts = datetime.now(timezone.utc).isoformat()
    line = f"{ts} {message}"
    print(line)
    log_dir = os.path.dirname(log_file)
    if log_dir:
        os.makedirs(log_dir, exist_ok=True)
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(line + "\n")


def append_checkpoint_event(checkpoint_file: str, event: dict) -> None:
    checkpoint_dir = os.path.dirname(checkpoint_file)
    if checkpoint_dir:
        os.makedirs(checkpoint_dir, exist_ok=True)
    payload = {"ts": datetime.now(timezone.utc).isoformat(), **event}
    with open(checkpoint_file, "a", encoding="utf-8") as f:
        f.write(json.dumps(payload, ensure_ascii=True) + "\n")


def load_checkpoint_state(checkpoint_file: str) -> tuple[set[str], set[str]]:
    done_cells: set[str] = set()
    done_bboxes: set[str] = set()
    if not os.path.exists(checkpoint_file):
        return done_cells, done_bboxes

    with open(checkpoint_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                event = json.loads(line)
            except json.JSONDecodeError:
                continue
            event_type = event.get("type", "")
            if event_type == "cell_done":
                run_key = clean_text(str(event.get("run_key", "")))
                visit_key = clean_text(str(event.get("visit_key", "")))
                if run_key and visit_key:
                    done_cells.add(f"{run_key}|{visit_key}")
            elif event_type == "bbox_done":
                run_key = clean_text(str(event.get("run_key", "")))
                if run_key:
                    done_bboxes.add(run_key)
    return done_cells, done_bboxes


def load_seen_keys_from_csv(output_path: str) -> set[str]:
    seen: set[str] = set()
    if not os.path.exists(output_path):
        return seen
    with open(output_path, "r", newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            lead = TrainerLead(
                country=clean_text(row.get("country")),
                city=clean_text(row.get("city")),
                keyword=clean_text(row.get("keyword")),
                business_name=clean_text(row.get("business_name")),
                phone=clean_text(row.get("phone")),
                website=clean_text(row.get("website")),
                email=clean_text(row.get("email")),
                address=clean_text(row.get("address")),
                maps_url=clean_text(row.get("maps_url")),
                scraped_at=clean_text(row.get("scraped_at")),
            )
            seen.add(build_lead_key(lead))
    return seen


def load_seen_keys_from_outputs(output_paths: List[str]) -> set[str]:
    seen: set[str] = set()
    for path in output_paths:
        seen |= load_seen_keys_from_csv(path)
    return seen


def prepare_output_csv(path: str, resume: bool) -> None:
    if resume and os.path.exists(path):
        return
    init_csv(path)


def km_to_lat_delta(km: float) -> float:
    return km / 111.0


def km_to_lng_delta(km: float, lat: float) -> float:
    cos_lat = max(0.1, math.cos(math.radians(lat)))
    return km / (111.0 * cos_lat)


def estimate_zoom_for_cell(cell_km: float, lat: float, viewport_width_px: int = 1280) -> int:
    meters_per_pixel = (cell_km * 1000.0) / max(1, viewport_width_px)
    cos_lat = max(0.1, math.cos(math.radians(lat)))
    raw_zoom = math.log2((156543.03392 * cos_lat) / max(1e-9, meters_per_pixel))
    return max(7, min(17, int(round(raw_zoom))))


def normalize_domain(website: str) -> str:
    if not website:
        return ""
    parsed = urlparse(website)
    netloc = (parsed.netloc or "").lower()
    if netloc.startswith("www."):
        netloc = netloc[4:]
    return netloc


def normalize_phone(phone: str) -> str:
    if not phone:
        return ""
    return re.sub(r"[^0-9+]", "", phone)


def build_lead_key(lead: TrainerLead) -> str:
    name_key = re.sub(r"\s+", " ", lead.business_name.lower()).strip()
    phone_key = normalize_phone(lead.phone)
    domain_key = normalize_domain(lead.website)
    return f"{name_key}|{phone_key}|{domain_key}"


def handle_google_consent(page) -> None:
    # Google consent UI varies by region/language; try common button labels.
    consent_selectors = [
        'button:has-text("Accept all")',
        'button:has-text("I agree")',
        'button:has-text("Reject all")',
        'button:has-text("Tout accepter")',
        'button:has-text("Tout refuser")',
        'button:has-text("Alle akzeptieren")',
        'button:has-text("Alles ablehnen")',
        'button:has-text("Akkoord")',
        'button:has-text("Alles accepteren")',
        'button:has-text("Accetta tutto")',
    ]

    for selector in consent_selectors:
        button = page.locator(selector).first
        try:
            if button.count() > 0 and button.is_visible(timeout=1200):
                button.click(timeout=3000)
                page.wait_for_timeout(1500)
                return
        except Exception:
            continue


def submit_maps_query(page, query: str) -> None:
    # Maps uses changing IDs (e.g., ucc-5), so prefer robust selectors first.
    selector_candidates = [
        'input[role="combobox"][aria-label*="Search"]',
        'input[role="combobox"][aria-label*="Rechercher"]',
        'input[role="combobox"][aria-label*="Suche"]',
        'input[role="combobox"][aria-label*="Cerca"]',
        'input[role="combobox"][aria-label*="Buscar"]',
        'input[id^="searchboxinput"]',
        'input[id^="ucc-"]',
        'input[name="q"]',
    ]

    search_input = None
    for selector in selector_candidates:
        candidate = page.locator(selector).first
        try:
            if candidate.count() > 0 and candidate.is_visible(timeout=1500):
                search_input = candidate
                break
        except Exception:
            continue

    if search_input is None:
        raise RuntimeError("Could not find Google Maps search input.")

    search_input.click()
    search_input.fill("")
    search_input.fill(query)
    page.keyboard.press("Enter")
    page.wait_for_timeout(2500)


def search_maps(page, query: str) -> None:
    page.goto("https://www.google.com/maps", wait_until="domcontentloaded")
    randomized_sleep()
    handle_google_consent(page)
    submit_maps_query(page, query)
def search_maps_at_point(page, keyword: str, country: str, lat: float, lng: float, zoom: int) -> None:
    # Use coordinate-anchored search URL to keep results local to the cell.
    encoded_keyword = quote_plus(keyword+" in "+country)
    page.goto(
        f"https://www.google.com/maps/search/{encoded_keyword}/@{lat},{lng},{zoom}z?hl=en",
        wait_until="domcontentloaded",
    )
    randomized_sleep()
    handle_google_consent(page)
    # If Maps loaded broad results, force local refresh for the current viewport.
    search_area_button = page.locator('button:has-text("Search this area")').first
    try:
        if search_area_button.count() > 0 and search_area_button.is_visible(timeout=1500):
            search_area_button.click(timeout=3000)
            page.wait_for_timeout(1800)
    except Exception:
        # Fallback: do a local-intent query using explicit coordinates.
        query = f"{keyword} near {lat:.5f}, {lng:.5f}, {country}"
        submit_maps_query(page, query)


def scroll_results_feed(page, rounds: int = 15) -> None:
    feed = page.locator('div[role="feed"]').first
    if feed.count() == 0:
        return

    print("Scrolling results feed...")
    for _ in range(rounds):
        try:
            feed.hover(timeout=3000)
            page.mouse.wheel(0, 6000)
            page.wait_for_timeout(1200)
        except PlaywrightTimeoutError:
            print(f"[INFO] Scroll results feed timed out")
            break

def extract_phone_text(page) -> str:
    # Google Maps cards usually contain phone in "button[data-item-id*=phone]".
    phone_button = page.locator('button[data-item-id*="phone"]').first
    if phone_button.count() > 0:
        return clean_text(phone_button.inner_text(timeout=1500))
    return ""
def extract_phone_text_v2(card) -> str:
    # Google Maps cards usually contain phone in "button[data-item-id*=phone]".
    phone_button = card.locator('span.UsdlK').first
    if phone_button.count() > 0:
        return clean_text(phone_button.inner_text(timeout=1500))
    return ""
def extract_website(page) -> str:
    site_link = page.locator('a[data-item-id="authority"]').first
    if site_link.count() > 0:
        href = site_link.get_attribute("href", timeout=1500)
        return clean_text(href)
    return ""
def extract_website_v2(card) -> str:
    site_link = card.locator('a.lcr4fd').first
    if site_link.count() > 0:
        href = site_link.get_attribute("href", timeout=1500)
        return clean_text(href)
    return ""
def extract_address(card) -> str:
    address_button = card.locator('button[data-item-id*="address"]').first
    if address_button.count() > 0:
        return clean_text(address_button.inner_text(timeout=1500))
    return ""
def extract_address_from_page(page) -> str:
    address_button = page.locator('button[data-item-id*="address"]').first
    if address_button.count() > 0 and address_button.locator('div.Io6YTe').first.count() > 0:
        return clean_text(address_button.locator('div.Io6YTe').first.inner_text(timeout=1500))
    return ""
def is_in_target_country(country: str, address: str, maps_url: str) -> bool:
    country_lower = country.strip().lower()
    aliases = COUNTRY_ALIASES.get(country_lower, {country_lower})
    haystack = f"{address} {maps_url}".lower()
    return any(alias in haystack for alias in aliases)
def extract_email_from_site(context, website: str) -> str:
    if not website:
        return ""

    parsed = urlparse(website)
    if parsed.scheme not in {"http", "https"}:
        return ""

    page = context.new_page()
    try:
        page.goto(website, wait_until="domcontentloaded", timeout=10000)
        randomized_sleep(0.5, 1.0)
        body = page.content()
        emails = sorted(set(EMAIL_REGEX.findall(body)))
        if emails:
            return emails[0]

        # A lightweight fallback: try common contact path.
        root = f"{parsed.scheme}://{parsed.netloc}"
        page.goto(f"{root}/contact", wait_until="domcontentloaded", timeout=7000)
        randomized_sleep(0.5, 1.0)
        contact_html = page.content()
        emails = sorted(set(EMAIL_REGEX.findall(contact_html)))
        if emails:
            return emails[0]
    except Exception:
        return ""
    finally:
        page.close()

    return ""


def collect_listings(
    page,
    context,
    country: str,
    city: str,
    keyword: str,
    max_results: int,
    skip_email_crawl: bool,
    seen_names: set[str] | None = None,
) -> List[TrainerLead]:
    records: List[TrainerLead] = []
    if seen_names is None:
        seen_names = set()

    scroll_results_feed(page)
    page.set_default_timeout(random.randint(15_000, 30_000))
    cards = page.locator('div.bfdHYd')
    clickable_cards = page.locator('a.hfpxzc')
    card_count = cards.count()
    #to_process = min(card_count, max_results)

    for idx in range(card_count):
        try:
            card = cards.nth(idx)
            clickable_card = clickable_cards.nth(idx)

            # Read the list-card title first so we can skip duplicates without clicking.
            title = clean_text(card.locator('div.qBF1Pd').first.inner_text(timeout=2500))
            if not title or title in seen_names:
                continue

            # check if the result is a Personal Trainer. Get the second last div.W4Efsd
            personal_trainer = card.locator('div.W4Efsd').nth(-2).locator('span').first.locator('span').first.inner_text(timeout=2500)
            if personal_trainer and not 'personal trainer' in personal_trainer.lower():
                print(f"[INFO] Not a Personal Trainer: {personal_trainer}")
                continue

            before_url = page.url
            clickable_card.scroll_into_view_if_needed(timeout=1500)
            clickable_card.click(timeout=2500)
            try:
                page.wait_for_function(
                    "(prev) => window.location.href !== prev",
                    arg=before_url,
                    timeout=2500,
                )
            except PlaywrightTimeoutError:
                # Some clicks keep the same URL; give the details panel a moment to settle.
                page.wait_for_timeout(500)

            print(f"[INFO] Title: {title}")
            seen_names.add(title)

            phone = extract_phone_text_v2(card)
            website = extract_website_v2(card) or extract_website(page)
            address = extract_address_from_page(page)
            email = "" if skip_email_crawl else extract_email_from_site(context, website)
            maps_url = page.url

            if not is_in_target_country(country, address, maps_url):
                print(f"[INFO] Skipping out-of-country result: {title}")
                continue

            records.append(
                TrainerLead(
                    country=country,
                    city=city,
                    keyword=personal_trainer,
                    business_name=title,
                    phone=phone,
                    website=website,
                    email=email,
                    address=address,
                    maps_url=maps_url,
                    scraped_at=datetime.now(timezone.utc).isoformat(),
                )
            )

            if len(records) >= max_results:
                break

            randomized_sleep()
        except Exception:
            continue
    return records


def collect_listings_with_dedupe(
    page,
    context,
    country: str,
    city: str,
    keyword: str,
    max_results: int,
    skip_email_crawl: bool,
    seen_keys: set[str],
    seen_names: set[str] | None = None,
    on_unique_row: Optional[callable] = None,
) -> tuple[List[TrainerLead], int]:
    rows = collect_listings(
        page=page,
        context=context,
        country=country,
        city=city,
        keyword=keyword,
        max_results=max_results,
        skip_email_crawl=skip_email_crawl,
        seen_names=seen_names,
    )
    unique_rows: List[TrainerLead] = []
    for row in rows:
        key = build_lead_key(row)
        if key in seen_keys:
            continue
        seen_keys.add(key)
        unique_rows.append(row)
        if on_unique_row is not None:
            on_unique_row(row)
    return unique_rows, len(unique_rows)


def estimate_result_count(page) -> int:
    scroll_results_feed(page, rounds=18)
    cards = page.locator('div.bfdHYd') #a.hfpxzc
    return cards.count()


def should_subdivide(
    result_count: int,
    new_unique_count: int,
    cell_size_km: float,
    depth: int,
    args: argparse.Namespace,
) -> bool:
    if depth >= args.max_grid_depth or cell_size_km <= args.min_cell_km:
        return False

    if result_count <= args.dead_zone_max:
        return False
    if result_count <= args.ok_zone_max:
        return False
    if new_unique_count < args.min_new_uniques_per_child and result_count < args.maps_cap:
        return False
    return True


def subdivide_cell(cell: GridCell) -> List[GridCell]:
    child_size = cell.size_km / 2.0
    lat_shift = km_to_lat_delta(child_size / 2.0)
    lng_shift = km_to_lng_delta(child_size / 2.0, cell.center_lat)
    return [
        GridCell(cell.center_lat - lat_shift, cell.center_lng - lng_shift, child_size, cell.depth + 1),
        GridCell(cell.center_lat - lat_shift, cell.center_lng + lng_shift, child_size, cell.depth + 1),
        GridCell(cell.center_lat + lat_shift, cell.center_lng - lng_shift, child_size, cell.depth + 1),
        GridCell(cell.center_lat + lat_shift, cell.center_lng + lng_shift, child_size, cell.depth + 1),
    ]


def build_initial_grid(min_lat: float, min_lng: float, max_lat: float, max_lng: float, cell_km: float) -> List[GridCell]:
    cells: List[GridCell] = []
    lat_step = km_to_lat_delta(cell_km)
    lat = min_lat
    while lat <= max_lat:
        lng_step = km_to_lng_delta(cell_km, lat)
        lng = min_lng
        while lng <= max_lng:
            cells.append(
                GridCell(
                    center_lat=min(lat + (lat_step / 2.0), max_lat),
                    center_lng=min(lng + (lng_step / 2.0), max_lng),
                    size_km=cell_km,
                    depth=0,
                )
            )
            lng += lng_step
        lat += lat_step
    return cells


def run_adaptive_grid(
    page,
    context,
    country: str,
    keyword: str,
    seen_keys: set[str],
    args: argparse.Namespace,
    bbox: tuple[float, float, float, float],
    run_key: str,
    done_cells: set[str],
    checkpoint_file: str,
    log_file: str,
    on_unique_row: Optional[callable] = None,
) -> List[TrainerLead]:
    min_lat, min_lng, max_lat, max_lng = bbox
    pending = build_initial_grid(min_lat, min_lng, max_lat, max_lng, args.initial_cell_km)
    visited: set[str] = set()
    seen_names_bbox: set[str] = set()
    rows: List[TrainerLead] = []

    log_message(log_file, f"[INFO] Pending cells: {len(pending)} run_key='{run_key}'")
    while pending:
        cell = pending.pop(0)
        remaining_cells = len(pending)
        log_message(
            log_file,
            "[GRID] Processing cell "
            f"depth={cell.depth} "
            f"center=({cell.center_lat:.5f},{cell.center_lng:.5f}) "
            f"size_km={cell.size_km:.2f} "
            f"remaining={remaining_cells} "
            f"run_key='{run_key}'"
        )
        visit_key = f"{keyword}|{round(cell.center_lat, 5)}|{round(cell.center_lng, 5)}|{round(cell.size_km, 2)}"
        cell_done_key = f"{run_key}|{visit_key}"
        if cell_done_key in done_cells:
            log_message(log_file, f"[GRID] Skipping checkpointed cell visit_key='{visit_key}'")
            continue
        if visit_key in visited:
            continue
        visited.add(visit_key)

        zoom = estimate_zoom_for_cell(cell.size_km, cell.center_lat)
        try:
            search_maps_at_point(page, keyword, country, cell.center_lat, cell.center_lng, zoom)
            result_count = estimate_result_count(page)
            unique_rows, new_count = collect_listings_with_dedupe(
                page=page,
                context=context,
                country=country,
                city=f"grid({cell.center_lat:.4f},{cell.center_lng:.4f})",
                keyword=keyword,
                max_results=args.max_results_per_query,
                skip_email_crawl=args.skip_email_crawl,
                seen_keys=seen_keys,
                seen_names=seen_names_bbox,
                on_unique_row=on_unique_row,
            )
            rows.extend(unique_rows)

            log_message(
                log_file,
                "[GRID] "
                f"keyword='{keyword}' "
                f"depth={cell.depth} size_km={cell.size_km:.2f} "
                f"results={result_count} new_uniques={new_count} "
                f"run_key='{run_key}'"
            )
            if should_subdivide(result_count, new_count, cell.size_km, cell.depth, args):
                pending.extend(subdivide_cell(cell))
            done_cells.add(cell_done_key)
            append_checkpoint_event(
                checkpoint_file,
                {
                    "type": "cell_done",
                    "run_key": run_key,
                    "visit_key": visit_key,
                },
            )
        except Exception as exc:
            log_message(
                log_file,
                "[WARN] Grid cell failed "
                f"(lat={cell.center_lat:.5f}, lng={cell.center_lng:.5f}, size={cell.size_km:.2f}): {exc}"
            )
            continue
    return rows


def init_csv(output: str) -> None:
    fieldnames = list(TrainerLead.__annotations__.keys())
    output_dir = os.path.dirname(output)
    if output_dir:
        os.makedirs(output_dir, exist_ok=True)
    with open(output, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()


def append_csv_row(output: str, row: TrainerLead) -> None:
    fieldnames = list(TrainerLead.__annotations__.keys())
    with open(output, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writerow(asdict(row))


def main() -> None:
    args = parse_args()
    countries = [c.strip() for c in args.countries.split(",") if c.strip()]
    cities = [c.strip() for c in args.cities.split(",") if c.strip()]
    keywords = [k.strip() for k in args.keywords.split(",") if k.strip()]
    pairs = get_country_city_pairs(countries, cities)

    if not countries:
        raise ValueError("No countries provided.")
    if not keywords:
        raise ValueError("No keywords provided.")
    if args.grid_mode and not args.bbox and not args.bboxes:
        raise ValueError("--grid-mode requires --bbox or --bboxes")

    log_file = args.log_file or default_log_file(args.output)

    bboxes_list: List[tuple[float, float, float, float]] = []
    if args.grid_mode:
        bboxes_list = parse_bboxes(args.bboxes) if args.bboxes else [parse_bbox(args.bbox)]
    split_bbox_outputs = args.grid_mode and len(bboxes_list) > 1
    grid_output_paths = grid_bbox_output_paths(args.output, len(bboxes_list)) if args.grid_mode else [args.output]

    if args.resume:
        if split_bbox_outputs:
            done_cells: set[str] = set()
            done_bboxes: set[str] = set()
            if args.checkpoint_file:
                done_cells, done_bboxes = load_checkpoint_state(args.checkpoint_file)
            else:
                for path in grid_output_paths:
                    dc, db = load_checkpoint_state(default_checkpoint_file(path))
                    done_cells |= dc
                    done_bboxes |= db
            seen_lead_keys = load_seen_keys_from_outputs(grid_output_paths)
        else:
            checkpoint_file_single = args.checkpoint_file or default_checkpoint_file(args.output)
            done_cells, done_bboxes = load_checkpoint_state(checkpoint_file_single)
            seen_lead_keys = load_seen_keys_from_csv(args.output)
            if not os.path.exists(args.output):
                init_csv(args.output)
    else:
        done_cells, done_bboxes = set(), set()
        seen_lead_keys = set()
        if args.grid_mode:
            if not split_bbox_outputs:
                init_csv(args.output)
        else:
            init_csv(args.output)

    log_message(log_file, "[INFO] Starting scraper run")
    log_message(
        log_file,
        f"[INFO] resume={args.resume} base_output='{args.output}' "
        f"split_bbox_outputs={split_bbox_outputs} log='{log_file}'",
    )
    if split_bbox_outputs:
        log_message(log_file, f"[INFO] Per-bbox output files: {grid_output_paths}")
    if args.resume:
        checkpoint_desc = (
            args.checkpoint_file
            if args.checkpoint_file
            else ("per-bbox <output>.checkpoint.jsonl" if split_bbox_outputs else default_checkpoint_file(args.output))
        )
        log_message(
            log_file,
            f"[INFO] Loaded checkpoint(s) '{checkpoint_desc}': "
            f"done_bboxes={len(done_bboxes)} done_cells={len(done_cells)}",
        )

    total_written = 0
    proxy_pool = load_proxy_pool_from_env()
    proxy_rotation_mode = choose_proxy_rotation_mode(args, len(proxy_pool))
    proxy_index = 0

    if proxy_pool:
        log_message(
            log_file,
            f"[INFO] Proxy pool enabled: count={len(proxy_pool)} rotation_mode='{proxy_rotation_mode}'",
        )
    else:
        log_message(log_file, "[INFO] Proxy pool disabled")

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=args.headless)
        context = None
        page = None

        def open_session(reason: str):
            nonlocal context, page, proxy_index
            if context is not None:
                context.close()
                context = None
                page = None

            context_kwargs = {"locale": "en-US"}
            if proxy_pool:
                proxy_cfg = proxy_pool[proxy_index % len(proxy_pool)]
                proxy_index += 1
                context_kwargs["proxy"] = proxy_cfg
                log_message(
                    log_file,
                    f"[INFO] Using proxy for {reason}: {summarize_proxy(proxy_cfg)}",
                )
            context = browser.new_context(**context_kwargs)
            page = context.new_page()
            page.set_default_timeout(15000)
            return context, page

        open_session("initial session")

        if args.grid_mode:
            bboxes = bboxes_list
            for country in countries:
                for keyword in keywords:
                    log_message(
                        log_file,
                        f"[INFO] Grid mode: keyword='{keyword}' country='{country}' "
                        f"bboxes={len(bboxes)}"
                    )
                    for bbox_idx, bbox in enumerate(bboxes, start=1):
                        bbox_output = (
                            output_path_for_grid_bbox(args.output, bbox_idx)
                            if split_bbox_outputs
                            else args.output
                        )
                        checkpoint_this_bbox = (
                            args.checkpoint_file
                            if args.checkpoint_file
                            else default_checkpoint_file(bbox_output)
                        )
                        run_key = checkpoint_key(country, keyword, bbox)
                        if run_key in done_bboxes:
                            log_message(
                                log_file,
                                f"[INFO] Skipping checkpointed bbox {bbox_idx}/{len(bboxes)} run_key='{run_key}'",
                            )
                            continue
                        if proxy_pool and proxy_rotation_mode == "bbox":
                            open_session(
                                f"bbox {bbox_idx}/{len(bboxes)} keyword='{keyword}' country='{country}'"
                            )
                        prepare_output_csv(bbox_output, args.resume)
                        on_unique_row = lambda row, path=bbox_output: append_csv_row(path, row)
                        log_message(
                            log_file,
                            f"[INFO] Starting bbox {bbox_idx}/{len(bboxes)} "
                            f"output='{bbox_output}' checkpoint='{checkpoint_this_bbox}' "
                            f"for keyword='{keyword}': {bbox}"
                        )
                        rows = run_adaptive_grid(
                            page=page,
                            context=context,
                            country=country,
                            keyword=keyword,
                            seen_keys=seen_lead_keys,
                            args=args,
                            bbox=bbox,
                            run_key=run_key,
                            done_cells=done_cells,
                            checkpoint_file=checkpoint_this_bbox,
                            log_file=log_file,
                            on_unique_row=on_unique_row,
                        )
                        total_written += len(rows)
                        done_bboxes.add(run_key)
                        append_checkpoint_event(
                            checkpoint_this_bbox,
                            {
                                "type": "bbox_done",
                                "run_key": run_key,
                            },
                        )
                        log_message(
                            log_file,
                            f"[INFO] Bbox {bbox_idx}/{len(bboxes)} collected "
                            f"{len(rows)} unique rows -> '{bbox_output}'"
                        )
                        is_last_bbox = bbox_idx == len(bboxes)
                        if not is_last_bbox:
                            delay_seconds = randomized_sleep(min_seconds=60, max_seconds=90)
                            log_message(
                                log_file,
                                "[INFO] Waiting between bboxes: "
                                f"{(delay_seconds / 60.0):.2f} min "
                                f"({delay_seconds:.0f} sec)"
                            )
                            time.sleep(delay_seconds)
        else:
            on_unique_row = lambda row: append_csv_row(args.output, row)
            for country, city in pairs:
                for keyword in keywords:
                    query = f"{keyword} in {city}, {country}" if city else f"{keyword} in {country}"
                    log_message(log_file, f"[INFO] Query: {query}")
                    try:
                        if proxy_pool and proxy_rotation_mode == "query":
                            open_session(f"query '{query}'")
                        search_maps(page, query)
                        rows, _ = collect_listings_with_dedupe(
                            page=page,
                            context=context,
                            country=country,
                            city=city,
                            keyword=keyword,
                            max_results=args.max_results_per_query,
                            skip_email_crawl=args.skip_email_crawl,
                            seen_keys=seen_lead_keys,
                            on_unique_row=on_unique_row,
                        )
                        total_written += len(rows)
                        log_message(log_file, f"[INFO] Collected {len(rows)} unique rows for query.")
                    except Exception as exc:
                        log_message(log_file, f"[WARN] Failed query '{query}': {exc}")
                        continue

        browser.close()

    if split_bbox_outputs:
        log_message(
            log_file,
            f"[DONE] Wrote {total_written} unique rows across bbox files: {grid_output_paths}",
        )
    else:
        log_message(log_file, f"[DONE] Wrote {total_written} rows to {args.output}")


if __name__ == "__main__":
    main()
