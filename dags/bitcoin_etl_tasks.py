import json
import pandas as pd
import pandas_ta as ta
from airflow.providers.postgres.hooks.postgres import PostgresHook
from dags.alpha_vantage_utils import get_crypto_daily

def extract_bitcoin_data(**kwargs):
    """
    Extracts daily Bitcoin data from the Alpha Vantage API and saves it to a file.
    """
    print("Extracting Bitcoin data...")
    btc_data = get_crypto_daily('BTC', 'USD')
    daily_data = btc_data.get('Time Series (Digital Currency Daily)', {})

    if not daily_data:
        raise ValueError("No data found in the API response.")
    
    with open('/tmp/bitcoin_data.json', 'w') as f:
        json.dump(daily_data, f)
    print("Bitcoin data extracted and saved successfully.")

def transform_and_load_bitcoin_data(**kwargs):
    print("Transforming and loading Bitcoin data...")
    with open('/tmp/bitcoin_data.json', 'r') as f:
        data = json.load(f)

    df = pd.DataFrame.from_dict(data, orient='index', dtype=float)
    
    print("Original columns:", df.columns.tolist())

    column_mapping = {}
    for col in df.columns:
        if 'open' in col.lower():
            column_mapping[col] = 'open'
        elif 'high' in col.lower():
            column_mapping[col] = 'high'
        elif 'low' in col.lower():
            column_mapping[col] = 'low'
        elif 'close' in col.lower():
            column_mapping[col] = 'close'
        elif 'volume' in col.lower():
            column_mapping[col] = 'volume'
    
    df.rename(columns=column_mapping, inplace=True)
    print("Columns after renaming:", df.columns.tolist())
    
    df.index = pd.to_datetime(df.index)
    df.sort_index(inplace=True)

    available_ohlcv_cols = [col for col in ['open', 'high', 'low', 'close', 'volume'] if col in df.columns]
    print("Available OHLCV columns:", available_ohlcv_cols)
    df = df[available_ohlcv_cols]
    if 'close' in df.columns:
        df['adj_close'] = df['close']

    if all(col in df.columns for col in ['open', 'high', 'low', 'close', 'volume']):
        df.ta.sma(length=20, append=True)
        df.ta.ema(length=50, append=True)
        df.ta.rsi(length=14, append=True)
        df.ta.macd(fast=12, slow=26, signal=9, append=True)

        df.rename(columns={
            'SMA_20': 'sma_20',
            'EMA_50': 'ema_50',
            'RSI_14': 'rsi_14',
            'MACD_12_26_9': 'macd_12_26_9',
            'MACDh_12_26_9': 'macdh_12_26_9',
            'MACDs_12_26_9': 'macds_12_26_9'
        }, inplace=True)
    else:
        print("Warning: Not all OHLCV columns available for technical indicators")

    df.fillna(0, inplace=True)

    print("Loading data into PostgreSQL...")
    postgres_hook = PostgresHook(postgres_conn_id='postgres_default')
    engine = postgres_hook.get_sqlalchemy_engine()
    
    df.reset_index(inplace=True)
    df.rename(columns={'index': 'date'}, inplace=True)
    
    print("Final DataFrame columns:", df.columns.tolist())
    print("DataFrame shape:", df.shape)
    
    df.to_sql(
        name='bitcoin_metrics',
        con=engine,
        if_exists='append',
        index=False,
        method='multi'
    )
    
    print("Bitcoin data transformed and loaded successfully into PostgreSQL.")