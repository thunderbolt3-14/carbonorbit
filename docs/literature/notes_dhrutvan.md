# ETA Prediction Literature Notes — R. Dhrutvan

These notes cover the five ETA and base-paper sources assigned to Member A for Phase 1. They follow the agreed literature-survey template. Results are reported only to the level supported by the source text reviewed.

## 1. Rawat et al. (2026), base paper

**Citation:** Seema Rawat, Alyona Abaidullina, Dilnaz Alimbayeva, Deepak Kumar, and Praveen Kumar, “Real-Time Bus Arrival Prediction and Bus Bunching Prevention Using a Multi-Agent LSTM Approach,” *Frontiers in Built Environment*, vol. 12, 2026. [https://doi.org/10.3389/fbuil.2026.1894212](https://doi.org/10.3389/fbuil.2026.1894212)  
**Read:** Publisher abstract reviewed on 18 November 2026. The page says the final formatted version will be published soon; detailed claims below are therefore limited to the abstract.

- **Problem:** Improve bus arrival-time prediction with sparse, infrequent real-time telemetry and use predictions to respond proactively to bus bunching.
- **Data:** Metropolitan Transportation Authority (MTA) SIRI real-time data for New York City’s 20 highest-frequency routes. The operational-control simulation focuses on routes B82 and Bx9.
- **Method:** A Long Short-Term Memory (LSTM) model with route embeddings predicts arrival times. A “forward-looking” target-imputation approach addresses sparse observations. The predicted ETAs feed a multi-agent simulation in which buses coordinate decentralized stop-skipping (“Express” mode).
- **Metrics and key result:** The abstract reports overall ETA mean absolute error (MAE) of 2.02 minutes, 28.5% lower than historical baselines. In 120-step simulations, zero headway gaps did not occur; Express mode was triggered in 19.2% of steps on B82 and 25.8% on Bx9, with headways recovering above the paper’s safe threshold after interventions.
- **Limitation or gap:** The evaluation uses New York City feeds and simulated bus-control interventions; it does not establish performance on BMTC routes or measure passenger response, mode shift, fuel use, or emissions. Since the full formatted text was not available on the publisher page when reviewed, these findings are abstract-level.
- **What carbonOrbit reuses:** Treat this as the closest base-paper comparator. Compare data frequency, ETA target, baselines, temporal validation, and metrics. Frame CarbonOrbit’s extension narrowly as a BMTC-route simulation and transparent emissions-scenario layer; do not claim to be the first project to integrate ETA and bunching analysis.
- **Questions an examiner could ask, with our answer:** **Does Rawat et al. already combine ETA prediction and bunching prevention?** Yes. CarbonOrbit’s contribution is a BMTC-focused simulation and separate scenario-based emissions analysis, not the first integration of ETA and reliability methods. **Does their simulated reduction prove real passenger or emissions benefits?** No; it demonstrates outcomes in the modeled control scenario, not observed passenger or environmental effects.

## 2. Liu, Sun, and Wang (2020), BusTime

**Citation:** Dairui Liu, Jingxiang Sun, and Shen Wang, “BusTime: Which is the Right Prediction Model for My Bus Arrival Time?,” arXiv:2003.10373, 2020. [https://arxiv.org/abs/2003.10373](https://arxiv.org/abs/2003.10373)  
**Read:** Full arXiv HTML paper reviewed on 18 November 2026.

- **Problem:** Help practitioners choose ETA models by comparing prediction quality alongside the training and prediction costs that affect real deployment.
- **Data:** Raw Dublin bus GPS records from November 2012 and January 2013. The detailed experiment uses route 46A, with up to 4,311 trips, and compares stop-based with distance-based trip representations.
- **Method:** The authors clean and segment GPS trajectories using schedule information, then compare delay, k-nearest neighbours (k-NN), kernel regression (KR), additive models, and LSTM. A KD-tree selects GPS observations nearest to each stop, reducing the number of input points.
- **Metrics and key result:** Evaluation covers MAE, root mean squared error (RMSE), mean absolute percentage error (MAPE), training time, and prediction time. The authors rank LSTM highest for accuracy and kernel regression next, while delay is least computationally expensive. Stop-based interpolation cuts computation by up to about five times without a large accuracy loss; LSTM has the highest training cost and needs substantial data and specialist tuning.
- **Limitation or gap:** The detailed study is centered on one Dublin route and historical feed conditions, so its rankings are not guaranteed for BMTC or for CarbonOrbit’s simulated data. Model trade-offs depend on dataset scale, preprocessing, and hardware.
- **What carbonOrbit reuses:** Use its model-comparison framing: compare simple baselines and more complex models on the same held-out days, report both error and runtime, and justify added model complexity with measured gains.
- **Questions an examiner could ask, with our answer:** **Why not select LSTM because BusTime ranked it most accurate?** Its accuracy came with high training cost and data needs. CarbonOrbit should select from a pre-specified ladder using its own validation results and a stated simplicity rule. **Can we reuse the Dublin model ranking directly?** No; it is evidence about that study’s data and implementation, not a BMTC result.

## 3. Taparia (2020), Trinity College Dublin MSc thesis

**Citation:** Ankit Taparia, *Bus Journey and Arrival Time Prediction based on Archived AVL/GPS Data using Machine Learning*, MSc dissertation, University of Dublin, Trinity College, 2020. [Full thesis](https://publications.scss.tcd.ie/theses/diss/2020/TCD-SCSS-DISSERTATION-2020-078.pdf) · [Abstract](https://publications.scss.tcd.ie/theses/diss/2020/TCD-SCSS-DISSERTATION-2020-078-ABSTRACT.pdf)  
**Read:** Full thesis and abstract reviewed on 18 November 2026. The full thesis PDF is available from the TCD repository.

- **Problem:** Predict both complete bus-journey times and stop-level arrival times from archived AVL/GPS observations and route/stop information.
- **Data:** Historical Dublin Bus AVL/GPS observations from November 6–30, 2012, joined with Dublin GTFS stop information. The journey-time analysis includes routes 40, 46, and 145; the stop-segment experiment uses route 46 and 459 trips across 20 frequent stops, with 369 training and 90 test trips.
- **Method:** For total journey time, the thesis compares linear regression, an artificial neural network (ANN), and LSTM. For adjacent-stop travel time, it compares historical averaging, linear regression, and XGBoost gradient boosting.
- **Metrics and key result:** Metrics include MaxAE, MAE, MAPE, and RMSE. For adjacent-stop prediction, Table 8.2 reports XGBoost as best of the three, with MAE 0.80 minutes, RMSE 1.16 minutes, and MaxAE 9.62 minutes. The thesis also reports an LSTM total-journey MAE of 4.28 minutes on route 46, about 43% better than linear regression; it is comparable to the ANN.
- **Limitation or gap:** The data are old and from Dublin, with small, route-specific samples and no external-city validation. The thesis’s Table 8.2 lists XGBoost MAE as 0.80 minutes, while nearby narrative text says 0.84 minutes; use the table value only with that discrepancy noted, or avoid quoting the exact value until checked against the original results table.
- **What carbonOrbit reuses:** Use the historical-average and linear-regression comparisons as defensible simple baselines, and the route/segment distinction to keep the prediction target precise. Treat the reported XGBoost result as a candidate baseline, not as an expected BMTC score.
- **Questions an examiner could ask, with our answer:** **Why is the thesis useful if its data are old?** It demonstrates a transparent comparison between simple baselines and machine-learning models using archived GPS and route information; its numerical results are not transferred to BMTC. **Why flag the 0.80/0.84-minute difference?** Reporting the inconsistency prevents false precision and shows that the original table must be checked before quoting the result.

## 4. Kumar et al. (2025), bus arrival prediction review

**Citation:** B. Anil Kumar, Ramanand Singh, Hima Elsa Shaji, and Lelitha Vanajakshi, “Bus Arrival Time Prediction: A Comprehensive Review,” *IEEE Transactions on Intelligent Transportation Systems*, vol. 26, no. 6, pp. 7362–7379, 2025. [https://doi.org/10.1109/TITS.2025.3545695](https://doi.org/10.1109/TITS.2025.3545695)  
**Read:** Bibliographic record and abstract reviewed on 18 November 2026. The full paper is paywalled; detailed claims are limited to its abstract and publication record.

- **Problem:** Organize the methods and practical decisions involved in designing bus-arrival prediction systems, including data collection and analysis, model selection, input-pattern identification, implementation, and evaluation.
- **Data:** This is a review of prior bus travel-time and arrival-prediction research, not a new dataset or field experiment.
- **Method:** The review surveys methods from naive and physics-based approaches to data-driven models, and discusses route discretization, multi-step prediction, single-route versus multi-route data, performance evaluation, and deployment challenges.
- **Metrics and key result:** The abstract identifies evaluation metrics and performance strategies as an explicit part of the review, but provides no new model score or empirical result. Its practical contribution is a structured checklist of design and evaluation choices.
- **Limitation or gap:** The full text was not accessible for this note, so the detailed taxonomy, study selection, and conclusions must be checked through institutional IEEE access before being described in depth. A review does not validate CarbonOrbit’s own model.
- **What carbonOrbit reuses:** Use the review to organize the survey and evaluation plan: data characteristics, target definition, route/stop representation, forecast horizon, baselines, common metrics, and compute cost should be specified consistently.
- **Questions an examiner could ask, with our answer:** **Can this review justify a particular CarbonOrbit model?** Not by itself. It organizes the choices; model selection must come from CarbonOrbit’s own pre-specified comparison. **Why are we only making broad claims from it?** The full IEEE text was not accessible, so we will verify detailed claims through the college library before expanding them.

## 5. Bhutani, Pachal, and Achar (2022; revised 2024), Seq2Seq RNN

**Citation:** Nancy Bhutani, Soumen Pachal, and Avinash Achar, “Public Transit Arrival Prediction: a Seq2Seq RNN Approach,” arXiv:2210.01655, version 2, 2024 (initial submission 2022). [https://arxiv.org/abs/2210.01655](https://arxiv.org/abs/2210.01655)  
**Read:** Full arXiv HTML paper, version 2, reviewed on 18 November 2026.

- **Problem:** Predict travel times for the remaining sections of a bus route under mixed-traffic conditions, using spatial and temporal patterns and the travel history of nearby buses.
- **Data:** GPS data collected on Delhi route 399 over September–October 2019. The route is divided into 34 sections of 800 metres. The study trains on the first seven weeks and tests on the eighth week.
- **Method:** A gated recurrent unit (GRU) encoder–decoder predicts multiple downstream section times. Its bidirectional decoder (EDB) incorporates synchronized inputs from the closest previous bus and the same weekday in the previous week. It is compared with four spatio-temporal baselines and a unidirectional encoder–decoder (EDU).
- **Metrics and key result:** The study reports MAE and MAPE and tests differences statistically. EDB generally outperforms EDU and the selected baselines on two-step and multi-step predictions. At five steps ahead, the paper reports maximum MAPE improvements of 12.49% over LNKF, 12.92% over SVKF, 5.71% over DpAR, 3.71% over CLSTM, and 8.61% over EDU; these are best-case comparisons, not average improvements.
- **Limitation or gap:** The main evaluation is on one Delhi route and one two-month data window. The approach needs carefully prepared synchronized previous-bus inputs; the paper describes substantial one-time data-preparation complexity. Results do not demonstrate generalization to BMTC or to simulated data.
- **What carbonOrbit reuses:** Use it to justify reporting prediction horizon explicitly and treating deep sequence models as optional candidates. Compare them fairly against simpler baselines on the same held-out days; do not assume their reported gains will transfer to CarbonOrbit.
- **Questions an examiner could ask, with our answer:** **Why not make this model the main CarbonOrbit model?** It was evaluated on one Delhi route with real GPS data and detailed prior-bus inputs; our project has different simulated data and should choose the model that earns its complexity on our own held-out data. **What does “up to” mean in its reported improvement?** It is the largest reported advantage in a comparison, not a typical or guaranteed gain.

---

**Review note:** Read status and access limits are recorded separately for each source. Before final submission, check the paper’s publisher metadata, update access dates, and re-open the paywalled IEEE article through institutional access if available.
