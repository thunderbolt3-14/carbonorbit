# Bus Bunching and Delay Literature Notes — Naga Sai

## 1. Andres and Nair (2017)

**Citation:** Matthias Andres and Rahul Nair, “A predictive-control framework to address bus bunching,” *Transportation Research Part B: Methodological*, vol. 104, pp. 123–148, 2017.  
**Link:** https://doi.org/10.1016/j.trb.2017.06.013  
**Read:** Abstract and publication record reviewed; full paper wasn’t accessible from the linked source.

- **Problem:** Buses on busy routes can lose their regular spacing and arrive close together, which harms service reliability.
- **Data or study scope:** The study uses data from a busy bus route in Dublin and also examines an artificial route through simulation.
- **Method:** The authors predict bus headways (the time gaps between buses) and study whether holding buses at stops can reduce irregular gaps.
- **Main findings:** The paper explores combining headway prediction with dynamic holding as a way to reduce bunching.
- **Limitations:** The approach includes operational control—deciding to hold buses—which our project does not implement. Our project uses simulated GPS data, so we cannot claim that its results show what would happen on an actual bus route.
- **Relevance to carbonOrbit:** It helps explain why headway gaps are useful for understanding bunching. Our project will detect and display bunching alerts rather than control bus movements.

## 2. Rezazada, Nassir, and Tanin (2022)

**Citation:** Mustafa Rezazada, Neema Nassir, and Egemen Tanin, “Public transport bunching: A critical review with focus on methods and findings for implications for policy and future research,” *Australasian Transport Research Forum*, 2022.  
**Link:** https://trid.trb.org/View/2259767  
**Read:** Conference paper PDF reviewed

- **Problem:** The review examines bus bunching, its causes, how researchers model it, and strategies proposed to address it.
- **Data or review scope:** This is a review of previous research, not a new GPS data collection study.
- **Method:** The authors organize and discuss existing definitions, contributing factors, models, and control strategies.
- **Main findings:** The review describes bunching as harmful to passengers and operators. It also points to areas that need more attention, including passenger-focused approaches and the way contributing factors vary over time and place.
- **Limitations:** Because this is a review, its conclusions depend on the studies it covers. It does not validate our project’s detection method or simulated data.
- **Relevance to carbonOrbit:** It supports explaining why bunching matters and why we should clearly state how our system defines and detects a bunching event.

## 3. Rezazada, Nassir, Tanin, and Ceder (2024)

**Citation:** Mustafa Rezazada, Neema Nassir, Egemen Tanin, and Avishai (Avi) Ceder, “Bus bunching: a comprehensive review from demand, supply, and decision-making perspectives,” *Transport Reviews*, vol. 44, no. 4, pp. 766–790, 2024.  
**Link:** https://doi.org/10.1080/01441647.2024.2313969  
**Read:** Open-access article page and available text reviewed

- **Problem:** The review studies the causes and consequences of bus bunching and the strategies proposed to manage it.
- **Data or review scope:** It reviews existing research from demand, supply, and decision-making perspectives.
- **Method:** The authors classify and compare earlier studies and their bunching strategies.
- **Main findings:** The review highlights that bunching reduces service reliability. It calls for more realistic evaluations and real-world applications, and discusses whether strategies focus on passengers, operators, or both.
- **Limitations:** This article reviews other research; it does not test carbonOrbit or prove that our simulated alerts improve real bus services.
- **Relevance to carbonOrbit:** It helps us explain the passenger and operational importance of bunching, and why our evaluation must clearly identify its simulated-data limits.

## 4. Yang, Cheng, and Liu (2024)

**Citation:** Ying Yang, Junchi Cheng, and Yang Liu, “An overview of solutions to the bus bunching problem in urban bus systems,” *Frontiers of Engineering Management*, vol. 11, pp. 661–675, 2024.  
**Link:** https://doi.org/10.1007/s42524-024-0297-1  
**Read:** Open-access article reviewed.

- **Problem:** The article surveys proposed ways of addressing bus bunching in urban bus systems.
- **Data or review scope:** This is a review of existing solution approaches, not a new field data collection study.
- **Method:** The authors group and discuss approaches from previous research.
- **Main findings:** The review describes bus bunching as an ongoing challenge and notes a gap in combining approaches from different directions.
- **Limitations:** Since it is a review, it does not test our detection system or establish that a dashboard alone can prevent bunching.
- **Relevance to carbonOrbit:** It helps us keep our project scope realistic: we will monitor and report bunching, not attempt to solve it with bus-control strategies.