Build and run:

`docker build -t trainer-scraper .`
`docker run --rm trainer-scraper --countries "France,Germany" --max-results-per-query 10 --output leads.csv`

To persist output to your host folder:

`docker run --rm -v "$(pwd):/app" trainer-scraper --countries "France" --output leads.csv`
https://bboxfinder.com/

**BBOXES
# Belgium
50.808538,2.532349,51.369208,3.383789
50.504693,3.298645,51.237847,4.086914
50.296358,4.081421,51.409486,5.072937
50.278809,5.004272,51.263634,5.666199
50.124100,5.589294,50.752097,6.336365
49.968889,4.161072,50.294603,4.913635
49.575102,4.888916,50.213822,5.737610

# Germany
52.335339,13.076477,52.728807,13.708191 (Berlin)

# California
38.950865,-124.541016,41.992160,-120.025635
38.324420,-123.706055,38.985033,-119.696045
37.169072,-123.112793,38.337348,-118.157959
35.817813,-122.398682,37.186579,-116.740723
34.443159,-121.398926,35.799994,-115.532227
34.039005,-119.273071,34.361576,-117.333984
33.302986,-118.454590,33.988918,-117.410889
32.551444,-117.246094,34.284453,-114.609375

# Hawaii
21.855126,-159.792023,22.250971,-159.275665
21.250982,-158.288269,21.671467,-157.642822
20.567225,-156.717224,21.040287,-155.966034
18.862108,-156.099243,20.275080,-154.783630

# Alaska
58.608334,-158.466797,65.910623,-140.976563
53.956086,-136.230469,58.790978,-130.385742

# Washington
46.019853,-121.036377,48.994636,-117.037354
45.675482,-124.178467,49.001844,-121.069336

docker run -d -v "$(pwd):/app" trainer-scraper --countries "Washington" \
  --keywords "Personal trainer" \
  --grid-mode \
  --bboxes="46.019853,-121.036377,48.994636,-117.037354;45.675482,-124.178467,49.001844,-121.069336" \
  --initial-cell-km 15 \
  --min-cell-km 2 \
  --dead-zone-max 20 \
  --ok-zone-max 60 \
  --maps-cap 120 \
  --min-new-uniques-per-child 10 \
  --max-grid-depth 3 \
  --max-results-per-query 120 \
  --skip-email-crawl \
  --output results/Washington/leads.csv

# Oregon
42.024814,-124.189453,45.721522,-120.168457
42.024814,-120.520020,45.974060,-116.971436

# Canada
59.288332,-137.724609,61.897578,-129.946289
61.627286,-116.850586,63.371832,-112.148438
48.980217,-128.122559,55.850650,-119.948730
49.167339,-119.970703,59.400365,-110.039063
49.525208,-110.039063,59.678835,-101.557617
54.622978,-101.953125,59.966010,-92.395020
48.224673,-101.997070,55.998381,-87.495117
41.738528,-86.484375,55.702355,-55.722656

`docker run -d -v "$(pwd):/app" trainer-scraper --countries "Canada" \
  --keywords "Personal trainer" \
  --grid-mode \
  --bboxes "59.288332,-137.724609,61.897578,-129.946289;61.627286,-116.850586,63.371832,-112.148438;48.980217,-128.122559,55.850650,-119.948730;49.167339,-119.970703,59.400365,-110.039063;49.525208,-110.039063,59.678835,-101.557617;54.622978,-101.953125,59.966010,-92.395020;48.224673,-101.997070,55.998381,-87.495117;41.738528,-86.484375,55.702355,-55.722656" \
  --initial-cell-km 15 \
  --min-cell-km 2 \
  --dead-zone-max 20 \
  --ok-zone-max 60 \
  --maps-cap 120 \
  --min-new-uniques-per-child 10 \
  --max-grid-depth 3 \
  --max-results-per-query 120 \
  --skip-email-crawl \
  --output results/Canada/leads.csv`

# Australia
-26.686730,112.697754,-20.076570,128.935547
-20.756114,121.003418,-13.603278,128.957520
-32.925707,115.565186,-31.052934,116.878052
-35.764260,138.031468,-33.756230,140.212254
-39.019024,144.259957,-32.231216,152.576608
-32.491230,150.864258,-23.503552,153.984375
-23.543845,137.988281,-15.749963,150.820313
-19.993998,128.847656,-11.436955,138.098145
-24.484649,132.006226,-22.885032,135.357056

# United Kingdom
57.621875,-5.910645,58.585436,-3.405762
56.121060,-6.339111,57.742281,-1.730347
54.838664,-5.597534,56.087362,-1.318359
54.191370,-3.587036,54.860801,-0.274658
53.312827,-3.128357,54.183334,0.140076
51.378638,-4.328613,53.396432,-2.268677
51.737235,-2.235718,53.445535,0.269165
51.856139,0.142822,52.961875,1.730347
51.330612,-2.510376,51.710012,0.900879
50.652943,-2.988281,51.385495,1.411743
50.196243,-4.987793,51.212045,-2.980042
54.056164,-7.970581,55.285372,-5.410767

# Ireland
53.255355,-9.909668,54.287675,-6.047974
52.140231,-9.602051,53.232345,-5.949097
51.477962,-10.343628,52.116626,-7.580566

`docker run -d -v "$(pwd):/app" trainer-scraper --countries "Australia" \
  --keywords "Personal trainer" \
  --grid-mode \
  --bboxes="-26.686730,112.697754,-20.076570,128.935547;-20.756114,121.003418,-13.603278,128.957520;-32.925707,115.565186,-31.052934,116.878052;-35.764260,138.031468,-33.756230,140.212254;-39.019024,144.259957,-32.231216,152.576608;-32.491230,150.864258,-23.503552,153.984375;-23.543845,137.988281,-15.749963,150.820313;-19.993998,128.847656,-11.436955,138.098145;-24.484649,132.006226,-22.885032,135.357056" \
  --initial-cell-km 15 \
  --min-cell-km 2 \
  --dead-zone-max 20 \
  --ok-zone-max 60 \
  --maps-cap 120 \
  --min-new-uniques-per-child 10 \
  --max-grid-depth 3 \
  --max-results-per-query 120 \
  --skip-email-crawl \
  --output results/Australia/leads.csv`

# New Zealand
-39.104489,173.858643,-36.155618,175.935059
-39.044786,176.000977,-37.670777,177.901611
-41.697526,173.638916,-38.891033,177.363281
-44.308127,169.650879,-40.813809,174.484863
-46.747389,166.025391,-42.980540,172.122803

`docker run -d -v "$(pwd):/app" trainer-scraper --countries "New Zealand" \
  --keywords "Personal trainer" \
  --grid-mode \
  --bboxes="-39.104489,173.858643,-36.155618,175.935059;-39.044786,176.000977,-37.670777,177.901611;-41.697526,173.638916,-38.891033,177.363281;-44.308127,169.650879,-40.813809,174.484863;-46.747389,166.025391,-42.980540,172.122803" \
  --initial-cell-km 15 \
  --min-cell-km 2 \
  --dead-zone-max 20 \
  --ok-zone-max 60 \
  --maps-cap 120 \
  --min-new-uniques-per-child 10 \
  --max-grid-depth 3 \
  --max-results-per-query 120 \
  --skip-email-crawl \
  --output results/New_Zealand/leads.csv`

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

`ssh root@178.104.56.95` Nuremberg (1)      -> California
`ssh root@62.238.22.24` Helsinki (1)        -> Hawaii, Washington
`ssh root@178.104.184.6` Falkenstein (1)    -> Alaska, Oregon
`ssh root@178.104.199.217` Nuremberg (2)    -> Canada
`ssh root@91.99.216.183` Falkenstein (2)    -> Australia
`ssh root@62.238.3.134` Helsinki (2)        -> New Zealand

`sudo apt update`
`sudo apt install -y git`
`cd ~`
# install docker
`sudo apt-get install -y git ca-certificates curl`
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
  --bboxes "38.324420,-123.706055,38.985033,-119.696045;37.169072,-123.112793,38.337348,-118.157959;35.817813,-122.398682,37.186579,-116.740723;34.443159,-121.398926,35.799994,-115.532227;34.039005,-119.273071,34.361576,-117.333984;33.302986,-118.454590,33.988918,-117.410889;32.551444,-117.246094,34.284453,-114.609375" \
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

`docker run -d -v "$(pwd):/app" trainer-scraper --countries "Hawaii" \
  --keywords "Personal trainer" \
  --grid-mode \
  --bboxes "21.855126,-159.792023,22.250971,-159.275665;21.250982,-158.288269,21.671467,-157.642822;20.567225,-156.717224,21.040287,-155.966034;18.862108,-156.099243,20.275080,-154.783630" \
  --initial-cell-km 15 \
  --min-cell-km 2 \
  --dead-zone-max 20 \
  --ok-zone-max 60 \
  --maps-cap 120 \
  --min-new-uniques-per-child 10 \
  --max-grid-depth 3 \
  --max-results-per-query 120 \
  --skip-email-crawl \
  --output results/Hawaii/leads.csv`

`docker run -d -v "$(pwd):/app" trainer-scraper --countries "Alaska" \
  --keywords "Personal trainer" \
  --grid-mode \
  --bboxes "58.608334,-158.466797,65.910623,-140.976563;53.956086,-136.230469,58.790978,-130.385742" \
  --initial-cell-km 15 \
  --min-cell-km 2 \
  --dead-zone-max 20 \
  --ok-zone-max 60 \
  --maps-cap 120 \
  --min-new-uniques-per-child 10 \
  --max-grid-depth 3 \
  --max-results-per-query 120 \
  --skip-email-crawl \
  --output results/Alaska/leads.csv`