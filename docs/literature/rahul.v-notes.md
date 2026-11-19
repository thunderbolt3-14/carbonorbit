# Phase 1 — Literature and Research Notes (carbonOrbit)

**Author:** Rahul Velpuri (Teammate D — ETA models, statistics, emissions)
**Project:** carbonOrbit (BCSP508 Environmental Science Mini-Project, BMSIT&M)
**Focus Areas:** Transport Emissions, Modal Shift, and the Indian Urban Mobility Context

## 1. Ramachandra & Shwetmala (2009)

### Citation and Link
Ramachandra, T. V., & Shwetmala. (2009). Emissions from India's transport sector: Statewise synthesis. Atmospheric Environment, 43(34), 5510–5517.

### DOI
https://doi.org/10.1016/j.atmosenv.2009.07.015

### Problem and data
Rapid economic liberalization and urbanization in India led to steep increases in fossil-fuel consumption and transport emissions, yet national-level inventories lacked the state- and city-level granularity needed for local mitigation policies. The authors compiled state-wise registered vehicle populations across categories (two-wheelers, cars, jeeps, buses, trucks, light motor vehicles), fuel sales/consumption statistics (diesel, petrol, CNG, aviation fuel, coal), and annual distance travelled assumptions (km/year) using government transport yearbooks and TEDDY (TERI Energy Data Directory and Yearbook) records for 2003–2004.

### Method
A bottom-up, decentralized emission inventory approach was applied for road transport, multiplying vehicle counts, annual utilization (km/year), and fuel-specific emission factors (sourced from IPCC, ALGAS, and Indian ARAI/CPCB studies). Country-level fuel consumption data was used for railways, aviation, and shipping. Emissions per unit urban area were also computed to evaluate pollution density in major metropolitan centres.

### Metrics and key result
India's transport sector emitted an estimated 258.10 Tg (teragrams / million tonnes) of $\text{CO}_2$ in 2003–2004, with road transport accounting for 94.5% of total sectoral $\text{CO}_2$ emissions. Among states, Maharashtra contributed the highest share at 28.85 Tg (11.8%), followed by Tamil Nadu (26.41 Tg, 10.8%) and Gujarat (23.31 Tg, 9.6%).

### Limitation or gap
The inventory relies on static fleet registration records (which often include retired vehicles still on RTO books) and uniform annual utilization averages rather than real-time traffic speed, congestion, idling, or stop-and-go drive cycles. Furthermore, the 2003–2004 baseline predates BS-IV/BS-VI emission standards and fleet electrification.

### What carbonOrbit reuses
Provides historical national context for road transport's share of transport-sector CO2 emissions and describes inventory methods. Its 2003–04 factors and state totals are not current BMTC inputs or a Bengaluru benchmark.

### Questions an examiner could ask, with our answer

> Ramachandra & Shwetmala (2009) used static annual vehicle-kilometre assumptions from 2003–2004. How does carbonOrbit improve upon static emission inventories for modern Bengaluru bus routes?

**Answer:** We do not replace the inventory with observed real-time data. The proposed simulator uses GTFS route context and synthetic GPS trajectories; any emissions estimate remains conditional until locally justified activity and vehicle factors are available.

## 2. ITF (2023) — Life-Cycle Assessment of Passenger Transport in India

### Citation and Link
International Transport Forum (ITF). (2023). Life-Cycle Assessment of Passenger Transport: An Indian Case Study (International Transport Forum Policy Papers, No. 120). OECD Publishing, Paris.

### DOI / URL
https://doi.org/10.1787/2d11e416-en | https://www.itf-oecd.org/sites/default/files/docs/life-cycle-assessment-passenger-transport-india.pdf

### Problem and data
Most Indian transport decarbonization evaluations focus exclusively on tailpipe emissions, ignoring upstream electricity generation mixes (heavy coal share), vehicle/battery manufacturing, and infrastructure construction. The report evaluates urban and inter-urban Indian passenger transport modes (two-wheelers, three-wheelers, private cars, shared taxis, diesel/CNG/electric buses, and metro rail) using Indian grid emission factors, vehicle occupancy rates, and secondary Indian fleet parameters.

### Method
Cradle-to-grave Life-Cycle Assessment (LCA) implemented via the ITF Transport LCA Tool for India (v1.0). Emissions and energy use are modelled across vehicle and battery manufacturing, transport to point of sale, operational use (Well-to-Wheel fuel and electricity production under baseline and clean-grid scenarios), and end-of-life disposal, normalized per vehicle-kilometre (vkm) and per passenger-kilometre (pkm).

### Metrics and key result
Battery-electric buses generate at least 24% lower life-cycle GHG emissions per pkm than electric two- and three-wheelers, 71% lower than private cars, and 79% lower than shared cars. Conventional ICE diesel buses still emit 65–76% fewer life-cycle GHGs per pkm than battery-electric private cars due to high passenger occupancy. Transitioning an urban bus to electric saves roughly 460 $\text{tCO}_2\text{e}$ over its lifetime under current policy scenarios, and up to 680 $\text{tCO}_2\text{e}$ additional savings when powered by 100% renewable electricity.

### Limitation or gap
Assumes fixed average passenger occupancy factors per mode across trips and does not capture real-time operational inefficiencies like bus bunching (where an overloaded lead bus runs alongside an empty trailing bus, spiking per-passenger emissions on the trailing vehicle).

### What carbonOrbit reuses
Supports using passenger-kilometres and a consistent lifecycle boundary when discussing mode comparisons. It does not prove a Bengaluru mode shift or provide project-specific BMTC factors; any comparison must use matched boundaries and explicit occupancy and diversion assumptions.

### Questions an examiner could ask, with our answer

> Why does the ITF (2023) study show that a diesel bus has lower per-passenger emissions than an electric private car in India, and how does bus bunching affect that advantage?

**Answer:** The report's comparison reflects its lifecycle assumptions and occupancy values. A lightly loaded bus could have higher emissions per passenger-kilometre, but carbonOrbit has no passenger-load data and does not quantify this effect; it should be presented only as a scenario if supported by declared inputs.

## 3. CSTEP (2017) — Decarbonisation Impact on Road Transport Sector Emissions

### Citation and Link
Ananthakumar, M. R., & Paladugula, A. L. (2017). Impact of Decarbonisation Strategies on Road Transport Sector Emissions (GHG Platform India — Phase II Policy Brief). Center for Study of Science, Technology and Policy (CSTEP), Bengaluru. URL: https://www.ghgplatform-india.org/wp-content/uploads/publications/phase-2/GHGPI-PhaseII-Decarbonisation%20Impact%20on%20Road%20Transport%20Sector%20Emissions-Oct17.pdf

### Problem and data
The report compares two national mitigation scenarios: shifting passenger-kilometres from two-wheelers, cars, and taxis to public transport versus shifting passenger-kilometres from hydrocarbon vehicles to EVs. It uses 2014–15 as the baseline and estimates 2017–18 outcomes. The report states that CO2 represents 98% of transport-sector GHG emissions; this should not be paraphrased as 98% of road-transport-only emissions.

### Method
Scenario-based modelling using IPCC methods. For 2017–18, BAU is compared with a 30% passenger-kilometre modal shift from two-wheelers, cars, and taxis to public transport, and a 30% EV shift from hydrocarbon vehicles. A further EV case assumes renewable electricity.

### Metrics and key result
$\text{CO}_2$ represents 98% of transport-sector GHG emissions in the report. Its 30% modal-shift scenario reduces CO2 emissions by 24% versus BAU; its EV-shift scenario reduces CO2 by 11% versus BAU under the then-current grid assumptions. The renewable-powered EV scenario produces 34% greater reductions than the modal-shift scenario. These are national modeled scenarios, not measured Bengaluru outcomes.

### Limitation or gap
Aggregates road transport demand at the national level without modelling city-specific transit reliability barriers (such as uncertain waiting times at stops) that prevent private vehicle users from actually switching to buses.

### What carbonOrbit reuses
Use the report as national scenario context for comparing mode shift and electrification, not as evidence that ETA improvements cause mode shift. Its 98% statement concerns CO2's share of transport-sector GHG emissions in the report. It does not supply current BMTC emission factors or support local PM estimates.

### Questions an examiner could ask, with our answer

> According to CSTEP (2017), why did modal shift outperform fleet electrification in near-term $\text{CO}_2$ reduction, and how does carbonOrbit operationalize modal shift?

**Answer:** In this report's scenarios, the modeled 30% passenger-kilometre shift to public transport reduced CO2 more than a 30% EV shift under the stated grid assumptions. carbonOrbit does not operationalize or measure modal shift; it can only show conditional emissions scenarios unless passenger behavior is observed.

## 4. TERI (undated) — Per-Passenger Emissions in Delhi

### Citation and Link
The Energy and Resources Institute (TERI). (n.d.). “Emission Saving Made by a Passenger by Choosing to Travel by Delhi Metro.” [Report PDF](https://www.teriin.org/sites/default/transport/Per_passenger_emission_in_Delhi_Different_Modes.pdf). The PDF uses 2019–20 public-transport data and car-registration data through 12 June 2023; its publication year is not stated in the PDF. Do not describe it as a “CarbonLite” branded study without a primary source confirming that title.

### Problem and data
The report estimates CO2 intensity for Delhi Metro and five road modes: buses, private cars, cabs/taxis, three-wheelers, and two-wheelers. It uses operator activity data, fuel/mileage assumptions, emission factors, passenger-kilometre estimates, and assumed occupancies; its inputs span different years, including 2019–20 public-transport data.

### Method
The report estimates mode-specific g CO2 per passenger-kilometre. It presents two Delhi Metro electricity-accounting methods and computes a weighted-average Delhi road-mode intensity for comparison with Metro. The PDF proposes passenger-facing savings messages; it does not establish that the values were integrated into DMRC ticketing or that a behavioral effect was measured.

### Metrics and key result
The report estimates bus intensity at 29.48 g CO2/pkm and private-car intensity at 87.73 g CO2/pkm for its Delhi assumptions. Its 32.38 g CO2/pkm saving compares the weighted-average Delhi road-mode intensity (53.11) with Delhi Metro Method 2 (20.73), not a private-car-to-bus trip. These are Delhi operational estimates, not carbonOrbit factors.

### Limitation or gap
Specific to Delhi's fleet, activity records, and assumptions; bus fuel is modeled as CNG in this report. It is not a Bengaluru calibration, does not estimate the effect of live ETA information, and does not provide a life-cycle comparison. The PDF does not describe live-speed adjustment.

### What carbonOrbit reuses
Provides an example of transparent per-passenger-kilometre accounting and weighted mode comparisons. Do not transfer its Delhi intensities to Bengaluru. A carbonOrbit bus-versus-private-vehicle calculation needs locally justified factors and explicit occupancy, distance, and diversion assumptions.

### Questions an examiner could ask, with our answer

> Can we apply TERI's 32.38 g CO2/pkm saving directly to a BMTC bus trip?

**Answer:** No. The 32.38 figure compares Delhi Metro Method 2 with a weighted Delhi road-mode average, not a BMTC bus with a private car. We need a consistent Bengaluru scenario and locally appropriate inputs.

## 5. Wills et al. (2019) — GPS-Based Bus Greenhouse-Gas Estimation

### Citation and Link
Wills, W., Meirelles, J., Baptista, V. G., Cury, G., & Cerdeira, P. (2019). “A Simple Sinuosity-Based Method Using GPS Data to Support Mitigation Policies for Public Buses GHG Emissions.” [arXiv:1907.09335](https://arxiv.org/abs/1907.09335), DOI: [10.48550/arXiv.1907.09335](https://doi.org/10.48550/arXiv.1907.09335). This is the preprint matching the team’s source list; it is not the Phadermrod et al. importance-performance-analysis paper.

### DOI
https://doi.org/10.48550/arXiv.1907.09335

### Problem and data
The paper addresses the difficulty of estimating spatially and temporally detailed bus greenhouse-gas emissions when conventional fuel-use inventories provide aggregate totals. It proposes using bus GPS trajectories to estimate operating activity and emissions.

### Method
The method reconstructs distances from successive GPS records using a sinuosity adjustment, estimates average speed from GPS points, applies a speed–fuel-consumption relation, and derives emissions. The study applies its method to one year of bus GPS data in Rio de Janeiro and compares estimates with top-down fuel-consumption estimates.

### Metrics and key result
The authors report that GPS-based estimates were consistent with top-down estimates after a data-filling step, while providing finer spatial and temporal detail. This is a method demonstration; do not treat its values as BMTC emission factors.

### Limitation or gap
The method depends on GPS completeness, filling/interpolation, assumptions in the speed–consumption function, and available vehicle/emission parameters. Its Rio de Janeiro fleet and operating context do not validate Bengaluru factors. It does not estimate passenger response, modal shift, or the causal emissions effect of better ETA information.

### What carbonOrbit reuses
Provides a candidate activity-data workflow for estimating bus emissions from GPS-derived distance and speed. carbonOrbit may reuse the general structure only after obtaining suitable vehicle-specific fuel/emission parameters; synthetic GPS alone cannot establish real BMTC emissions or passenger diversion.

### Questions an examiner could ask, with our answer

> Can carbonOrbit use this paper to claim that accurate ETA information reduces emissions?

**Answer:** No. The paper estimates bus emissions from GPS-derived activity. It does not study ETA information or passenger mode choice. carbonOrbit must keep emissions scenarios separate and state any diversion as an assumption.

## Summary Matrix for carbonOrbit Pipeline Integration

| Source | Primary Metric / Unit | Key Takeaway for carbonOrbit |
|---|---|---|
| Ramachandra & Shwetmala (2009) | Tg CO2 / year (94.5% road share) | Establishes road transport as India's dominant GHG source and provides baseline fuel emission factor structures. |
| ITF (2023) | g CO2e / pkm & tCO2e / bus lifetime | Proves buses beat private cars/2Ws by 24–79% on a full life-cycle basis; underscores why high bus occupancy matters. |
| CSTEP (2017) | 24% CO2 reduction for 30% modal shift; 11% for EV shift in national modeled scenarios | Scenario comparison only; does not establish ETA-caused mode shift or local BMTC outcomes. |
| TERI (n.d.; 2019–20 public-transport data) | Bus 29.48 and private car 87.73 g CO2/pkm under Delhi assumptions; 32.38 g/pkm is Metro vs weighted road modes | Example of mode-specific CO2 intensity and weighted comparisons; not a BMTC factor or demonstrated behavior change. |
| Wills et al. (2019) | GPS-derived activity and estimated GHG emissions | Provides a method reference for trajectory-based bus-emissions estimation; it is not evidence of ETA-driven modal shift. |
