# Literature Survey — carbonOrbit

**Project:** Real-Time Bus Tracking and ETA Prediction for Sustainable Urban Mobility
**Phase:** 1 synthesis draft for team and guide review
**Evidence scope:** Focused narrative survey based on the team’s source notes; not a systematic review.

## 1. Survey question and method

This survey asks what existing work supports for bus ETA prediction, bus reliability and bunching, passenger response to real-time information, and transport-emissions estimation—and which methods and claims can reasonably be carried into carbonOrbit. Member notes are retained in [`docs/literature/`](literature/) and use the team’s agreed fields: problem, data, method, metrics and result, limitation, project reuse, and examiner question with answer.

This is a focused narrative synthesis of the sources assembled by the four project members, not a systematic search with a registered protocol. Access differed by source: several papers are open in full text, the IEEE ETA review was available through its abstract/record only, and some team notes report an abstract or publication record rather than the complete paper. Claims below are kept within those boundaries. The bibliography and source-identity issues listed in Section 7 require resolution before report freeze.

## 2. Bus arrival-time prediction

ETA research ranges from historical and statistical baselines to machine-learning and sequence models. Liu, Sun, and Wang’s BusTime study compares delay, k-nearest neighbours, kernel regression, additive models, and LSTM on Dublin GPS data. It evaluates accuracy alongside training and prediction cost and finds that model rankings involve practical trade-offs: LSTM is reported as most accurate in their comparison but also computationally expensive, while simpler methods are cheaper. The stop-based representation reduces computational cost relative to distance-based interpolation in that dataset. The result supports comparing models under one common project split; it does not predict which method will win on synthetic BMTC-route data.

Taparia’s Dublin thesis compares regression, ANN, and LSTM for journey time and historical averaging, linear regression, and gradient boosting for adjacent-stop travel time. It provides a useful precedent for keeping a simple historical baseline and a route-segment target in the comparison. Its archived data are from 2012, and one reported XGBoost MAE differs between a table and nearby prose; the exact value should not be repeated without checking the thesis table.

Bhutani, Pachal, and Achar use a GRU encoder–decoder with a bidirectional decoder on one Delhi route, testing multi-step predictions against several spatio-temporal baselines. This shows how forecast horizon and downstream route sections affect model design and evaluation. The model uses previous-bus and previous-week inputs and a more involved data-preparation pipeline; its reported advantages are not expected scores for carbonOrbit. The 2025 IEEE review is relevant for organizing data, route representation, implementation, and evaluation choices, but full-text details require library access.

Ganesh et al. provide an early passenger-information-system prototype linking GPS, server-side prediction, and passenger displays, but the available report describes a demonstration rather than a controlled accuracy or emissions evaluation. Taken together, these studies support a fixed ETA target, common chronological splits, simple baselines, multiple error metrics, and reporting runtime. They do not justify choosing a complex model before testing it.

## 3. Reliability, delays, and bunching

Delay analysis and bunching control are related but distinct. Aemmer et al. analyze GTFS-Realtime delays by network segment and distinguish systematic from stochastic variation. Andres and Nair examine headway prediction together with dynamic holding; this is a control strategy. Rezazada et al. (2022, 2024) and Yang et al. synthesize bunching causes and operational responses. These reviews emphasize that definitions and interventions depend on network, service, and decision context; they do not provide ground-truth labels for the carbonOrbit simulator.

Rawat et al. (2026), the project’s base paper, combines ETA prediction with simulated multi-agent stop-skipping to prevent bunching. It already integrates prediction and operational control, so carbonOrbit should not claim that such integration is novel. Its planned reliability contribution is narrower: generate transparent synthetic events, detect delay and headway-based bunching against simulator labels, and show alerts. Detection does not prevent bunching. Event thresholds must be declared before evaluation and tested for sensitivity rather than described as universal.

## 4. Real-time information and passenger response

Brakewood, Macfarlane, and Watkins analyze New York City route-level ridership during rollout of real-time information, and Tang and Thakuriah study Chicago’s Bus Tracker rollout. Both provide context that information systems can be associated with route-level ridership changes in particular cities. Their estimates are not direct measures of private-car diversion, and results cannot be transferred to Bengaluru without local evidence. A passenger taking the bus after seeing an ETA does not establish which mode that trip replaced.

Therefore, the project’s simulator can evaluate ETA and event-detection metrics, but it cannot establish that better information increases BMTC ridership or causes lower emissions. Any diversion share used in emissions calculations must be an explicit scenario input, reported across a sensitivity range, not an empirical effect attributed to carbonOrbit.

## 5. Emissions and the Indian/Bengaluru context

Ramachandra and Shwetmala provide historical state-wise transport-emissions context; their 2003–04 inventory is not a current BMTC operating factor. ITF’s India passenger-transport life-cycle assessment demonstrates why emissions boundaries matter: vehicle and infrastructure production, energy supply, and vehicle use can all contribute. Its lifecycle factors cannot be mixed with tailpipe-only factors. CSTEP’s national decarbonisation scenarios and TERI’s Delhi transport materials can provide contextual scenario or methodology references after their exact tables, boundaries, and publication metadata are checked. None estimates the causal emissions effect of a BMTC ETA system.

Wills et al. (2019), as listed in the project’s original source plan, concerns GPS-based bus GHG estimation and can inform activity-data methods. However, the current `rahul.v-notes.md` entry labels a different paper by Phadermrod, Crowder, and Wills on importance-performance analysis with a DOI from 2016. That entry is not the same paper and does not support bus emissions or modal-shift claims. It is excluded from this synthesis pending correction. Likewise, carbonOrbit should not infer ambient PM2.5 concentration from tailpipe particulate emissions.

The project’s defensible emissions output is a scenario calculation with explicit bus-service and displaced-trip assumptions, pollutant-specific factors, and uncertainty/sensitivity ranges. It should distinguish fixed-service from marginal additional-service cases and report break-even conditions rather than a single “carbon saved by ETA” claim.

## 6. Synthesis: evidence gap and project fit

Across the literature, ETA prediction, reliability control, passenger-information effects, and emissions accounting use different data and answer different questions. Open research and city-specific studies provide methods and context, but they do not jointly validate a BMTC workflow using the project’s planned data. The practical gap for this student project is an auditable, reproducible integration of those evaluation steps for selected BMTC route geometry, with simulated data clearly labelled and claims kept within the data boundary.

The survey therefore supports four design choices:

1. Compare ETA models against historical and lightweight baselines on contiguous held-out days.
2. Keep ground-truth event labels separate from model features and evaluate detection separately from control.
3. Treat external-city ridership findings as context, not Bengaluru mode-shift estimates.
4. Present emissions as transparent scenarios, with consistent boundaries and no ambient air-quality claim.

## 7. Source-quality and citation audit before freeze

- **Rawat et al. (2026):** publisher abstract reviewed; verify detailed claims from the final formatted paper when available.
- **Kumar et al. (2025), IEEE ETA review:** full text is not confirmed as read; use abstract-level claims until institutional access is obtained.
- **Taparia thesis:** the full TCD repository thesis is available; resolve the table/prose MAE discrepancy before quoting an exact adjacent-stop XGBoost value.
- **Rakhimzhanov and Mansurova (2025):** the current notes cite DOI `10.1109/ICCIKE67021.2025.11318207`, while the project’s earlier source list identifies a different 2025 Mansurova dataset paper. Confirm title, authors, venue, and DOI against a publisher record before citing the conference result. Do not conflate the travel-time paper with the Astana GTFS dataset.
- **Wills et al. (2019):** replace the mismatched Phadermrod et al. citation in the emissions notes with the actual GPS-based bus-emissions paper only after metadata are checked; exclude the current importance-performance-analysis claims from this survey.
- **TERI and CSTEP:** verify the exact report edition, authorship, table, units, and operational/lifecycle boundary before importing numerical values.
- **All sources:** final bibliography must contain the version actually read, DOI or stable publisher/repository link, access date, and any access limitation.

## 8. Member-note index

- [R. Dhrutvan — ETA and base-paper notes](literature/notes_dhrutvan.md)
- [Naga Sai — bunching and delay notes](literature/notes_naga-sai.md)
- [Rahul A.M. — passenger information, ETA, delay, and ridership notes](literature/notes_rahul_am.md)
- [Rahul Velpuri — emissions and modal-shift notes](literature/rahul.v-notes.md)

## Selected references

- Rawat, S. et al. (2026). “Real-Time Bus Arrival Prediction and Bus Bunching Prevention Using a Multi-Agent LSTM Approach.” [Frontiers publisher abstract](https://www.frontiersin.org/journals/built-environment/articles/10.3389/fbuil.2026.1894212/abstract).
- Liu, D., Sun, J., & Wang, S. (2020). “BusTime: Which is the Right Prediction Model for My Bus Arrival Time?” [arXiv:2003.10373](https://arxiv.org/abs/2003.10373).
- Taparia, A. (2020). *Bus Journey and Arrival Time Prediction based on Archived AVL/GPS data using Machine Learning.* [TCD full thesis](https://publications.scss.tcd.ie/theses/diss/2020/TCD-SCSS-DISSERTATION-2020-078.pdf).
- Bhutani, N., Pachal, S., & Achar, A. (2022; v2 2024). “Public Transit Arrival Prediction: a Seq2Seq RNN Approach.” [arXiv:2210.01655](https://arxiv.org/abs/2210.01655).
- Kumar, B. A. et al. (2025). “Bus Arrival Time Prediction: A Comprehensive Review.” *IEEE Transactions on Intelligent Transportation Systems*, 26(6), 7362–7379. [DOI](https://doi.org/10.1109/TITS.2025.3545695). Full text requires access confirmation.
- Brakewood, C., Macfarlane, G. S., & Watkins, K. (2015). “The Impact of Real-Time Information on Bus Ridership in New York City.” [DOI](https://doi.org/10.1016/j.trc.2015.01.021).
- Tang, L., & Thakuriah, P. (2012). “Ridership Effects of Real-Time Bus Information System: A Case Study in the City of Chicago.” [DOI](https://doi.org/10.1016/j.trc.2012.01.001).
- International Transport Forum (2023). *Life-cycle Assessment of Passenger Transport: An Indian Case Study.* [Official ITF report page](https://www.itf-oecd.org/life-cycle-assessment-passenger-transport-indian-case-study).
- Wills, J. M. et al. (2019). “A Simple Sinuosity-Based Method using GPS Data to Support Mitigation Policies for Public Buses GHG Emissions.” [arXiv:1907.09335](https://arxiv.org/abs/1907.09335). Verify full metadata before final reference freeze.
