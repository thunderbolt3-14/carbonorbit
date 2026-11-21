# Literature Survey — carbonOrbit

**Project:** Real-Time Bus Tracking and ETA Prediction for Sustainable Urban Mobility
**Phase:** 1 synthesis draft for team and guide review
**Evidence scope:** Focused narrative survey based on the team’s source notes; not a systematic review.

## 1. Survey question and method

This survey asks what existing work supports for bus ETA prediction, bus reliability and bunching, passenger response to real-time information, and transport-emissions estimation—and which methods and claims can reasonably be carried into carbonOrbit. Member notes are retained in [`docs/literature/`](literature/) and use the team’s agreed fields: problem, data, method, metrics and result, limitation, project reuse, and examiner question with answer.

This is a focused narrative synthesis of the sources assembled by the four project members, not a systematic search with a registered protocol. Access differed by source: several papers are open in full text, the IEEE ETA review was available through its abstract/record only, and some team notes report an abstract or publication record rather than the complete paper. Claims below are kept within those boundaries. The bibliography and source-identity issues listed in Section 7 require resolution before report freeze.

## 2. Bus arrival-time prediction

ETA research ranges from historical and statistical baselines to machine-learning and sequence models. Liu, Sun, and Wang’s BusTime study compares delay, k-nearest neighbours, kernel regression, additive models, and LSTM on Dublin GPS data. It evaluates accuracy alongside training and prediction cost and finds that model rankings involve practical trade-offs: LSTM is reported as most accurate in their comparison but also computationally expensive, while simpler methods are cheaper. The stop-based representation reduces computational cost relative to distance-based interpolation in that dataset. The result supports comparing models under one common project split; it does not predict which method will win on synthetic BMTC-route data.

Taparia’s Dublin thesis compares regression, ANN, and LSTM for journey time and historical averaging, linear regression, and gradient boosting for adjacent-stop travel time. It provides a useful precedent for keeping a simple historical baseline and a route-segment target in the comparison. Its archived data are from 2012. In the full thesis, Table 8.2 gives XGBoost MAE of 0.80 minutes and linear-regression MAE of 0.93, while nearby prose gives 0.84 and 0.90 respectively; the table values are cited with this inconsistency noted.

Bhutani, Pachal, and Achar use a GRU encoder–decoder with a bidirectional decoder on one Delhi route, testing multi-step predictions against several spatio-temporal baselines. This shows how forecast horizon and downstream route sections affect model design and evaluation. The model uses previous-bus and previous-week inputs and a more involved data-preparation pipeline; its reported advantages are not expected scores for carbonOrbit. The 2025 IEEE review is relevant for organizing data, route representation, implementation, and evaluation choices, but full-text details require library access.

Rakhimzhanov and Mansurova’s ICCIKE 2025 paper studies a data-limited BiLSTM approach and reports results on Kandy and Astana routes. It is distinct from Mansurova et al.’s 2025 *Data* article, which describes a three-route Astana GPS-to-GTFS dataset rather than an ETA-model benchmark. Both are useful prediction-method and data-documentation precedents, but neither establishes BMTC performance; detailed conference-paper claims need full-text verification. Ganesh et al. provide an early passenger-information-system prototype linking GPS, server-side prediction, and passenger displays, but the available report describes a demonstration rather than a controlled accuracy or emissions evaluation. Taken together, these studies support a fixed ETA target, common chronological splits, simple baselines, multiple error metrics, and reporting runtime. They do not justify choosing a complex model before testing it.

Amogha et al. (2026) is a particularly close comparator: its Springer abstract describes two XGBoost models using real Indian GPS and bus-operational data, one for bus-delay prediction and one for per-trip CO2 estimation. The abstract reports 49-second MAE and R² 0.9533 for delay, and 1.903 kg/trip MAE and R² 0.99615 for emissions. This means carbonOrbit should not claim that connecting bus-delay prediction and CO2 estimation is itself novel. The chapter is paywalled, so these are abstract-level results only; the full data definition, emission boundary, and validation protocol remain to be checked before detailed comparison.

## 3. Reliability, delays, and bunching

Delay analysis and bunching control are related but distinct. Aemmer et al. analyze GTFS-Realtime delays by network segment and distinguish systematic from stochastic variation. Andres and Nair combine data-driven headway prediction with dynamic holding, so their work evaluates control as well as prediction. Rezazada et al.’s 2022 ATRF review, its expanded 2024 *Transport Reviews* paper, and Yang et al.’s 2024 review synthesize causes and operational responses. They identify context-specific trade-offs and gaps in realistic, passenger-focused evaluation. These works inform definitions and scope; they do not provide ground-truth labels for the carbonOrbit simulator.

Rawat et al. (2026), the project’s base paper, combines ETA prediction with simulated multi-agent stop-skipping to prevent bunching. It already integrates prediction and operational control, so carbonOrbit should not claim that such integration is novel. Its planned reliability contribution is narrower: generate transparent synthetic events, detect delay and headway-based bunching against simulator labels, and show alerts. Detection does not prevent bunching. Event thresholds must be declared before evaluation and tested for sensitivity rather than described as universal.

## 4. Real-time information and passenger response

Brakewood, Macfarlane, and Watkins analyze New York City route-level ridership during rollout of real-time information, and Tang and Thakuriah study Chicago’s Bus Tracker rollout. Tampa’s 2014 before-after control-group study found improvements in reported waiting experience and related perceptions; it was not evidence of a significant ridership increase. Brakewood and Watkins’ 2019 review summarizes passenger benefits and flags gaps in measuring actual path-choice behavior and post-implementation cost-benefit. These findings complement the city-specific ridership studies but do not measure private-car diversion or transfer directly to Bengaluru. A passenger taking the bus after seeing an ETA does not establish which mode that trip replaced.

Therefore, the project’s simulator can evaluate ETA and event-detection metrics, but it cannot establish that better information increases BMTC ridership or causes lower emissions. Any diversion share used in emissions calculations must be an explicit scenario input, reported across a sensitivity range, not an empirical effect attributed to carbonOrbit.

## 5. Emissions and the Indian/Bengaluru context

Ramachandra and Shwetmala provide historical state-wise transport-emissions context; their 2003–04 inventory is not a current BMTC operating factor. ITF’s India passenger-transport life-cycle assessment demonstrates why emissions boundaries matter: vehicle and infrastructure production, energy supply, and vehicle use can all contribute. Its lifecycle factors cannot be mixed with tailpipe-only factors. CSTEP’s national scenarios compare a modeled 30% passenger-kilometre shift to public transport (24% lower CO2 than BAU) with a 30% EV shift (11% lower under the report’s grid assumptions); these are scenario results, not evidence that ETA information causes mode shift. TERI’s Delhi report estimates bus intensity at 29.48 and private-car intensity at 87.73 g CO2/pkm under Delhi assumptions. Its 32.38 g/pkm saving compares a weighted Delhi road-mode average with Delhi Metro Method 2, not a private-car-to-bus trip. Neither report provides carbonOrbit factors or a causal emissions estimate.

Wills et al. (2019), as listed in the project’s original source plan, concerns GPS-based bus GHG estimation and can inform activity-data methods. The member note has been corrected to the arXiv preprint and its actual topic; it does not support passenger mode-shift claims. Likewise, carbonOrbit should not infer ambient PM2.5 concentration from tailpipe particulate emissions.

The project’s defensible emissions output is a scenario calculation with explicit bus-service and displaced-trip assumptions, pollutant-specific factors, and uncertainty/sensitivity ranges. It should distinguish fixed-service from marginal additional-service cases and report break-even conditions rather than a single “carbon saved by ETA” claim.

## 6. Synthesis: evidence gap and project fit

Across the literature, ETA prediction, reliability control, passenger-information effects, and emissions accounting use different data and answer different questions. Open research and city-specific studies provide methods and context, but they do not jointly validate a BMTC workflow using the project’s planned data. The practical gap for this student project is an auditable, reproducible integration of those evaluation steps for selected BMTC route geometry, with simulated data clearly labelled and claims kept within the data boundary.

The survey therefore supports four design choices:

1. Compare ETA models against historical and lightweight baselines on contiguous held-out days.
2. Keep ground-truth event labels separate from model features and evaluate detection separately from control.
3. Treat external-city ridership findings as context, not Bengaluru mode-shift estimates.
4. Present emissions as transparent scenarios, with consistent boundaries and no ambient air-quality claim.

## 7. Source-quality and citation audit before freeze

- **Rawat et al. (2026):** full article checked at the publisher. Report values with their NYC dataset and simulated-control boundaries; note the limitations described by the authors.
- **Kumar et al. (2025), IEEE ETA review:** full text is not confirmed as read; use abstract-level claims until institutional access is obtained.
- **Taparia thesis:** full TCD thesis checked. Table/prose discrepancies confirmed: XGBoost MAE 0.80 vs 0.84 minutes and linear-regression MAE 0.93 vs 0.90 minutes.
- **Rakhimzhanov and Mansurova (2025):** the ICCIKE DOI identifies “Bus Travel Time Prediction Under Data Constraints: A Lightweight Deep Learning Approach,” a separate prediction paper reporting Kandy and Astana results. The project’s earlier source list also includes Mansurova et al.’s distinct Astana GPS-to-GTFS dataset paper, *Data* 10(8), 119, DOI `10.3390/data10080119`, and its Zenodo data DOI `10.5281/zenodo.15769359`. Both now have separate entries in Rahul A.M.’s notes. Verify detailed model results against the full conference paper before quoting them.
- **Amogha et al. (2026):** Springer’s chapter abstract reports XGBoost delay prediction and CO2-per-trip estimation on real Indian bus data. The full chapter is paywalled; treat the performance numbers as abstract-only and compare its scope before making contribution claims.
- **Wills et al. (2019):** the emissions note now cites the GPS-based bus GHG estimation preprint at arXiv:1907.09335 (DOI `10.48550/arXiv.1907.09335`); it is not a passenger-preference or modal-shift study.
- **TERI and CSTEP:** the cited primary PDFs were checked. CSTEP's modal-shift and EV-shift percentages are national 2017–18 scenarios; TERI's 32.38 g/pkm comparison is Metro Method 2 versus a weighted Delhi road-mode average. Do not label either result as a BMTC effect or reuse them as project emission factors.
- **All sources:** final bibliography must contain the version actually read, DOI or stable publisher/repository link, access date, and any access limitation.

## 8. Member-note index

The individual paper notes use the shared Phase 1 citation template: **Problem; Data; Method; Metrics and key result; Limitation or gap; What carbonOrbit reuses; Questions an examiner could ask, with our answer.** Where a source is available only as an abstract, the notes identify that limit and avoid presenting abstract-level information as full-text findings.

- [R. Dhrutvan — ETA and base-paper notes](literature/notes_dhrutvan.md)
- [Naga Sai — bunching and delay notes](literature/notes_naga-sai.md)
- [Rahul A.M. — passenger information, ETA, delay, and ridership notes](literature/notes_rahul_am.md)
- [Rahul Velpuri — emissions and modal-shift notes](literature/rahul.v-notes.md)

## Selected references

- Rawat, S. et al. (2026). “Real-Time Bus Arrival Prediction and Bus Bunching Prevention Using a Multi-Agent LSTM Approach.” *Frontiers in Built Environment*, 12, published 22 September 2026. [Full publisher article](https://www.frontiersin.org/journals/built-environment/articles/10.3389/fbuil.2026.1894212/full). DOI: 10.3389/fbuil.2026.1894212.
- Ganesh, K. et al. (2012). “Implementation of a Real Time Passenger Information System.” *International Journal of Engineering Science and Management*, 2(2). [arXiv:1206.0447](https://arxiv.org/abs/1206.0447).
- Liu, D., Sun, J., & Wang, S. (2020). “BusTime: Which is the Right Prediction Model for My Bus Arrival Time?” [arXiv:2003.10373](https://arxiv.org/abs/2003.10373).
- Taparia, A. (2020). *Bus Journey and Arrival Time Prediction based on Archived AVL/GPS data using Machine Learning.* [TCD full thesis](https://publications.scss.tcd.ie/theses/diss/2020/TCD-SCSS-DISSERTATION-2020-078.pdf).
- Bhutani, N., Pachal, S., & Achar, A. (2022; v2 2024). “Public Transit Arrival Prediction: a Seq2Seq RNN Approach.” [arXiv:2210.01655](https://arxiv.org/abs/2210.01655).
- Kumar, B. Anil, Singh, R., Shaji, H. E., & Vanajakshi, L. (2025). “Bus Arrival Time Prediction: A Comprehensive Review.” *IEEE Transactions on Intelligent Transportation Systems*, 26(6), 7362–7379. [DOI](https://doi.org/10.1109/TITS.2025.3545695). Bibliographic metadata verified; full text not reviewed, so use abstract-level claims only.
- Brakewood, C., Macfarlane, G. S., & Watkins, K. (2015). “The Impact of Real-Time Information on Bus Ridership in New York City.” [DOI](https://doi.org/10.1016/j.trc.2015.01.021).
- Brakewood, C., Barbeau, S., & Watkins, K. (2014). “An Experiment Evaluating the Impacts of Real-Time Transit Information on Bus Riders in Tampa, Florida.” *Transportation Research Part A: Policy and Practice*, 69, 409–422. [DOI](https://doi.org/10.1016/j.tra.2014.09.003).
- Brakewood, C., & Watkins, K. (2019). “A Literature Review of the Passenger Benefits of Real-Time Transit Information.” *Transport Reviews*, 39(3), 327–356. [DOI](https://doi.org/10.1080/01441647.2018.1472147).
- Tang, L., & Thakuriah, P. (2012). “Ridership Effects of Real-Time Bus Information System: A Case Study in the City of Chicago.” [DOI](https://doi.org/10.1016/j.trc.2012.01.001).
- Andres, M., & Nair, R. (2017). “A Predictive-Control Framework to Address Bus Bunching.” *Transportation Research Part B: Methodological*, 104, 123–148. [DOI](https://doi.org/10.1016/j.trb.2017.06.013).
- Rezazada, M., Nassir, N., & Tanin, E. (2022). “Public transport bunching: A critical review with focus on methods and findings for implications for policy and future research.” *Australasian Transport Research Forum 2022 Proceedings*, Adelaide, 28–30 September. [Proceedings PDF](https://australasiantransportresearchforum.org.au/wp-content/uploads/2022/05/ATRF2022_Resubmission_77.pdf).
- Rezazada, M., Nassir, N., Tanin, E., & Ceder, A. (2024). “Bus Bunching: A Comprehensive Review from Demand, Supply, and Decision-Making Perspectives.” *Transport Reviews*, 44(4), 766–790. [DOI](https://doi.org/10.1080/01441647.2024.2313969).
- Yang, Y., Cheng, J., & Liu, Y. (2024). “An Overview of Solutions to the Bus Bunching Problem in Urban Bus Systems.” *Frontiers of Engineering Management*, 11, 661–675. [DOI](https://doi.org/10.1007/s42524-024-0297-1).
- Rakhimzhanov, D., & Mansurova, A. (2025). “Bus Travel Time Prediction Under Data Constraints: A Lightweight Deep Learning Approach.” *Proceedings of ICCIKE 2025*, 444–449. [DOI](https://doi.org/10.1109/ICCIKE67021.2025.11318207). Detailed metrics need full-text verification.
- Amogha, B. V., Bairy, P. R., Selvam, S., & Joy, J. D. (2026). “Machine Learning-Based Prediction of Bus Delay and CO2 Emission Estimation Using XGBoost.” In *Data Science and Applications (ICDSA 2025)*, *Lecture Notes in Networks and Systems*, vol. 1795, pp. 216–227. [Springer DOI](https://doi.org/10.1007/978-3-032-15404-0_19). Full chapter is paywalled; claims above use the publisher abstract only.
- International Transport Forum (2023). *Life-cycle Assessment of Passenger Transport: An Indian Case Study.* [Official ITF report page](https://www.itf-oecd.org/life-cycle-assessment-passenger-transport-indian-case-study).
- Wills, W. et al. (2019). “A Simple Sinuosity-Based Method using GPS Data to Support Mitigation Policies for Public Buses GHG Emissions.” [arXiv:1907.09335](https://arxiv.org/abs/1907.09335). Preprint; verify any later publication status before final reference freeze.
- Mansurova, A., Mussina, A., Aubakirov, S., Nugumanova, A., & Yedilkhan, D. (2025). “From Raw GPS to GTFS: A Real-World Open Dataset for Bus Travel Time Prediction.” *Data*, 10(8), 119. [DOI](https://doi.org/10.3390/data10080119); [dataset](https://doi.org/10.5281/zenodo.15769359).
- The Energy and Resources Institute (n.d.). “Emission Saving Made by a Passenger by Choosing to Travel by Delhi Metro.” [Report PDF](https://www.teriin.org/sites/default/transport/Per_passenger_emission_in_Delhi_Different_Modes.pdf). Publication year is not stated in the PDF; source inputs include 2019–20 public-transport data.
- Aemmer, Z., Ranjbari, A., & MacKenzie, D. (2022). “Measurement and Classification of Transit Delays Using GTFS-RT Data.” *Public Transport*, 14(2), 263–285. [DOI](https://doi.org/10.1007/s12469-022-00291-7).
- Ramachandra, T. V., & Shwetmala (2009). “Emissions from India's transport sector: Statewise synthesis.” *Atmospheric Environment*, 43(34), 5510–5517. [DOI](https://doi.org/10.1016/j.atmosenv.2009.07.015).
- Ananthakumar, M. R., & Paladugula, A. L. (2017). *Impact of Decarbonisation Strategies on Road Transport Sector Emissions.* GHG Platform India, Phase II. [Report PDF](https://ghgplatform-india.org/wp-content/uploads/publications/phase-2/GHGPI-PhaseII-Decarbonisation%20Impact%20on%20Road%20Transport%20Sector%20Emissions-Oct17.pdf).
