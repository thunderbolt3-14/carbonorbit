# Literature Notes — Rahul A.M.

**Project:** carbonOrbit  
**Assigned topic:** Bus arrival prediction, transit delays, and real-time information

## 1. Ganesh et al. (2012) — Real-Time Passenger Information System

**Citation:** Ganesh, K., Thrivikraman, M., Kuri, J., Dagale, H., Sudhakar, G., & Sanyal, S. (2012). “Implementation of a Real Time Passenger Information System.” *International Journal of Engineering Science and Management*, 2(2). [arXiv version](https://arxiv.org/abs/1206.0447)

- **Problem:** Bus passengers need current bus-location and arrival-time information; operators need tools to monitor their fleet.
- **Data:** GPS positions sent periodically from vehicle units to a server. The prototype was demonstrated on a campus using cars and two-wheelers to emulate buses.
- **Method:** A passenger-information system with vehicle units, a server-side ETA algorithm, and passenger displays or announcements at stops.
- **Metrics and key result:** The authors demonstrated a working prototype showing bus locations and predicted arrivals. The paper abstract does not report a numerical ETA error.
- **Limitation or gap:** The demonstration used a campus setting and vehicles emulating buses; it does not report a numerical accuracy evaluation on an urban bus network.
- **What carbonOrbit can reuse:** The basic GPS-to-server-to-ETA-to-passenger-display architecture. Our project can add quantitative evaluation and clearly label its GPS data as simulated.
- **Examiner question and answer:** **Was this tested on a live city bus fleet?** The reported prototype was demonstrated on a campus using vehicles to emulate buses.

## 2. Rakhimzhanov and Mansurova (2025) — Prediction with Limited Data

**Citation:** Rakhimzhanov, D., & Mansurova, A. (2025). “Bus Travel Time Prediction Under Data Constraints: A Lightweight Deep Learning Approach.” *Proceedings of the 2025 International Conference on Computational Intelligence and Knowledge Economy*, pp. 444–449. [https://doi.org/10.1109/ICCIKE67021.2025.11318207](https://doi.org/10.1109/ICCIKE67021.2025.11318207). This conference paper is distinct from Mansurova et al.'s open Astana GPS-to-GTFS dataset paper listed below.

- **Problem:** Predicting bus travel times when external information such as weather or traffic feeds is unavailable.
- **Data:** Real bus routes in Kandy, Sri Lanka, and Astana, Kazakhstan.
- **Method:** A hybrid bidirectional LSTM model using historical transit data without external contextual inputs.
- **Metrics and key result:** The paper reports MAE of 5.44 seconds and MAPE of 2.41% on one Kandy route. For three Astana routes, it reports MAE values of 42.16–50.45 seconds and MAPE values of 34.23–39.84%; the model outperformed its comparison methods in those experiments.
- **Limitation or gap:** Results from these real routes may not transfer to Bengaluru or to our simulated data.
- **What carbonOrbit can reuse:** Compare ETA methods using the same held-out time periods and report clear error metrics such as MAE and MAPE. Treat the paper’s results as context rather than a performance target.
- **Examiner question and answer:** **Can we compare our MAE directly with theirs?** Not without accounting for differences in cities, data, prediction targets, and evaluation setup.

## 3. Aemmer et al. (2022) — Measuring and Classifying Transit Delays

**Citation:** Aemmer, Z., Ranjbari, A., & MacKenzie, D. (2022). “Measurement and Classification of Transit Delays Using GTFS-RT Data.” *Public Transport*, 14(2), 263–285. [https://doi.org/10.1007/s12469-022-00291-7](https://doi.org/10.1007/s12469-022-00291-7)

- **Problem:** Transit agencies need to identify where delays occur and distinguish predictable delays from random variation.
- **Data:** One year of GTFS-Realtime data from the King County Metro bus network in Seattle, Washington.
- **Method:** The authors calculated transit-performance measures from GTFS-Realtime and grouped them by road segment. They analyzed systematic and stochastic delay patterns.
- **Metrics and key result:** Delay measures were assigned to network segments. The authors found opportunities for stochastic speedups on some segments and suggested that the network might have excessive schedule padding overall. The abstract does not provide a single model-accuracy score.
- **Limitation or gap:** The method depends on GTFS-Realtime vehicle data. Our project uses simulated pings, so we need known synthetic delay labels to evaluate detection.
- **What carbonOrbit can reuse:** Analyze delay by route segment and keep ground-truth event labels separate from model inputs.
- **Examiner question and answer:** **Why separate systematic and stochastic delays?** Recurring delays may call for schedule or infrastructure changes, while random variation is less predictable.

## 4. Brakewood et al. (2015) — Real-Time Information and New York Bus Ridership

**Citation:** Brakewood, C., Macfarlane, G. S., & Watkins, K. (2015). “The Impact of Real-Time Information on Bus Ridership in New York City.” *Transportation Research Part C: Emerging Technologies*, 53, 59–75. [https://doi.org/10.1016/j.trc.2015.01.021](https://doi.org/10.1016/j.trc.2015.01.021)

- **Problem:** Whether access to real-time bus information is associated with changes in bus ridership.
- **Data:** Monthly route-level bus-ridership data in New York City during the rollout of its real-time information system, along with service and other contextual data.
- **Method:** Fixed-effects analysis of route-level ridership, controlling for factors including service, fares, weather, and local conditions.
- **Metrics and key result:** The study estimated about 118 additional weekday trips per route on average, a median increase of about 1.7% in route-level weekday ridership. The largest routes saw a larger estimated increase.
- **Limitation or gap:** This is evidence from New York City, not Bengaluru. It does not show that our prototype will increase BMTC ridership or reduce emissions.
- **What carbonOrbit can reuse:** Use the paper to explain why reliable arrival information may matter. Describe our own ridership and emissions outcomes as scenario estimates unless we collect real-world evidence.
- **Examiner question and answer:** **Does carbonOrbit prove real-time information increases BMTC ridership?** No. Our prototype evaluates simulated bus data; it does not measure passenger behavior.

## 5. Tang and Thakuriah (2012) — Chicago Real-Time Bus Information

**Citation:** Tang, L., & Thakuriah, P. (2012). “Ridership Effects of Real-Time Bus Information System: A Case Study in the City of Chicago.” *Transportation Research Part C: Emerging Technologies*, 22, 146–161. [https://doi.org/10.1016/j.trc.2012.01.001](https://doi.org/10.1016/j.trc.2012.01.001)

- **Problem:** Whether Chicago’s real-time bus-information system was associated with changes in ridership across the bus network.
- **Data:** Monthly average weekday ridership for 144 Chicago Transit Authority bus routes from 2002 to 2010, along with service, fare, weather, economic, and local-area data.
- **Method:** A quasi-experimental analysis of the phased Bus Tracker rollout using a linear mixed-effects model with statistical controls.
- **Metrics and key result:** The model estimated about 126 additional weekday riders per route when Bus Tracker information was provided; the result was statistically significant at the 0.05 level. The average gain was described as modest and varied by route.
- **Limitation or gap:** The study measures ridership effects in Chicago; it does not evaluate our ETA model or establish outcomes for Bengaluru. The authors note limits in separating the effects of different ways users received the information.
- **What carbonOrbit can reuse:** Use it as context for evaluating the broader value of real-time information, while avoiding claims that the same ridership effect will occur in our project.
- **Examiner question and answer:** **Why include both the Chicago and New York studies?** They examine different cities and rollouts, offering context, but neither directly validates our simulator or predicts BMTC outcomes.

## 6. Mansurova et al. (2025) — Astana GPS-to-GTFS Dataset

**Citation:** Mansurova, A., Mussina, A., Aubakirov, S., Nugumanova, A., & Yedilkhan, D. (2025). “From Raw GPS to GTFS: A Real-World Open Dataset for Bus Travel Time Prediction.” *Data*, 10(8), 119. [https://doi.org/10.3390/data10080119](https://doi.org/10.3390/data10080119). Associated dataset: [Zenodo record 15769359](https://doi.org/10.5281/zenodo.15769359).

- **Problem:** Public-transport prediction research needs accessible operational data and a reproducible path from raw vehicle GPS to timetable-compatible records.
- **Data:** GPS trajectories from three high-frequency bus routes in Astana, Kazakhstan, collected July–September 2024 and published with processed GTFS-related data.
- **Method:** The authors describe processing raw trajectories into a documented dataset intended for bus travel-time prediction; consult the full article and repository documentation before reproducing exact processing steps.
- **Metrics and key result:** This is a data descriptor, not a model leaderboard. Its main contribution is an openly documented real-world dataset and processing resource; do not attribute model accuracy results to it.
- **Limitation or gap:** The network and operating conditions are Astana-specific. It does not validate a Bengaluru model and must not be conflated with the separately cited ICCIKE 2025 prediction paper.
- **What carbonOrbit can reuse:** Use its data-documentation and raw-GPS-to-structured-transit workflow as a reproducibility reference. The team may consider the dataset only as an external comparison after reviewing access, licence, and scope; it is not a substitute for BMTC route geometry.
- **Examiner question and answer:** **Does this paper show that a model will work on BMTC?** No. It provides an Astana dataset and data-processing resource; BMTC performance needs separate evaluation.

## Overall takeaway

These papers cover system design, travel-time prediction, delay analysis, and the possible passenger effects of real-time information. Their results come from different cities and data types. carbonOrbit should evaluate its own simulated data, report its own metrics, and describe ridership or emissions impacts as estimates rather than measured outcomes.

## References and access

- Ganesh et al. (2012): [arXiv paper](https://arxiv.org/abs/1206.0447)
- Rakhimzhanov and Mansurova (2025): [conference paper DOI](https://doi.org/10.1109/ICCIKE67021.2025.11318207)
- Mansurova et al. (2025): [Data article](https://doi.org/10.3390/data10080119); [associated Zenodo dataset](https://doi.org/10.5281/zenodo.15769359)
- Aemmer et al. (2022): [Penn State publication record and DOI](https://pure.psu.edu/en/publications/measurement-and-classification-of-transit-delays-using-gtfs-rt-da/)
- Brakewood et al. (2015): [paper DOI](https://doi.org/10.1016/j.trc.2015.01.021)
- Tang and Thakuriah (2012): [paper DOI](https://doi.org/10.1016/j.trc.2012.01.001)
