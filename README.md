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

As a reminder, an affordable mortgage is considered everything under the 30% wage for 2 workers (purple line in last graph)

If we define affordability as: <img src="https://render.githubusercontent.com/render/math?math=1-\frac{monthly\_mortgage}{30percent\_of\_Wages\_for\_2\_workers}">

Where 
- 100% affordability is essentially free property
- 0% affordability is no longer affordable and considered a "housing burden"

Affordability has shrunk from 67.8% in 2010 to 56.6% in 2019. In 2024, affordability is projected to shrink to 51.8%

These are the results found from the "*Total Mean Wages per Month of 2 Workers vs. Typical Morgage Payment for a New Home Purchase*" graph. The data down below is in reference to the `results.txt`

|                             |r2  |m        |b          |2010              |2011              |2012             |2013              |2014              |2015              |2016              |2017              |2018              |2019              |2020              |2021              |2022              |2023              |2024              |
|-----------------------------|----|---------|-----------|------------------|------------------|-----------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|------------------|
|Mean Hourly Wage             |0.94|0.468061 |-918.97    |21.82872727272718 |22.29678787878788 |22.76484848484847|23.23290909090906 |23.70096969696965 |24.16903030303024 |24.63709090909083 |25.10515151515142 |25.573212121212123|26.041272727272712|26.509333333333302|26.97739393939389 |27.44545454545448 |27.91351515151507 |28.38157575757566 |
|Mean Wage Monthly for 2      |-   |-        |-          |7567.292121212089 |7729.553131313132 |7891.814141414137|8054.075151515141 |8216.336161616146 |8378.59717171715  |8540.858181818156 |8703.119191919159 |8865.380202020204 |9027.641212121207 |9189.902222222212 |9352.163232323217 |9514.42424242422  |9676.685252525225 |9838.94626262623  |
|Mean 30% Wage Monthly for 2  |-   |-        |-          |2270.1876363636266|2318.8659393939397|2367.544242424241|2416.2225454545423|2464.9008484848437|2513.579151515145 |2562.2574545454468|2610.9357575757476|2659.6140606060612|2708.292363636362 |2756.9706666666634|2805.648969696965 |2854.327272727266 |2903.0055757575674|2951.683878787869 |
|Mean ZHVI House Selling Price|0.95|13730.4  |-27413389.2|184714.80000000075|198445.19999999925|212175.6000000015|225906.0          |239636.3999999985 |253366.80000000075|267097.19999999925|280827.6000000015 |294558.0          |308288.3999999985 |322018.80000000075|335749.19999999925|349479.6000000015 |363210.0          |376940.3999999985 |
|Mean Mortgage Payment        |0.93|49.490475|-98746.71  |729.147364671735  |778.6378399979585 |828.1283153241675|877.618790650391  |927.1092659766146 |976.5997413028381 |1026.090216629047 |1075.5806919552706|1125.0711672814941|1174.561642607703 |1224.0521179339266|1273.5425932601502|1323.0330685863737|1372.5235439125827|1422.0140192388062|


<h2>Conclusion</h2>
<h6>

Although affordability has shrunk, homes are still affordable and will continue to be for a while. 
</h6>
