FROM mcr.microsoft.com/playwright/python:v1.58.0-jammy

WORKDIR /app

COPY requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r /app/requirements.txt

COPY . /app

ENTRYPOINT ["python", "extract_contact_openai.py"]
