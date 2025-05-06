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

FEC classify primary / general. Imperfect process as some contributions are marked as "g2016" with a date in 2015. Possible discrepancy around separating general // Mention inconsistencies looked at contributions in all of 2015 up through June 8, 2016. I did not use the PGI classification of FEC
