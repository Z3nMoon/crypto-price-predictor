import streamlit as st
import pandas as pd
import requests
import time

# Initialize an empty DataFrame
predictions_df = pd.DataFrame(columns=['crypto', 'price', 'timestamp'])

@st.cache_data
def make_prediction():
    global predictions_df
    
    # Fetch current crypto prices (example using CoinGecko API)
    url = 'https://api.coingecko.com/api/v3/simple/price'
    params = {'ids': 'bitcoin,ethereum', 'vs_currencies': 'usd'}
    response = requests.get(url, params=params)
    data = response.json()
    
    # Create a new row for each crypto
    new_rows = []
    for crypto, price_data in data.items():
        new_row = {'crypto': crypto, 'price': price_data['usd'], 'timestamp': time.time()}
        new_rows.append(new_row)
    
    # Convert new rows to a DataFrame
    new_rows_df = pd.DataFrame(new_rows)
    
    # Concatenate new rows with existing DataFrame
    predictions_df = pd.concat([predictions_df, new_rows_df], ignore_index=True)
    
    # Log the updated DataFrame
    predictions_df.to_csv('crypto_prices.csv', index=False)
    
    return predictions_df

st.title("Crypto Price Predictor")

if st.button("Make Prediction"):
    predictions_df = make_prediction()

st.write(predictions_df)
