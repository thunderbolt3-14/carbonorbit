# Phase 1 — Literature and Research Notes (carbonOrbit)

**Author:** Rahul Velpuri (Teammate D — ETA models, statistics, emissions)
**Project:** carbonOrbit (BCSP508 Environmental Science Mini-Project, BMSIT&M)
**Focus Areas:** Transport Emissions, Modal Shift, and the Indian Urban Mobility Context

## 1. Ramachandra & Shwetmala (2009)

### Citation and Link
Ramachandra, T. V., & Shwetmala. (2009). Emissions from India's transport sector: Statewise synthesis. Atmospheric Environment, 43(34), 5510–5517.

### DOI
https://doi.org/10.1016/j.atmosenv.2009.07.015

### Problem and Data Used
Rapid economic liberalization and urbanization in India led to steep increases in fossil-fuel consumption and transport emissions, yet national-level inventories lacked the state- and city-level granularity needed for local mitigation policies. The authors compiled state-wise registered vehicle populations across categories (two-wheelers, cars, jeeps, buses, trucks, light motor vehicles), fuel sales/consumption statistics (diesel, petrol, CNG, aviation fuel, coal), and annual distance travelled assumptions (km/year) using government transport yearbooks and TEDDY (TERI Energy Data Directory and Yearbook) records for 2003–2004.

### Method
A bottom-up, decentralized emission inventory approach was applied for road transport, multiplying vehicle counts, annual utilization (km/year), and fuel-specific emission factors (sourced from IPCC, ALGAS, and Indian ARAI/CPCB studies). Country-level fuel consumption data was used for railways, aviation, and shipping. Emissions per unit urban area were also computed to evaluate pollution density in major metropolitan centres.

### Key Result and Its Units
India's transport sector emitted an estimated 258.10 Tg (teragrams / million tonnes) of $\text{CO}_2$ in 2003–2004, with road transport accounting for 94.5% of total sectoral $\text{CO}_2$ emissions. Among states, Maharashtra contributed the highest share at 28.85 Tg (11.8%), followed by Tamil Nadu (26.41 Tg, 10.8%) and Gujarat (23.31 Tg, 9.6%).

### Limitation or Gap
The inventory relies on static fleet registration records (which often include retired vehicles still on RTO books) and uniform annual utilization averages rather than real-time traffic speed, congestion, idling, or stop-and-go drive cycles. Furthermore, the 2003–2004 baseline predates BS-IV/BS-VI emission standards and fleet electrification.

### What carbonOrbit Can Use From It
Provides foundational macro-justification for why road transport is the primary target for urban GHG mitigation in India (94.5% share). Supplies baseline fuel-specific emission factor structures ($\text{CO}_2$, $\text{CO}$, $\text{NO}_x$, $\text{SO}_2$, $\text{PM}$) and state-level benchmarking context (Karnataka / Bengaluru).

### Potential Examiner Question

> Ramachandra & Shwetmala (2009) used static annual vehicle-kilometre assumptions from 2003–2004. How does carbonOrbit improve upon static emission inventories for modern Bengaluru bus routes?

**Answer angle:** We replace static annual averages with dynamic, real-time GTFS/GPS trajectory data, accounting for segment-level speeds, congestion delays, bus bunching, and occupancy adjustments rather than assuming constant annual mileage.

## 2. ITF (2023) — Life-Cycle Assessment of Passenger Transport in India

### Citation and Link
International Transport Forum (ITF). (2023). Life-Cycle Assessment of Passenger Transport: An Indian Case Study (International Transport Forum Policy Papers, No. 120). OECD Publishing, Paris.

### DOI / URL
https://doi.org/10.1787/2d11e416-en | https://www.itf-oecd.org/sites/default/files/docs/life-cycle-assessment-passenger-transport-india.pdf

### Problem and Data Used
Most Indian transport decarbonization evaluations focus exclusively on tailpipe emissions, ignoring upstream electricity generation mixes (heavy coal share), vehicle/battery manufacturing, and infrastructure construction. The report evaluates urban and inter-urban Indian passenger transport modes (two-wheelers, three-wheelers, private cars, shared taxis, diesel/CNG/electric buses, and metro rail) using Indian grid emission factors, vehicle occupancy rates, and secondary Indian fleet parameters.

### Method
Cradle-to-grave Life-Cycle Assessment (LCA) implemented via the ITF Transport LCA Tool for India (v1.0). Emissions and energy use are modelled across vehicle and battery manufacturing, transport to point of sale, operational use (Well-to-Wheel fuel and electricity production under baseline and clean-grid scenarios), and end-of-life disposal, normalized per vehicle-kilometre (vkm) and per passenger-kilometre (pkm).

### Key Result and Its Units
Battery-electric buses generate at least 24% lower life-cycle GHG emissions per pkm than electric two- and three-wheelers, 71% lower than private cars, and 79% lower than shared cars. Conventional ICE diesel buses still emit 65–76% fewer life-cycle GHGs per pkm than battery-electric private cars due to high passenger occupancy. Transitioning an urban bus to electric saves roughly 460 $\text{tCO}_2\text{e}$ over its lifetime under current policy scenarios, and up to 680 $\text{tCO}_2\text{e}$ additional savings when powered by 100% renewable electricity.

### Limitation or Gap
Assumes fixed average passenger occupancy factors per mode across trips and does not capture real-time operational inefficiencies like bus bunching (where an overloaded lead bus runs alongside an empty trailing bus, spiking per-passenger emissions on the trailing vehicle).

### What carbonOrbit Can Use From It
Validates the pkm (per passenger-kilometre) comparison metric used in carbonOrbit's emission avoidance module. Proves that shifting commuters from private 2W/cars to BMTC buses yields massive $\text{CO}_2\text{e}$ reductions even for existing diesel buses, and even larger gains for BMTC's growing electric bus fleet.

### Potential Examiner Question

> Why does the ITF (2023) study show that a diesel bus has lower per-passenger emissions than an electric private car in India, and how does bus bunching affect that advantage?

**Answer angle:** High occupancy amortizes emissions over 40+ passengers, while EV cars still draw from a coal-heavy grid and carry 1–2 people. However, when bunching occurs, a trailing bus carries very few passengers, driving its g CO2/pkm sharply upward—which carbonOrbit detects and flags.

## 3. CSTEP (2017) — Decarbonisation Impact on Road Transport Sector Emissions

### Citation and Link
Ananthakumar, M. R., & Paladugula, A. L. (2017). Impact of Decarbonisation Strategies on Road Transport Sector Emissions (GHG Platform India — Phase II Policy Brief). Center for Study of Science, Technology and Policy (CSTEP), Bengaluru. URL: https://www.ghgplatform-india.org/wp-content/uploads/publications/phase-2/GHGPI-PhaseII-Decarbonisation%20Impact%20on%20Road%20Transport%20Sector%20Emissions-Oct17.pdf

### Problem and Data Used
Indian road transport GHG emissions rose by 78% between 2005 and 2014 due to rapid motorization. Policymakers needed an empirical comparison between two primary mitigation levers under India's NDC targets: (a) shifting commuters from private vehicles to public bus transport, versus (b) electrifying the vehicle fleet. The study used national diesel/petrol sectoral demand data (PPAC/MoPNG), modal share datasets, and India's grid electricity emission factors for 2014–15 to 2017–18.

### Method
Scenario-based bottom-up modelling using IPCC emission estimation methodologies. Three scenarios were constructed for 2017–18: Business-As-Usual (BAU), a Modal Shift scenario (shifting passenger-kilometres from two-wheelers, cars, and taxis to public buses), and an EV Shift scenario (replacing ICE two-wheelers, cars, taxis, and buses with electric equivalents under the prevailing electricity generation mix).

### Key Result and Its Units
$\text{CO}_2$ constitutes 98% of total road transport GHG ($\text{CO}_2\text{e}$) emissions in India. Under India's coal-dominated electricity grid mix, a modal shift from private two-wheelers, cars, and taxis to public buses reduces net $\text{CO}_2$ emissions more effectively in the near term than an immediate EV shift.

### Limitation or Gap
Aggregates road transport demand at the national level without modelling city-specific transit reliability barriers (such as uncertain waiting times at stops) that prevent private vehicle users from actually switching to buses.

### What carbonOrbit Can Use From It
Directly supports carbonOrbit's core thesis: improving bus reliability and real-time ETA visibility to trigger modal shift is an immediate, high-leverage climate intervention for Bengaluru—complementing, rather than waiting solely for, full fleet electrification. Justifies focusing carbonOrbit's emission tracking primarily on $\text{CO}_2$ (98% of transport GHGs) alongside local particulate matter ($\text{PM}$).

### Potential Examiner Question

> According to CSTEP (2017), why did modal shift outperform fleet electrification in near-term $\text{CO}_2$ reduction, and how does carbonOrbit operationalize modal shift?

**Answer angle:** Because charging EVs on a coal-heavy grid shifts tailpipe emissions upstream to power plants, whereas moving 30–40 private vehicle riders into one bus immediately cuts total vehicle-kilometres travelled. carbonOrbit encourages this shift by eliminating ETA uncertainty and quantifying the exact $\text{CO}_2$ saved per trip.

## 4. TERI (2023) — Per-Passenger Emissions in Delhi (CarbonLite Methodology)

### Citation and Link
The Energy and Resources Institute (TERI) & Delhi Metro Rail Corporation (DMRC). (2023). Comparative Study of Per-Passenger-Kilometre $\text{CO}_2$ Emissions Across Urban Motorized Transport Modes in Delhi (CarbonLite Metro Travel Initiative). TERI, New Delhi. URL: https://new.delhimetrorail.com/en/carbonlite-metro-travel | https://www.teriin.org/files/TERI-Annual-Report-2023-24.pdf

### Problem and Data Used
Commuters rarely see tangible environmental feedback from their daily mode choices, limiting behavioural nudges toward public transit. TERI conducted an empirical emissions benchmarking study in Delhi comparing metro rail against five road modes: city buses, private cars, cabs/taxis, three-wheelers (auto-rickshaws), and two-wheelers, using Delhi fleet fuel-efficiency distributions, fuel emission factors, and average passenger occupancy surveys.

### Method
Fuel consumption per vehicle-kilometre was converted into tailpipe/operational $\text{CO}_2$ emissions using India-specific emission factors and divided by observed modal occupancy rates to derive standardized per-passenger-kilometre (g CO2/pkm) emission intensities. These factors were integrated into DMRC's ticketing system to display trip-level $\text{CO}_2$ savings directly to passengers.

### Key Result and Its Units
Quantified mode-by-mode per-passenger emission intensities in g CO2 / passenger-km, demonstrating that switching a single commuter trip from a private car to mass transit saves approximately 32.4 grams of $\text{CO}_2$ per kilometre (g CO2/pkm). Showed that displaying personalized per-trip carbon savings on commuter interfaces acts as an actionable behavioural nudge toward sustainable public transport.

### Limitation or Gap
Calibrated specifically to Delhi's fuel mix (heavy CNG adoption in buses and autos) and flat terrain, which differs from Bengaluru's BMTC fleet (predominantly diesel + expanding electric buses) and corridor congestion profiles. Uses static average occupancy and speed factors rather than live vehicle speed/delay variations.

### What carbonOrbit Can Use From It
Serves as the direct methodological blueprint for carbonOrbit's Commuter Carbon Savings Calculator—computing the delta between a displaced private vehicle (2W or car) and a BMTC bus trip in g CO2/pkm. Validates the user-facing dashboard design of showing real-time $\text{CO}_2$ avoided per commuter trip.

### Potential Examiner Question

> How does carbonOrbit adapt TERI's Delhi CarbonLite methodology to Bengaluru's BMTC network?

**Answer angle:** While TERI uses static average emission factors for Delhi's CNG-heavy fleet and Metro, carbonOrbit calibrates emission factors for Bengaluru's diesel and electric BMTC buses and adjusts emissions dynamically based on real-time segment speeds and congestion delays.

## 5. Wills et al. (2019) — Service Attribute Prioritization & Modal Shift Dynamics

### Citation and Link
Phadermrod, B., Crowder, R. M., & Wills, G. B. (2019). Importance-Performance Analysis based SWOT analysis. International Journal of Information Management, 44, 194–203. (Note: Cross-referenced in our literature survey alongside urban transit real-time passenger information and modal-shift adoption studies; verify exact URL/DOI from team reference sheet before final report freeze).

### DOI
https://doi.org/10.1016/j.ijinfomgt.2016.03.009

### Problem and Data Used
Service providers (including public transit agencies) frequently misallocate resources because traditional strategic evaluations treat all service attributes as equally important or rely on subjective management opinions rather than empirical commuter perception data. The study analyzes multi-attribute user satisfaction survey datasets where users rate performance across distinct operational attributes alongside overall service satisfaction.

### Method
Combines Multiple Linear Regression (MLR) with Importance-Performance Analysis (IPA) to derive implicit attribute importance (regression weights linking specific service attributes to overall user satisfaction) rather than relying on biased self-reported importance scores. Attributes are mapped onto a four-quadrant matrix (Concentrate Here / Major Weaknesses, Keep Up the Good Work, Low Priority, Possible Overkill) to prioritize high-impact interventions.

### Key Result and Its Units
Demonstrates quantitatively (via standardized regression coefficients $\beta$ and quadrant diagnosticity metrics) that attributes with high implicit impact on user satisfaction but low current operational performance ("Concentrate Here" quadrant) act as the primary bottlenecks driving user defection. Fixing high-importance, low-performance operational gaps produces the largest marginal gain in user retention and mode preference.

### Limitation or Gap
The empirical validation case study in the paper was conducted on service organizations rather than directly measuring tailpipe emissions; therefore, connecting service-quality improvements to $\text{CO}_2$ reductions requires pairing behavioral modal-shift elasticities with physical emission models.

### What carbonOrbit Can Use From It
Provides the analytical rationale for why carbonOrbit targets schedule reliability, accurate ETA prediction, and bus-bunching mitigation: in urban bus systems, waiting-time unpredictability is a classic "high-importance, low-performance" weakness that drives commuters to private two-wheelers and cars. Supports structuring our evaluation metrics around commuter-facing reliability gains alongside environmental metrics.

### Potential Examiner Question

> Why is a service-attribute prioritization paper like Wills et al. (2019) included in an Environmental Science project on bus emissions?

**Answer angle:** Emissions only drop if commuters actually choose buses over private vehicles. Wills et al. provide the quantitative framework showing that fixing high-importance, low-performance bottlenecks—specifically arrival time unpredictability and bunching—is the decisive lever for retaining riders and inducing modal shift.

## Summary Matrix for carbonOrbit Pipeline Integration

| Source | Primary Metric / Unit | Key Takeaway for carbonOrbit |
|---|---|---|
| Ramachandra & Shwetmala (2009) | Tg CO2 / year (94.5% road share) | Establishes road transport as India's dominant GHG source and provides baseline fuel emission factor structures. |
| ITF (2023) | g CO2e / pkm & tCO2e / bus lifetime | Proves buses beat private cars/2Ws by 24–79% on a full life-cycle basis; underscores why high bus occupancy matters. |
| CSTEP (2017) | Mt CO2e scenario deltas | Shows modal shift to buses cuts near-term CO2 faster than EV-only transitions under India's current power grid. |
| TERI (2023) | g CO2 / pkm (~32.4 g/km saved vs car) | Blueprint for calculating and displaying real-time per-passenger CO2 avoidance to commuters. |
| Wills et al. (2019) | Implicit Importance (β) vs. Performance | Justifies targeting arrival reliability and bus bunching as the highest-leverage bottlenecks to drive modal shift. |
