<h1>Austin Income and Housing</h1>

<h2>Intro</h2>
<h6>
Housing is increasing across the US. How much has Austin's housing increased over the past decade and is it still affordable?
</h6>

<h2>Method</h2>
<h6>

- Income Data: Will be using .gov resource Occupational Employment Statistics from 2010-2019
- Affordability Data: Will be using 30% of 2 workers wages. 
- Housing Data:  Housing data will be from Zillow from 2010-2019. `monthly_mortgage` will be calculated with <img src="https://render.githubusercontent.com/render/math?math=P*\frac{r*(1%2Br)^{n}}{(1%2Br)^{n}-1}">
- Time Series : Due to the OES limitation, we will only be evaluating up from 2010-2019, with projections of 2020-2024.
- Machine Learning : Machine learning will be used to project the years 2020-2024
</h6>

<h2>Data</h2>

<h4>Resource 1</h4>
<h6>

30% of income standard for Home affordability: https://www.census.gov/housing/census/publications/who-can-afford.pdf

Mary Schwartz and Ellen Wilson wrote a publication on housing back in 2006 and is still regarded by Harvard (as of 2018) and other well regarded resources as standard to this day. The short of the census publication, is that 30% of income is the threshold for housing affordability until it becomes a housing cost burden.
</h6>

<h4>Resource 2</h4>

<h6>
Occupational Employment Statistics (2010-2019): Data gathered from https://www.bls.gov/oes/tables.htm

Occupational Employment Statistics (OES) has data for several regions across the US separated by year, including the Austin Area, which is found in the 'Metropolitan and non-metropolitan area' HTML and XLS in the link above. The OES has the Austin Area in Texas classified as two regions, both as Austin-Round Rock (post 2014) and as Austin-Round Rock-San Maros (2014 and prior). This distinction has been noted during plotting. We will not be looking at any one specific job as OES has a record called `All Occupations` which is the summary of `All Occupations` within a region. We will be looking at the `H_MEAN` of this `All Occupations` record. Note that these reports are given in May annually.

Due to the sheer size of each OES file per year (33MB), the files were cut down to just the Regions of interest (1. Austin-Round Rock, 2. Austin-Round Rock-San Marcos)
</h6>

<h4>Resource 3A</h4>
<h6>

ZHVI Single-Family Homes Time Series: Data gathered from https://www.zillow.com/research/data/

Zillow has a bunch of really cool data, but we will be looking at Zillow Home Value Index (ZHVI) for Single-Family Homes, which is the typical value for all single-family homes in a given region. Specifically the records under the `Metro` column called 'Austin-Round Rock' area (which does include the largest cities: Austin, Round Rock, Georgetown, San Marcos). Given that the OES released each May, we will be looking at the May columns in the ZHVI file.

To filter out the outliers, the inter-decile mean average is taken (excluding the first and last 10%, so all records from 10-90% are included) for all the regions in Austin-Round Rock records.
</h6>

<h4>Resource 3B</h4>
<h6>

Zillow has an article about down payment on a house https://www.zillow.com/home-buying-guide/down-payment-on-a-house/

Area's around the US vary for a typical down payment on a house. But for simplicity this article shows the benefits of choosing 20%, and we will be using that figure. 20% down payment will be considered a constant from 2010-2019
</h6>

<h4>Resource 4</h4>
<h6>

Macrotrends 30 Year Fixed Mortgage Rate https://www.macrotrends.net/2604/30-year-fixed-mortgage-rate-chart

As mortgage rates change over time, it will not be considered a constant as these have a range of influences from local, state to country-wide economy over time. The only loan type considered will be 30-year fixed mortgage. 
</h6>

<h4>Resource 5</h4>
<h6> 

Bankrate offers a way to calculate mortgage payments https://www.bankrate.com/calculators/mortgages/mortgage-calculator.aspx

We will be using this formula to calculate 30 year fixed rate mortgages.

<h2>Calculations</h2>

<h4>Monthly Wage for 2</h4>

<h6> 

Mean Wage = is taking the `H_MEAN` column of each `All Occupations` records

Assuming a 40 hour work week for 52 weeks a year
`hours_worked_per_month` = <img src="https://render.githubusercontent.com/render/math?math=40\frac{hour(s)}{week(s)}*\frac{52week(s)}{12month(s)}=173.\overline{33}\frac{hour(s)}{month(s)}">

`wage_monthly_for_two` = Mean Wage * `hours_worked_per_month`* 2
</h6>

<h4>30% of Wage for 2<h4>
<h6>

`p30_monthly_wage_for_2` = `wage_monthly_for_two` * 0.30
</h6>

<h4>Mortgage formula<h4>
<h6>

`monthly_mortgage`<img src="https://render.githubusercontent.com/render/math?math==P*\frac{r*(1%2Br)^{n}}{(1%2Br)^{n}-1}">

- `monthly_mortgage` = the total monthly mortgage payment
- P = the principal loan amount
- r = monthly interest rate, varies depending on when a house is sold. This has been accounted for by using Yearly Macrotrends 30-Year Fixed Mortgage rate.
- n = number of payments of lifetime (monthly), assuming 30-year fixed rate
</h6>

<h2>Results</h2>
<h6>

<img src=graphs/OES.png width=325>
<img src=graphs/ZHVI.png width=325>
<img src=graphs/mortgage.png width=325>
<img src=graphs/OES&ZHVIMortgage.png width=500>

As a reminder, an affordable mortgage is considered everything under the 30% wage for 2 workers

If we define affordability as: <img src="https://render.githubusercontent.com/render/math?math=1-\frac{monthly\_mortgage}{30percent\_of\_Wages\_for\_2\_workers}">

Where 
- 100% affordability is essentially free property
- 0% affordability is no longer affordable and considered a "housing burden"

Affordability has shrunk from 67.8% in 2010 to 56.6% in 2019. In 2024, affordability is projected to shrink to 51.8%

These are the results found from the "*Total Mean Wages per Month of 2 Workers vs. Typical Morgage Payment for a New Home Purchase*" graph. The data from the graph can is stored in `results.csv`

<h2>Conclusion</h2>
<h6>

Although affordability has shrunk, homes are still affordable and will continue to be for a while. 
</h6>
