Build and run:

`docker build -t trainer-scraper .`
`docker run --rm trainer-scraper --countries "France,Germany" --max-results-per-query 10 --output leads.csv`

To persist output to your host folder:

`docker run --rm -v "$(pwd):/app" trainer-scraper --countries "France" --output leads.csv`
https://bboxfinder.com/

**BBOXES
Belgium
50.808538,2.532349,51.369208,3.383789
50.504693,3.298645,51.237847,4.086914
50.296358,4.081421,51.409486,5.072937
50.278809,5.004272,51.263634,5.666199
50.124100,5.589294,50.752097,6.336365
49.968889,4.161072,50.294603,4.913635
49.575102,4.888916,50.213822,5.737610

Germany
52.335339,13.076477,52.728807,13.708191 (Berlin)

#California
38.950865,-124.541016,41.992160,-120.025635
38.324420,-123.706055,38.985033,-119.696045
37.169072,-123.112793,38.337348,-118.157959
35.817813,-122.398682,37.186579,-116.740723
34.443159,-121.398926,35.799994,-115.532227
34.039005,-119.273071,34.361576,-117.333984
33.302986,-118.454590,33.988918,-117.410889
32.551444,-117.246094,34.284453,-114.609375

python3 main.py \
  --countries "Belgium" \
  --keywords "Personal trainer" \
  --grid-mode \
  --bbox "50.808538,2.532349,51.369208,3.383789" \
  --initial-cell-km 15 \
  --min-cell-km 2 \
  --dead-zone-max 20 \
  --ok-zone-max 60 \
  --maps-cap 120 \
  --min-new-uniques-per-child 10 \
  --max-grid-depth 3 \
  --max-results-per-query 120 \
  --skip-email-crawl \
  --output results/Belgium/leads_bbox_1.csv

# Multi-bbox run with delay between each bbox
python3 main.py \
  --countries "Germany" \
  --cities "Berlin" \
  --keywords "Personal trainer" \
  --grid-mode \
  --bboxes "52.335339,13.076477,52.728807,13.708191" \
  --initial-cell-km 15 \
  --min-cell-km 2 \
  --dead-zone-max 20 \
  --ok-zone-max 60 \
  --maps-cap 120 \
  --min-new-uniques-per-child 10 \
  --max-grid-depth 3 \
  --max-results-per-query 120 \
  --skip-email-crawl \
  --log-file results/Belgium/leads.csv.log \
  --output results/Belgium/leads.csv

With multiple bboxes, leads go to separate files: `results/Belgium/leads_bbox_1.csv`, `results/Belgium/leads_bbox_2.csv`, … (same directory and extension as `--output`). Default checkpoint per file is `<that_csv>.checkpoint.jsonl`. If you scrape several countries in one run with the same `--output` base, bbox indices repeat per country—use a different `--output` base per country (e.g. `results/Belgium/leads.csv` vs `results/France/leads.csv`).

# Resume after interruption from saved checkpoint (appends to existing CSV)
python3 main.py \
  --countries "Belgium" \
  --keywords "Personal trainer" \
  --grid-mode \
  --bboxes "50.808538,2.532349,51.369208,3.383789;50.504693,3.298645,51.237847,4.086914" \
  --resume \
  --log-file results/Belgium/leads.csv.log \
  --output results/Belgium/leads.csv

## Proxy rotation (for Hetzner / datacenter IPs)

Set proxies through environment variables (works for local runs and Docker).

- Single proxy:
`export PROXY_URL="http://user:pass@proxy1.example.com:8000"`

- Multiple proxies (rotated):
`export PROXY_LIST="http://user:pass@proxy1.example.com:8000;http://user:pass@proxy2.example.com:8000"`

- Rotation mode:
`export PROXY_ROTATION_MODE="auto"`  
Allowed values: `auto`, `run`, `query`, `bbox`

Behavior:
- `auto`: rotates per `bbox` in `--grid-mode`, otherwise per `query`.
- `run`: one proxy for the whole scraper run.
- `query`: rotate before each query.
- `bbox`: rotate before each bbox (falls back to `query` when not in grid mode).

`ssh root@178.104.56.95` Nuremberg

`sudo apt update`
`sudo apt install -y git`
`cd ~`
# install docker
`sudo apt-get install -y ca-certificates curl`
`sudo install -m 0755 -d /etc/apt/keyrings`
`sudo curl -fsSL https://download.docker.com/linux/debian/gpg -o /etc/apt/keyrings/docker.asc`
`sudo chmod a+r /etc/apt/keyrings/docker.asc`
`echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.asc] https://download.docker.com/linux/debian $(. /etc/os-release && echo "$VERSION_CODENAME") stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null`
If VERSION_CODENAME is empty on your image, check with cat /etc/os-release and replace it manually (e.g. bookworm, trixie).
`sudo apt-get update`
`sudo apt-get install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugin docker-compose-plugin`
[TEST] `sudo docker run --rm hello-world`
`git clone https://github.com/stepup-fitness/stepup-trainer-scraping.git new-folder-name`
`cd stepup-trainer-scraping`

`docker build -t trainer-scraper .`
`docker run -d -v "$(pwd):/app" trainer-scraper --countries "California" \
  --keywords "Personal trainer" \
  --grid-mode \
  --bboxes "-123.706055,38.985033,-119.696045;37.169072,-123.112793,38.337348,-118.157959;35.817813,-122.398682,37.186579,-116.740723;34.443159,-121.398926,35.799994,-115.532227;34.039005,-119.273071,34.361576,-117.333984;33.302986,-118.454590,33.988918,-117.410889;32.551444,-117.246094,34.284453,-114.609375" \
  --initial-cell-km 15 \
  --min-cell-km 2 \
  --dead-zone-max 20 \
  --ok-zone-max 60 \
  --maps-cap 120 \
  --min-new-uniques-per-child 10 \
  --max-grid-depth 3 \
  --max-results-per-query 120 \
  --skip-email-crawl \
  --output results/California/leads.csv`

# To Download result on pc (don't connect with ssh)

cd aws_env/stepup/stepup-trainer-scraping
scp root@178.104.56.95:/root/stepup-12-04-2026-20-46/results/California/leads_bbox_1.csv .
