import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
from sklearn import linear_model
import os
from mortgagecalc import MortgagePayment

YEAR_RANGE          = np.arange(2010,2020) #2010-2019, dependent on OES files
YEAR_RANGE_FUTURE   = np.arange(2020,2025) #2020-2024

def OES(graph = False):
    """
    Finds the Selling Price trend of the Austin-Round Rock region.
    
    WARNING: dependent upon OES.csv files to operate

    Parameters
    ----------
    graph: bool
        set to True if you want to see the Graph
    """

    # Accumulating Data
    # Specific Occupation Title found in all .csv's
    occ = "All Occupations"

    # Creation of Ogranized DataFrame
    df_of_occ = pd.DataFrame(columns = ['LOC', 'OCC_TITLE', 'H_MEAN', 'H_MEDIAN'])

    # Organizing Data from several .csv's into one DataFrame
    for year in YEAR_RANGE:
        if year > 2014:
            loc = "Austin-RoundRock"
        elif year <=2014:
            loc = "Austin-RoundRock-SanMarcos"
        filename = os.path.join("data", "OES-{}-May{}.csv".format(loc, year))
        df = pd.read_csv(filename)
        for column in df.columns:
            if column.upper() == "OCC_TITLE": #Finds the OCC_TITLE column
                occ_title_idx = df.columns.get_loc(column) #The OCC_TITLE column index
            elif column.upper() == "H_MEAN":
                h_mean_idx = df.columns.get_loc(column)
            elif column.upper() == "H_MEDIAN":
                h_median_idx = df.columns.get_loc(column)
            else:
                pass
        occ_df = df.iloc[:,[occ_title_idx]]
        occ_idx = occ_df[occ_df==occ].index.values[0]   
        h_mean = float(df.iloc[occ_idx,[h_mean_idx]])
        h_median = float(df.iloc[occ_idx,[h_median_idx]])

        df_of_occ.loc[year] = [loc, occ,h_mean,h_median]



    # Machine Learning
    # data of both Austin-RoundRock and Austin-RoundRock-SandMarcos
    x = df_of_occ.index.values.reshape(-1,1)
    y = df_of_occ['H_MEAN'].values

    # Applying Linear Regression
    regr = linear_model.LinearRegression()
    regr.fit(x,y)
    r2 = round(regr.score(x,y),2)

    # Fitting based on the current Data
    y_bf = regr.predict(x)

    # Predicting future wages
    x_future = YEAR_RANGE_FUTURE.reshape(-1,1)
    y_bf_future = regr.predict(x_future)

    # Values that are just for location Austin-RoundRock-SandMarcos, aka ARRSM
    x_ARRSM = df_of_occ.loc[:2014].index.values
    y_ARRSM = df_of_occ['H_MEAN'].loc[:2014].values

    # Values that are just for location Austin-RoundRock, aka ARR
    x_ARR = df_of_occ.loc[2015:].index.values
    y_ARR = df_of_occ['H_MEAN'].loc[2015:].values



    # Graphing
    if graph == True:
        fig,ax = plt.subplots()
        ax.set( title = "Time Series of Mean OES Hourly Wage of {}\nAustin(A),RoundRock(RR),SanMarcos(SM), Texas".format(occ),
                xlabel = "Years",
                ylabel = "Mean Hourly Wage (Dollars)")
        ax.text( 0.90,0.1, 'R2={}'.format(r2), horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
        ax.plot(   x_ARR,        y_ARR, 'o', color = "#03a1fc", label = 'A, RR')
        ax.plot( x_ARRSM,      y_ARRSM, 'o', color = "#0356fc", label = 'A, RR, SM')
        ax.plot(       x,         y_bf, '-', color = "#0377fc", label = 'Best Fit for A, RR & A, RR, SM')
        ax.plot(x_future,  y_bf_future, '--', color = "#03fc6f", label = 'Prediction')
        ax.set_xticks(np.arange(x[0][0],x_future[-1][0]+1))
        ax.set_xticklabels(ax.get_xticks(), rotation=45, ha='right')
        ax.legend(loc='upper left')
        
        # saving the graph
        graph_filename = "OES.png"
        child_dir = "graphs"
        if not os.path.exists(child_dir):
            os.makedirs(child_dir)
        plt.savefig(os.path.join(child_dir, graph_filename), dpi=300, bbox_inches='tight')
        plt.show()
        print("saving {} in {}".format(graph_filename, os.getcwd()))

    return(x,y,y_bf,x_future,y_bf_future,regr, r2)



def ZHVI (graph = False):
    """
    Finds the Selling Price trend of the Austin-Round Rock region.
    
    WARNING: dependent upon ZHVI-SingleFamilyHomes.csv to operate

    Parameters
    ----------
    graph: bool
        set to True if you want to see the Graph
    """

    # Accumulating Data
    filename = os.path.join("data", "ZHVI-SingleFamilyHomes.csv")
    df_data = pd.read_csv(filename)
    loc = "Austin-Round Rock"
    Austin_RoundRock_idx = df_data['Metro'][df_data['Metro']==loc].index.values

    df_ARRSM = df_data.iloc[Austin_RoundRock_idx]
    dates = ["{}-05-31".format(year) for year in YEAR_RANGE] #2010-2019
    avg_sell = []

    for date in dates:
        q10 = df_ARRSM[date].quantile(0.10)
        q90 = df_ARRSM[date].quantile(0.90)
        avg_spy_em = df_ARRSM[date].values #average sell price in year for 'each' Metro, just now in an array for logic splicing
        m_avg_spy_am = int(avg_spy_em[(avg_spy_em > q10) & (avg_spy_em < q90)].mean())# mean of average sell price in year for 'all' Metro
        avg_sell.append(m_avg_spy_am)
    years = [int(date[:4]) for date in dates]



    # Machine Learning
    # data of both Austin-RoundRock and Austin-RoundRock-SandMarcos
    x = np.array(years).reshape(-1,1)
    y = np.array(avg_sell)

    # Applying Linear Regression
    regr = linear_model.LinearRegression()
    regr.fit(x,y)
    r2 = round(regr.score(x,y),2)

    # Fitting based on the current Data
    y_bf = regr.predict(x)

    # Predicting future wages
    x_future = YEAR_RANGE_FUTURE.reshape(-1,1)
    y_bf_future = regr.predict(x_future)



    # Graphing
    if graph == True:
        fig,ax = plt.subplots()
        ax.set( title = "Mean House Sell Price in range 10-90% of ZHVI for\nAustin(A),RoundRock(RR),SanMarcos(SM), Texas",
                xlabel = "Years",
                ylabel = "Mean of 10-90% ZHVI (Dollars)")
        ax.text( 0.90,0.1, 'R2={}'.format(r2), horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
        ax.plot(       x,            y, 'o', color = "#000000", label = 'A, RR, SM')
        ax.plot(       x,         y_bf, '-', color = "#000000", label = 'Best Fit for A, RR, SM')
        ax.plot(x_future,  y_bf_future, '--', color = "#6A5D5D", label = 'Prediction')
        ax.set_xticks(np.arange(x[0][0],x_future[-1][0]+1))
        ax.set_xticklabels(ax.get_xticks(), rotation=45, ha='right')
        ax.legend(loc='upper left')

        # Saving the graph
        graph_filename = "ZHVI.png"
        child_dir = "graphs"
        if not os.path.exists(child_dir):
            os.makedirs(child_dir)
        plt.savefig(os.path.join(child_dir, graph_filename), dpi=300, bbox_inches='tight')
        print("saving {} in {}".format(graph_filename, os.getcwd()))

    return(x,y,y_bf,x_future,y_bf_future,regr, r2)

def mortgage(sp, sp_future, graph = False):
    """
    Finds the mortage trend of now and projected for the future

    Parameters
    ----------
    sp : numpy.ndarray dtype=ints
        the selling price of the house. For example 300000.
    sp_future: numpy.ndarray dtype=ints
        the selling price of the house projected. For example 300000.
    graph: bool
        set to True if you want to see the Graph
    """

    # Machine Learning
    # Reshaping the Data
    x = YEAR_RANGE.reshape(-1,1)
    y = MortgagePayment(x.flatten(), sp).Ms

    # Applying Linear Regression
    regr = linear_model.LinearRegression()
    regr.fit(x,y)
    r2 = round(regr.score(x,y),2)

    # Fitting based on the current Data
    y_bf = regr.predict(x)

    # Predicting future wages
    x_future = YEAR_RANGE_FUTURE.reshape(-1,1)
    y_bf_future = regr.predict(x_future)



    # Graphing
    if graph == True:
        fig,ax = plt.subplots()
        ax.set( title = "Mean Mortgage Payment for\nAustin(A),RoundRock(RR),SanMarcos(SM), Texas",
                xlabel = "Years",
                ylabel = "Typical Mortgage Payment (Dollars)")
        ax.text( 0.90,0.1, 'R2={}'.format(r2), horizontalalignment='center', verticalalignment='center', transform=ax.transAxes)
        ax.plot(       x,            y, 'o', color = "#000000", label = 'A, RR, SM')
        ax.plot(       x,         y_bf, '-', color = "#000000", label = 'Best Fit for A, RR, SM')
        ax.plot(x_future,  y_bf_future, '--', color = "#6A5D5D", label = 'Prediction')
        ax.set_xticks(np.arange(x[0][0],x_future[-1][0]+1))
        ax.set_xticklabels(ax.get_xticks(), rotation=45, ha='right')
        ax.legend(loc='upper left')

        # Saving the graph
        graph_filename = "mortgage.png"
        child_dir = "graphs"
        if not os.path.exists(child_dir):
            os.makedirs(child_dir)
        plt.savefig(os.path.join(child_dir, graph_filename), dpi=300, bbox_inches='tight')
        print("saving {} in {}".format(graph_filename, os.getcwd()))
        plt.show()

    return(x,y,y_bf,x_future,y_bf_future,regr, r2)

# Accumulating the Data
#x and x_future from both OES() and ZHVI() are the same, hence the same variable
x,  y_oes,  y_bf_oes, x_future,   y_bf_future_oes,   regr_oes,    r2_oes = OES(graph = True)
x, y_zhvi, y_bf_zhvi, x_future,  y_bf_future_zhvi,  regr_zhvi,   r2_zhvi = ZHVI(graph = True)
x, y_mort, y_bf_mort, x_future,  y_bf_future_mort,  regr_mort,   r2_mort = mortgage(y_bf_zhvi, y_bf_future_zhvi, graph = True)

hours_worked_per_month = (40 * 52 / 12)

wage_monthly_for_2          = y_bf_oes*hours_worked_per_month * 2
wage_monthly_future_for_2   = y_bf_future_oes*hours_worked_per_month * 2

p30_monthly_wage_for_2         = wage_monthly_for_2 * 0.3
p30_monthly_wage_future_for_2  = wage_monthly_future_for_2 * 0.3

monthly_mortgage = y_bf_mort
monthly_mortgage_future = y_bf_future_mort

# Saving data to csv
column_names = ['r2', 'm', 'b'] + list(YEAR_RANGE) + list(YEAR_RANGE_FUTURE)
df = pd.DataFrame(columns=column_names)
df.loc['Mean Hourly Wage'] = [r2_oes, round(regr_oes.coef_[0],6), round(regr_oes.intercept_,2)] +list(y_bf_oes) + list(y_bf_future_oes)
df.loc['Mean Wage Monthly for 2'] = ['-', '-', '-'] +list(wage_monthly_for_2) + list(wage_monthly_future_for_2)
df.loc['Mean 30% Wage Monthly for 2'] = ['-', '-', '-'] +list(p30_monthly_wage_for_2 ) + list(p30_monthly_wage_future_for_2)
df.loc['Mean ZHVI House Selling Price'] = [r2_zhvi, round(regr_zhvi.coef_[0],6), round(regr_zhvi.intercept_,2)] + list(y_bf_zhvi) + list(y_bf_future_zhvi)
df.loc['Mean Mortgage Payment'] = [r2_mort, round(regr_mort.coef_[0],6), round(regr_mort.intercept_,2)] + list(y_bf_mort) + list(y_bf_future_mort)
df.to_csv("results.csv")



# Graphing
plt.plot(       x.flatten(),            wage_monthly_for_2,  '-', color = '#0356fc', label = "Mean Wages for 2 Workers")
plt.plot(x_future.flatten(),     wage_monthly_future_for_2, '--', color = '#03fc6f', label = "Mean Wage Prediction for 2 Workers")

plt.plot(       x.flatten(),        p30_monthly_wage_for_2,  '-', color = '#9600FD', label = "30% of Mean Wages for 2 Workers")
plt.plot(x_future.flatten(), p30_monthly_wage_future_for_2, '--', color = '#5D00FD', label = "30% of Mean Wages for 2 Workers Prediction")

plt.plot(       x.flatten(),              monthly_mortgage, '-', color = '#000000', label = "Mean Mortage")
plt.plot(x_future.flatten(),       monthly_mortgage_future,'--', color = '#6A5D5D', label = "Mean Mortgage Prediction")

plt.ylabel("Dollars per Month")
plt.xlabel("Years")
plt.legend(bbox_to_anchor=(1,1), loc="upper left")
plt.xticks(np.arange(x[0][0],x_future[-1][0]+1), rotation=45)
plt.title(label = "Total Mean Wages per Month of 2 Workers vs.\nTypical Mortgage Payment for a New Home Purchase\nAustin(A),RoundRock(RR),SanMarcos(SM), Texas")

# Saving the Graphs
graph_filename = "OES&ZHVIMortgage.png"
child_dir = "graphs"
if not os.path.exists(child_dir):
    os.makedirs(child_dir)
plt.savefig(os.path.join(child_dir, graph_filename), dpi=300, bbox_inches='tight')
plt.show()
print("saving {} in {}".format(graph_filename, os.getcwd()))

# OES_and_ZHVI()





