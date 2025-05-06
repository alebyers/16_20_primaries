# FEC Democratic Primary Contributions Analysis: 2016 & 2020

## Purpose of the Project

This repository explores financial contributions to Democratic presidential primary candidates during the 2016 and 2020 election cycles. The project has three key goals:

1. To investigate whether there is a relationship between individual-level contributions and voting outcomes across the U.S.
1. To evaluate the potential electoral impact of the 2016 voter purge in Brooklyn on the Hillary Clinton vs. Bernie Sanders primary results.
1. To examine how ActBlue, a PAC-like fundraising platform, appears in the Federal Election Commission’s (FEC) individual contributions dataset.

## Data Sources

All raw data used in this project are publicly available:

* FEC candidate master file and individual contributions file:
  * [2016 Data](https://www.fec.gov/data/browse-data/?tab=bulk-data)
  * [2020 Data](https://www.fec.gov/data/browse-data/?tab=bulk-data)
* U.S. Census Shapefiles:
  * [State Boundaries](https://www.census.gov/geographies/mapping-files/time-series/geo/cartographic-boundary.2020.html#list-tab-1883739534)
  * [ZIP Code Tabulation Areas (ZCTAs)](https://www.census.gov/cgi-bin/geo/shapefiles/index.php)

## Repository Structure

Since analysis was done for two elections with different candidates, there is a 2016 folder and 2020 folder each with their own data, Python scripts and outputs. See the individual year-specific README files for detailed instructions.

## Caveats

FEC Classification Inconsistencies: The Federal Election Commission's (FEC) designation of contributions as either "primary" or "general" can be unreliable. Some contributions marked as “g2016” (for the general election) are dated as early as 2012, well before the official start of the 2016 election cycle. This raises concerns about data cleanliness and highlights the difficulty in clearly distinguishing between primary and general election contributions.

PGI Field Not Used: Due to these inconsistencies, this analysis did not rely on the FEC’s TRANSACTION_PGI (Primary/General Indicator) field to filter contributions. Instead, contributions made during the active campaign period were considered. For the 2016 analysis, this included all of 2015 to June 8, 2016 → Bernie Sanders suspended his campaign.

Geographic Anomalies in NYC: Contribution behavior in New York City deviates from broader national trends. Specifically, the city shows stronger individual-level support for Hillary Clinton relative to Bernie Sanders, which stands in contrast to other progressive-leaning urban areas. Several factors may explain this: Hillary Clinton had recently served as U.S. Senator for New York, while Bernie Sanders, though born in Brooklyn, had lived in Vermont for decades and may have lacked recent political ties to the area. Lastly, Bernie’s base of support included many new and independent voters who may have been less likely to contribute financially or register in time for New York’s closed primaries.
