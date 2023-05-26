import boto3
import json
import time
import pandas as pd


# Crear cliente para interactuar con el servicio Kinesis de AWS
kinesis_client = boto3.client('kinesis', region_name='us-east-1')


# Función para obtener el iterador de fragmentos de un flujo de Kinesis
def get_shard_iterator(stream_name, shard_id):
    response = kinesis_client.get_shard_iterator(
        StreamName=stream_name,
        ShardId=shard_id,
        ShardIteratorType='TRIM_HORIZON'
    )
    return response['ShardIterator']


# Función para leer datos de un flujo de Kinesis usando el iterador
def read_data_from_stream(stream_name, shard_iterator):
    response = kinesis_client.get_records(
        ShardIterator=shard_iterator,
        Limit=1000
    )
    return response['Records'], response['NextShardIterator']


# Función para procesar los registros leídos del flujo de Kinesis
def process_records(records, values_nvda, values_amd, periods, dev_bands):
    for record in records:
        stock_data = json.loads(record['Data'])

        # Procesar datos de la acción NVDA
        if stock_data['Symbol'] == 'NVDA':
            current_value = stock_data['Current_value']

            values_nvda.append(current_value)
            values_nvda = values_nvda[-periods:]
            series_nvda = pd.Series(values_nvda)
            bollinger_bands(stock_data, series_nvda, periods, dev_bands)

        # Procesar datos de la acción AMD
        elif stock_data['Symbol'] == 'AMD':
            current_value = stock_data['Current_value']

            values_amd.append(current_value)
            values_amd = values_amd[-periods:]
            series_amd = pd.Series(values_amd)
            bollinger_bands(stock_data, series_amd, periods, dev_bands)


# Función para calcular las bandas de Bollinger
def bollinger_bands(stock_data, series_values, periods, dev_bands):
    current_value = stock_data['Current_value']
    symbol = stock_data['Symbol']
    movil_average = series_values.rolling(window=periods).mean()
    dev_movil = series_values.rolling(window=periods).std()
    lower_band = movil_average - (dev_movil * dev_bands)
    print(f'Symbol: {symbol}, Current_value: {round(current_value, 3)}, \
    Bollinger_lower_band: {round(lower_band.iloc[-1], 3)}')

    if current_value < lower_band.iloc[-1]:
        print(f'*** ALERT *** The value is below the range: '
              f'{lower_band.iloc[-1]} current value: {current_value}')


# Punto de entrada principal del programa
if __name__ == '__main__':
    stream_name = 'bollinger_stream'
    shard_id = 'shardId-000000000000'
    shard_iterator = get_shard_iterator(stream_name, shard_id)
    values_nvda, values_amd = [], []
    periods = 15
    dev_bands = 2

    # Bucle infinito para leer y procesar datos del flujo de Kinesis
    while True:
        records, next_shard_iterator = read_data_from_stream(
            stream_name,
            shard_iterator
        )
        process_records(records, values_nvda, values_amd, periods, dev_bands)
        shard_iterator = next_shard_iterator
