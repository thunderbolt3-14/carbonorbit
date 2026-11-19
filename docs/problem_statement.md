# Problem Statement — carbonOrbit

**Phase:** 1 draft for team and guide review
**Project:** Real-Time Bus Tracking and ETA Prediction for Sustainable Urban Mobility
**Evidence boundary:** Proposed study; results have not yet been produced.

## Context

Bus passengers face uncertainty about when a bus will arrive, while irregular delays and headways can make service less reliable. GPS-based estimated-time-of-arrival (ETA) prediction and reliability alerts can make service information more useful, but an accurate prediction system does not by itself demonstrate improved passenger behaviour, operational performance, or lower emissions.

The project currently has no verified live BMTC vehicle-position feed. Its proposed data design uses a documented BMTC route and timetable snapshot as geographic and service context, then generates synthetic bus trajectories, delays, and bunching events with known labels. Consequently, model performance will be measured against simulator ground truth. It will not be a field validation of actual BMTC operations.

## Problem

There is a need for a small, reproducible workflow that can estimate bus arrival times and identify simulated delay and bunching events on selected BMTC routes, while making clear what evidence would be required to estimate environmental effects. The project must compare ETA approaches on held-out time periods, evaluate event detection against known labels, and keep any emissions calculation separate from observed passenger response. Since no passenger diversion data are available, the environmental component can only report scenario-based estimates under explicit assumptions about additional bus service, private-vehicle trips displaced, occupancy, distance, and emission factors.

## Scope boundary

- Route, stop, shape, and timetable information may come from a documented GTFS snapshot; its source, licence, version, and limitations must be recorded first.
- Bus locations, speeds, dwell, delays, missing pings, and reliability-event labels are synthetic unless a verified real-time feed is separately obtained and approved for use.
- ETA and reliability results describe performance on the selected simulation configuration and held-out simulated periods.
- Emissions results are conditional scenarios, not measured BMTC savings or causal effects of better ETA information.
- Tailpipe particulate emissions must not be described as ambient PM2.5 concentration changes. Life-cycle and operational emission boundaries must not be mixed.

## Research question

How well do pre-specified ETA methods predict stop arrivals, and how reliably can delay and bunching events be detected, on reproducibly simulated service using selected BMTC routes—and how sensitive are explicitly bounded emissions scenarios to their assumptions?
