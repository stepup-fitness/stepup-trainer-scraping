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
49.521643,5.763702,49.787471,5.942230

# Germany
53.823354,8.552856,54.908199,10.025024
53.826597,9.964600,54.450880,10.964355
52.656394,7.157593,53.878440,11.953125
52.819363,12.233276,54.402946,14.381104
51.869708,12.255249,52.799440,14.622803 (Berlin)
51.862924,9.420776,52.619725,12.255249
51.923943,7.080688,52.412472,9.678955
50.562304,6.207275,51.886664,9.970093
50.387508,9.948120,51.655519,14.798584
49.210420,6.597290,50.275299,12.084961
47.565407,7.509155,49.048670,10.469971
47.483801,10.398560,48.944151,13.765869

docker run -d -v "$(pwd):/app" trainer-scraper --countries "Germany" \
  --keywords "Personal trainer" \
  --grid-mode \
  --bboxes="53.823354,8.552856,54.908199,10.025024;53.826597,9.964600,54.450880,10.964355;52.656394,7.157593,53.878440,11.953125;52.819363,12.233276,54.402946,14.381104;51.869708,12.255249,52.799440,14.622803;51.862924,9.420776,52.619725,12.255249;51.923943,7.080688,52.412472,9.678955;50.562304,6.207275,51.886664,9.970093;50.387508,9.948120,51.655519,14.798584;49.210420,6.597290,50.275299,12.084961;47.565407,7.509155,49.048670,10.469971;47.483801,10.398560,48.944151,13.765869" \
  --initial-cell-km 15 \
  --min-cell-km 2 \
  --dead-zone-max 20 \
  --ok-zone-max 60 \
  --maps-cap 120 \
  --min-new-uniques-per-child 10 \
  --max-grid-depth 3 \
  --max-results-per-query 120 \
  --skip-email-crawl \
  --output results/Germany/leads.csv

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

docker run -d -v "$(pwd):/app" trainer-scraper --countries "Oregon" \
  --keywords "Personal trainer" \
  --grid-mode \
  --bboxes="42.024814,-124.189453,45.721522,-120.168457;42.024814,-120.520020,45.974060,-116.971436" \
  --initial-cell-km 15 \
  --min-cell-km 2 \
  --dead-zone-max 20 \
  --ok-zone-max 60 \
  --maps-cap 120 \
  --min-new-uniques-per-child 10 \
  --max-grid-depth 3 \
  --max-results-per-query 120 \
  --skip-email-crawl \
  --output results/Oregon/leads.csv

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

docker run -d -v "$(pwd):/app" trainer-scraper --countries "United Kingdom" \
  --keywords "Personal trainer" \
  --grid-mode \
  --bboxes="57.621875,-5.910645,58.585436,-3.405762;56.121060,-6.339111,57.742281,-1.730347;54.838664,-5.597534,56.087362,-1.318359;54.191370,-3.587036,54.860801,-0.274658;53.312827,-3.128357,54.183334,0.140076;51.378638,-4.328613,53.396432,-2.268677;51.737235,-2.235718,53.445535,0.269165;51.856139,0.142822,52.961875,1.730347;51.330612,-2.510376,51.710012,0.900879;50.652943,-2.988281,51.385495,1.411743;50.196243,-4.987793,51.212045,-2.980042;54.056164,-7.970581,55.285372,-5.410767" \
  --initial-cell-km 15 \
  --min-cell-km 2 \
  --dead-zone-max 20 \
  --ok-zone-max 60 \
  --maps-cap 120 \
  --min-new-uniques-per-child 10 \
  --max-grid-depth 3 \
  --max-results-per-query 120 \
  --skip-email-crawl \
  --output results/United_Kingdom/leads.csv

# Ireland
53.255355,-9.909668,54.287675,-6.047974
52.140231,-9.602051,53.232345,-5.949097
51.477962,-10.343628,52.116626,-7.580566

# Spain
41.718030,-9.244995,43.659924,-5.921631
41.562032,-5.822754,43.492783,-1.400757
41.578471,-1.389771,43.016697,0.856934
41.029643,0.900879,42.439674,3.191528
39.825413,-6.877441,41.203456,-3.087158
39.892880,-3.142090,41.327326,0.439453
38.169114,-3.197021,39.960280,0.252686
38.108628,-7.272949,39.410733,-3.262939
37.147182,-7.437744,38.082690,-3.268433
37.147182,-3.251953,38.186387,-0.598755
36.664013,-6.509399,37.085858,-1.867676
36.004673,-6.448975,36.716871,-4.383545

# Montana
47.809465,-116.037598,49.001844,-110.626831
46.611715,-115.180664,47.835283,-110.670776
45.011419,-114.312744,46.581518,-104.051514

# Idaho
47.548725,-117.029114,48.998240,-116.065063
41.996243,-117.004395,44.127028,-114.356689
42.000325,-114.384155,44.044167,-111.044312

# Italy
45.544831,12.420044,46.653207,13.573608
45.475540,10.453491,46.987747,12.529907
45.824971,8.989563,46.502173,10.508423
45.110362,8.577576,45.847934,10.494690
45.821143,7.890930,46.422713,8.920898
44.844186,6.748352,45.945421,7.940369
43.771094,6.869202,44.902578,8.313904
44.400430,7.918396,45.673563,8.679199
44.091531,8.714905,45.151053,10.840759
44.197959,10.805054,45.127805,12.425537
43.574422,9.992065,44.130971,13.601074
42.879990,10.269470,43.568452,13.927917
42.368691,10.755615,42.918218,14.403076
42.012571,11.579590,42.362603,15.051270
41.662653,12.016296,41.998284,12.914429
41.395355,12.900696,41.988077,15.004578
41.343825,12.444763,41.691373,13.073730
41.202423,12.889709,41.403596,15.034790
41.223085,15.029297,41.974806,16.546783
40.524239,13.771362,41.213788,17.130432
39.597223,14.883728,40.524239,17.078247
39.770548,17.053528,41.085562,18.597107
38.884619,15.842285,39.599340,17.218323
37.905199,15.614319,38.935912,16.946411
36.611118,12.299194,38.419166,15.639038
38.835429,8.085938,41.310824,9.843750

# France
50.110011,1.477661,51.131108,2.576294
50.110011,2.592773,50.781629,3.257446
50.127622,3.273926,50.494211,4.152832
49.567978,1.452942,50.134664,4.177551
49.014455,0.013733,50.018329,1.472168
48.770672,4.150085,49.984786,4.822998
48.754378,4.875183,49.786584,6.361084
48.730832,6.350098,49.443129,8.179321
48.266741,1.367798,49.435985,4.334106
48.589326,-1.917114,49.713825,0.082397
47.286682,-4.833984,48.846643,-1.433716
47.450380,4.372559,48.698212,7.866211
46.316584,-2.076416,48.531157,0.703125
46.316584,0.703125,48.011975,4.229736
46.149394,4.290161,47.368594,7.064209
43.012681,4.262695,46.210250,7.042236
43.536603,6.943359,44.308127,7.717896
43.476840,-1.527100,46.263443,4.097900
42.386951,-1.807251,43.532620,3.592529

# Nevada
40.082274,-118.789673,41.224118,-114.472046
38.933776,-120.003662,40.170479,-114.060059
37.596824,-119.910278,38.933776,-114.060059
35.541166,-117.053833,37.596824,-114.054565
34.770948,-115.136719,35.469618,-114.139709

# Arizona
35.915747,-114.049072,36.998166,-109.039307
34.939985,-114.730225,35.986896,-109.039307
32.708733,-114.713745,34.858890,-109.055786
31.325487,-114.796143,32.667125,-109.039307

# Utah
37.002553,-114.049072,39.206719,-109.050293
39.223743,-114.027100,40.988192,-109.061279
40.990265,-114.049072,42.002366,-111.049805

# Wyoming
43.715535,-111.049805,45.003651,-104.073486
42.061529,-111.044312,43.707594,-104.040527
40.992338,-111.055298,42.098222,-104.046021

# Colorado
39.181175,-109.039307,40.996484,-102.052002
37.006939,-109.044800,39.270537,-102.041016

# Netherlands
52.626395,4.438477,53.657661,7.272949
51.825593,3.861694,52.639730,7.102661
51.210325,3.356323,51.815407,6.229248
50.742539,5.618134,51.182786,6.179810

# Sweden
65.757706,14.545898,69.154740,24.719238
63.233627,11.821289,65.302650,22.082520
59.723177,11.843262,63.243521,19.116211
54.597528,11.052246,59.756395,19.138184

# New Mexico
35.581384,-109.039307,36.998166,-103.018799
33.637489,-109.050293,35.626047,-103.035278
31.330179,-109.039307,33.678640,-103.051758

docker run -d -v "$(pwd):/app" trainer-scraper --countries "New Mexico" \
  --keywords "Personal trainer" \
  --grid-mode \
  --bboxes="35.581384,-109.039307,36.998166,-103.018799;33.637489,-109.050293,35.626047,-103.035278;31.330179,-109.039307,33.678640,-103.051758" \
  --initial-cell-km 15 \
  --min-cell-km 2 \
  --dead-zone-max 20 \
  --ok-zone-max 60 \
  --maps-cap 120 \
  --min-new-uniques-per-child 10 \
  --max-grid-depth 3 \
  --max-results-per-query 120 \
  --skip-email-crawl \
  --output results/New_Mexico/leads.csv

# Norway
68.576441,12.480469,71.052665,28.740234
63.411198,8.789063,68.171555,18.325195
57.973157,4.658203,63.411198,12.941895

# Texas
34.633208,-103.029785,36.509636,-100.019531
32.008076,-103.040771,34.506557,-94.042969
29.764377,-106.600342,32.008076,-93.504639
25.799891,-101.557617,29.802518,-93.801270

# Oklahoma
36.500805,-103.002319,37.002553,-94.619751
33.651208,-99.997559,36.509636,-94.405518

# Denmark
55.838314,7.981567,57.765729,10.980835
54.559323,8.091431,56.111873,12.716675

# Finland
65.694476,23.071289,69.801724,30.454102
63.450509,22.126465,65.685430,30.871582
59.811685,21.027832,62.935235,31.618652

# Switzerland
47.058896,6.685181,47.805776,9.665222
46.122749,5.949097,47.055154,6.825256
45.853673,6.767578,47.032695,8.456726
45.817315,8.379822,47.043926,10.461731

# Louisiana
31.896214,-94.042969,33.027088,-90.911865
30.996446,-93.960571,31.914868,-91.373291
29.171349,-93.740845,31.015279,-89.423218

# Arkansas
35.038992,-94.603271,36.518466,-90.285645
33.568861,-94.482422,35.137879,-90.203247
33.017876,-94.042969,33.536816,-91.005249

# Kansas
36.993778,-102.062988,40.002372,-94.097900

# Nebraska
40.010787,-104.062500,43.020714,-95.284424

# South Dakota
42.996612,-104.040527,45.951150,-96.437988

# North Dakota
45.943511,-104.040527,48.994636,-96.525879

# Minnesota
46.739861,-97.229004,49.339441,-89.780273
43.516689,-96.800537,46.830134,-91.944580

# Iowa
40.597271,-96.547852,43.548548,-90.307617

# Austria
46.623034,9.569092,47.779943,12.947388
46.384833,12.892456,49.066668,17.105713

# Missouri
39.083172,-95.762329,40.601441,-90.543823
36.496390,-94.652710,39.138582,-89.274902

# Mississippi
33.408517,-91.241455,35.021000,-88.044434
31.793555,-91.400757,33.399345,-88.236694
31.015279,-91.669922,31.788886,-88.406982
30.197366,-89.846191,31.010571,-88.404236

# Tennessee
35.007503,-90.302124,36.628754,-85.308838
34.989504,-85.231934,36.602299,-82.359009

docker run -d -v "$(pwd):/app" trainer-scraper --countries "Tennessee" \
  --keywords "Personal trainer" \
  --grid-mode \
  --bboxes="35.007503,-90.302124,36.628754,-85.308838;34.989504,-85.231934,36.602299,-82.359009" \
  --initial-cell-km 15 \
  --min-cell-km 2 \
  --dead-zone-max 20 \
  --ok-zone-max 60 \
  --maps-cap 120 \
  --min-new-uniques-per-child 10 \
  --max-grid-depth 3 \
  --max-results-per-query 120 \
  --skip-email-crawl \
  --output results/Tennessee/leads.csv

docker run -d -v "$(pwd):/app" trainer-scraper --countries "Mississippi" \
  --keywords "Personal trainer" \
  --grid-mode \
  --bboxes="33.408517,-91.241455,35.021000,-88.044434;31.793555,-91.400757,33.399345,-88.236694;31.015279,-91.669922,31.788886,-88.406982;30.197366,-89.846191,31.010571,-88.404236" \
  --initial-cell-km 15 \
  --min-cell-km 2 \
  --dead-zone-max 20 \
  --ok-zone-max 60 \
  --maps-cap 120 \
  --min-new-uniques-per-child 10 \
  --max-grid-depth 3 \
  --max-results-per-query 120 \
  --skip-email-crawl \
  --output results/Mississippi/leads.csv

docker run -d -v "$(pwd):/app" trainer-scraper --countries "Missouri" \
  --keywords "Personal trainer" \
  --grid-mode \
  --bboxes="39.083172,-95.762329,40.601441,-90.543823;36.496390,-94.652710,39.138582,-89.274902" \
  --initial-cell-km 15 \
  --min-cell-km 2 \
  --dead-zone-max 20 \
  --ok-zone-max 60 \
  --maps-cap 120 \
  --min-new-uniques-per-child 10 \
  --max-grid-depth 3 \
  --max-results-per-query 120 \
  --skip-email-crawl \
  --output results/Missouri/leads.csv

docker run -d -v "$(pwd):/app" trainer-scraper --countries "Austria" \
  --keywords "Personal trainer" \
  --grid-mode \
  --bboxes="46.623034,9.569092,47.779943,12.947388;46.384833,12.892456,49.066668,17.105713" \
  --initial-cell-km 15 \
  --min-cell-km 2 \
  --dead-zone-max 20 \
  --ok-zone-max 60 \
  --maps-cap 120 \
  --min-new-uniques-per-child 10 \
  --max-grid-depth 3 \
  --max-results-per-query 120 \
  --skip-email-crawl \
  --output results/Austria/leads.csv

docker run -d -v "$(pwd):/app" trainer-scraper --countries "Iowa" \
  --keywords "Personal trainer" \
  --grid-mode \
  --bboxes="40.597271,-96.547852,43.548548,-90.307617" \
  --initial-cell-km 15 \
  --min-cell-km 2 \
  --dead-zone-max 20 \
  --ok-zone-max 60 \
  --maps-cap 120 \
  --min-new-uniques-per-child 10 \
  --max-grid-depth 3 \
  --max-results-per-query 120 \
  --skip-email-crawl \
  --output results/Iowa/leads.csv

docker run -d -v "$(pwd):/app" trainer-scraper --countries "Minnesota" \
  --keywords "Personal trainer" \
  --grid-mode \
  --bboxes="46.739861,-97.229004,49.339441,-89.780273;43.516689,-96.800537,46.830134,-91.944580" \
  --initial-cell-km 15 \
  --min-cell-km 2 \
  --dead-zone-max 20 \
  --ok-zone-max 60 \
  --maps-cap 120 \
  --min-new-uniques-per-child 10 \
  --max-grid-depth 3 \
  --max-results-per-query 120 \
  --skip-email-crawl \
  --output results/Minnesota/leads.csv

docker run -d -v "$(pwd):/app" trainer-scraper --countries "North Dakota" \
  --keywords "Personal trainer" \
  --grid-mode \
  --bboxes="45.943511,-104.040527,48.994636,-96.525879" \
  --initial-cell-km 15 \
  --min-cell-km 2 \
  --dead-zone-max 20 \
  --ok-zone-max 60 \
  --maps-cap 120 \
  --min-new-uniques-per-child 10 \
  --max-grid-depth 3 \
  --max-results-per-query 120 \
  --skip-email-crawl \
  --output results/North_Dakota/leads.csv

docker run -d -v "$(pwd):/app" trainer-scraper --countries "South Dakota" \
  --keywords "Personal trainer" \
  --grid-mode \
  --bboxes="42.996612,-104.040527,45.951150,-96.437988" \
  --initial-cell-km 15 \
  --min-cell-km 2 \
  --dead-zone-max 20 \
  --ok-zone-max 60 \
  --maps-cap 120 \
  --min-new-uniques-per-child 10 \
  --max-grid-depth 3 \
  --max-results-per-query 120 \
  --skip-email-crawl \
  --output results/South_Dakota/leads.csv

docker run -d -v "$(pwd):/app" trainer-scraper --countries "Nebraska" \
  --keywords "Personal trainer" \
  --grid-mode \
  --bboxes="40.010787,-104.062500,43.020714,-95.284424" \
  --initial-cell-km 15 \
  --min-cell-km 2 \
  --dead-zone-max 20 \
  --ok-zone-max 60 \
  --maps-cap 120 \
  --min-new-uniques-per-child 10 \
  --max-grid-depth 3 \
  --max-results-per-query 120 \
  --skip-email-crawl \
  --output results/Nebraska/leads.csv

# New Zealand
-39.104489,173.858643,-36.155618,175.935059
-39.044786,176.000977,-37.670777,177.901611
-41.697526,173.638916,-38.891033,177.363281
-44.308127,169.650879,-40.813809,174.484863
-46.747389,166.025391,-42.980540,172.122803

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

`ssh root@178.104.56.95` Nuremberg (1)      -> California, Montana, Nevada, Utah, New Mexico*
`ssh root@62.238.22.24` Helsinki (1)        -> Hawaii, Washington, Idaho, Arizona, Wyoming, Texas, Louisiana, Missouri*
`ssh root@178.104.184.6` Falkenstein (1)    -> Alaska, Oregon, Colorado, Oklahoma, Arkansas, Mississippi*
`ssh root@178.104.199.217` Nuremberg (2)    -> Canada, Kansas*
`ssh root@91.99.216.183` Falkenstein (2)    -> Australia, Switzerland, Nebraska*
`ssh root@62.238.3.134` Helsinki (2)        -> New Zealand, Denmark*
`ssh root@94.130.150.188` Nuremberg (3)     -> United Kingdom, Netherlands, Finland, South Dakota*
`ssh root@89.167.14.174` Helsinki (3)       -> Ireland, Italy, Belgium, North Dakota*
`ssh root@46.224.188.3` Nuremberg (4)       -> Germany, Sweden, Minnesota*
`ssh root@62.238.8.11` Helsinki (4)         -> Spain, Norway, Iowa*
`ssh root@178.104.201.243` Nuremberg (5)    -> France, Austria

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
scp root@178.104.56.95:/root/stepup-scraping/results/California/leads_bbox_1.csv .

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

`={
leads_bbox_1!A1:Z1;
SORTN({
FILTER(leads_bbox_1!A2:Z;leads_bbox_1!A2:A<>"");
FILTER(leads_bbox_2!A2:Z;leads_bbox_2!A2:A<>"");
FILTER(leads_bbox_3!A2:Z;leads_bbox_3!A2:A<>"");
FILTER(leads_bbox_4!A2:Z;leads_bbox_4!A2:A<>"");
FILTER(leads_bbox_5!A2:Z;leads_bbox_5!A2:A<>"");
FILTER(leads_bbox_6!A2:Z;leads_bbox_6!A2:A<>"");
FILTER(leads_bbox_7!A2:Z;leads_bbox_7!A2:A<>"");
FILTER(leads_bbox_8!A2:Z;leads_bbox_8!A2:A<>"");
FILTER(leads_bbox_9!A2:Z;leads_bbox_9!A2:A<>"");
FILTER(leads_bbox_10!A2:Z;leads_bbox_10!A2:A<>"");
FILTER(leads_bbox_11!A2:Z;leads_bbox_11!A2:A<>"");
FILTER(leads_bbox_12!A2:Z;leads_bbox_12!A2:A<>"");
FILTER(leads_bbox_13!A2:Z;leads_bbox_13!A2:A<>"");
FILTER(leads_bbox_14!A2:Z;leads_bbox_14!A2:A<>"");
FILTER(leads_bbox_15!A2:Z;leads_bbox_15!A2:A<>"");
FILTER(leads_bbox_16!A2:Z;leads_bbox_16!A2:A<>"");
FILTER(leads_bbox_17!A2:Z;leads_bbox_17!A2:A<>"");
FILTER(leads_bbox_18!A2:Z;leads_bbox_18!A2:A<>"");
FILTER(leads_bbox_19!A2:Z;leads_bbox_19!A2:A<>"");
FILTER(leads_bbox_20!A2:Z;leads_bbox_20!A2:A<>"");
FILTER(leads_bbox_21!A2:Z;leads_bbox_21!A2:A<>"");
FILTER(leads_bbox_22!A2:Z;leads_bbox_22!A2:A<>"");
FILTER(leads_bbox_23!A2:Z;leads_bbox_23!A2:A<>"");
FILTER(leads_bbox_24!A2:Z;leads_bbox_24!A2:A<>"");
FILTER(leads_bbox_25!A2:Z;leads_bbox_25!A2:A<>"");
FILTER(leads_bbox_26!A2:Z;leads_bbox_26!A2:A<>"")
};
999999;
2;
4;
VERO
)
}`


# to upload
scp ./results/Italy/consolidated_leads.csv root@178.104.201.243:/root/stepup-scraping/results/consolidated/Italy

docker run -d -v "$(pwd):/app" trainer-scraper --input-csv="results/consolidated/Italy/consolidated_leads.csv" --api-key=""