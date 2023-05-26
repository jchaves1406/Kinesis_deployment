import boto3
import json
import time
import yfinance as yf
from datetime import datetime


# Crear cliente para interactuar con el servicio Kinesis de AWS
kinesis_client = boto3.client('kinesis', region_name='us-east-1')


# Función para enviar datos al flujo de Kinesis
def send_data_to_stream(stock_data):
    kinesis_client.put_record(
        StreamName='bollinger_stream',
        Data=json.dumps(stock_data),
        PartitionKey='stock'
    )


# Función para generar datos de acciones a partir de un DataFrame
def generate_stock_data(symbol, df, index):
    date_time = df.index[index]
    current_value = df['Close'].values[index]
    high_price = df['High'].values[index]
    low_price = df['Low'].values[index]

    return {
        'Timestamp': str(date_time).split()[0],
        'Symbol': symbol,
        'Currency': 'USD',
        'Current_value': round(current_value, 3),
        'High_value': round(high_price, 3),
        'Low_value': round(low_price, 3),
    }


# Punto de entrada principal del programa
if __name__ == '__main__':
    symbol = "AMD"
    start_time = datetime(2021, 1, 1)
    end_time = datetime.now()
    df_amd = yf.download(symbol, start=start_time, end=end_time)
    index = 0
    while True:
        stock_data = generate_stock_data(symbol, df_amd, index)
        print(f"Enviando a Kinesis: {stock_data}")
        send_data_to_stream(stock_data)
        time.sleep(1.5)
        index += 1
