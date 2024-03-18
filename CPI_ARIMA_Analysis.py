import pandas as pd
from statsmodels.tsa.stattools import adfuller
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.holtwinters import ExponentialSmoothing
from sklearn.metrics import mean_absolute_error
import matplotlib.pyplot as plt
import os

def load_cpi_data(filepath, header_row=0):
    return pd.read_excel(filepath, header=header_row)

def prepare_cpi_series(cpi_data, category, start_year, end_year):
    # Filter the data for the selected category
    category_data = cpi_data[cpi_data['Consumer Price Index item'] == category]
    
    # If the category data is empty or not found, return None
    if category_data.empty:
        return None

    # Drop the 'CPI Item' column to leave only the year columns
    category_data = category_data.drop(columns=['Consumer Price Index item'])

    # Transpose the data so that years become the index and we have one column with the annual changes
    category_data = category_data.T
    category_data.columns = ['Annual Change (%)']

    category_data = category_data.filter(regex='^\\d{4}$', axis=0)

    # Convert the index to a datetime index
    category_data.index = pd.to_datetime(category_data.index, format='%Y')

    # Extract the year from the datetime index for comparison
    category_data['Year'] = category_data.index.year

    # Filter the DataFrame for the specified year range if given
    if start_year is not None:
        category_data = category_data[category_data['Year'] >= start_year]
    if end_year is not None:
        category_data = category_data[category_data['Year'] <= end_year]

    # Drop the 'Year' column after filtering
    category_data = category_data.drop(columns=['Year'])

    # Ensure the index is set to datetime format (optional, based on further requirements)
    category_data.index = pd.to_datetime(category_data.index, format='%Y')
    category_data.index.freq = 'YS'
    
    return category_data


def check_stationarity(series):
    result = adfuller(series['Annual Change (%)'])
    p_value = result[1]
    return p_value < 0.05

def fit_arima(series, order=(1, 0, 1)):
    model = ARIMA(series, order=order)
    result = model.fit()
    return result

def fit_ets(series, trend='add', seasonal=None, damped_trend=True):
    model = ExponentialSmoothing(series, trend=trend, seasonal=seasonal, damped_trend=damped_trend)
    result = model.fit()
    return result

def forecast_and_evaluate(model, series, steps):
    forecast = model.forecast(steps=steps)
    actual = series.iloc[-steps:]
    mae = mean_absolute_error(actual, forecast)
    return forecast, mae

def plot_forecast(forecast, actual, category_name):
    plt.figure(figsize=(10, 6))
    plt.plot(actual.index, actual, label='Actual', marker='o')
    plt.plot(forecast.index, forecast, label='Forecast', marker='x')
    plt.title(f'Historical data and Forcast for {category_name}', loc='center')
    plt.xlabel('Year')
    plt.ylabel('Annual Change (%)')
    plt.legend()
    plt.savefig(rf'C:\Users\Caleb\Downloads\Figures\arima-{category_name}-forecast.png')
    plt.clf()

def ets_plot_forecast(forecast, actual, category_name):
    plt.figure(figsize=(10, 6))
    plt.plot(actual.index, actual, label='Actual', marker='o')
    plt.plot(forecast.index, forecast, label='Forecast', marker='x')
    plt.title(f'Historical data and Forcast for {category_name}', loc='center')
    plt.xlabel('Year')
    plt.ylabel('Annual Change (%)')
    plt.legend()
    plt.savefig(rf'C:\Users\Caleb\Downloads\Figures\ets-{category_name}-forecast.png')
    plt.clf()

# Main workflow
if __name__ == '__main__':
    # Load the historical CPI data
    filepath = r'C:\Users\Caleb\Downloads\historicalcpi (1).xlsx'
    header_row = 1  # Change this to the correct row number where your headers are (Python uses 0-based indexing)
    cpi_data = load_cpi_data(filepath, header_row=header_row)
    # Specify the start and end years based on your data
    start_year = int(1974)
    end_year = 2023  # Update this to your latest year

    if os.path.exists(rf'C:\Users\Caleb\Downloads\Figures\forecast.txt'):
        os.remove(rf'C:\Users\Caleb\Downloads\Figures\forecast.txt')

    # Specify the CPI categories to analyze
    cpi_categories = [
        "All food", "Food away from home", "Food at home", "Meats, poultry, and fish",
        "Meats", "Beef and veal", "Pork", "Other meats", "Poultry",
        "Fish and seafood", "Eggs", "Dairy products", "Fats and oils",
        "Fruits and vegetables", "Fresh fruits and vegetables", "Fresh fruits",
        "Fresh vegetables", "Processed fruits and vegetables", "Sugar and sweets",
        "Cereals and bakery products", "Nonalcoholic beverages", "Other foods"
    ]

    # Loop through each CPI category
    for category in cpi_categories:
        # For 'Processed fruits and vegetables', adjust the start year
        category_start_year = start_year if category != "Processed fruits and vegetables" else 1999
        
        series = prepare_cpi_series(cpi_data, category, start_year=category_start_year, end_year=end_year)
        
        if series is not None:
            # Proceed with ARIMA model fitting and evaluation using 'series'
            # Similar to the previous steps
            pass
        else:
            print(f"No data available for category: {category}")

        # Check for stationarity
        if check_stationarity(series):
            print(f'Series for {category} is stationary.')
        else:
            print(f'Series for {category} is not stationary. Consider differencing.')

        # Fit ARIMA model
        arima_result = fit_arima(series)
        print(arima_result.summary())

        # Forecast and evaluate ARIMA model
        forecast_steps = 10  # Change this to the number of steps you want to forecast
        arima_forecast, arima_mae = forecast_and_evaluate(arima_result, series, forecast_steps)
        #print(f'ARIMA MAE for {category}: {arima_mae}')
        with open(rf'C:\Users\Caleb\Downloads\Figures\forecast.txt', 'a') as f:
            f.write(f'ARIMA MAE for {category}: {arima_mae}\nThe ARIMA AIC of the model is: {arima_result.aic}\n')
        with open(rf'C:\Users\Caleb\Downloads\Figures\aforecast.txt', 'a') as f:
            f.write(f'{arima_forecast}\n')

        # Plot ARIMA forecast
        plot_forecast(arima_forecast, series, category)

        # Fit ETS model
        ets_result = fit_ets(series)
        print(ets_result.summary())

        # Forecast and evaluate ETS model
        ets_forecast, ets_mae = forecast_and_evaluate(ets_result, series, forecast_steps)
        #print(f'ETS MAE for {category}: {ets_mae}')
        with open(rf'C:\Users\Caleb\Downloads\Figures\forecast.txt', 'a') as f:
            f.write(f'ETS MAE for {category}: {ets_mae}\nThe ETS AIC of the model is: {ets_result.aic}\n')
        #print(ets_forecast)

        # Plot ETS forecast
        ets_plot_forecast(ets_forecast, series, category)
