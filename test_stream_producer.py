import unittest
from unittest.mock import patch
import pandas as pd

# Importar las funciones que se van a probar
from stream_producer import send_data_to_stream, generate_stock_data


class TestStreamProducer(unittest.TestCase):

    @patch('stream_producer.kinesis_client')
    def test_send_data_to_stream(self, mock_kinesis_client):
        """
        Prueba unitaria para la función send_data_to_stream.
        Verifica si se llama correctamente al método put_record del
        objeto simulado de kinesis_client.
        """
        stock_data = {
            'Timestamp': '2023-05-24',
            'Symbol': 'AAPL',
            'Currency': 'USD',
            'Current_value': 150.0,
            'High_value': 155.0,
            'Low_value': 145.0
        }

        send_data_to_stream(stock_data)

        mock_kinesis_client.put_record.assert_called_once_with(
            StreamName='bollinger_stream',
            Data='{"Timestamp": "2023-05-24", '
            '"Symbol": "AAPL", '
            '"Currency": "USD", '
            '"Current_value": 150.0, '
            '"High_value": 155.0, '
            '"Low_value": 145.0}',
            PartitionKey='stock'
        )

    def test_generate_stock_data(self):
        """
        Prueba unitaria para la función generate_stock_data.
        Verifica si la salida de la función es igual al resultado esperado.
        """
        symbol = "AAPL"
        df = pd.DataFrame({
            'Date': pd.date_range('2023-05-24', periods=3),
            'Close': [150.0, 155.0, 145.0],
            'High': [152.0, 157.0, 147.0],
            'Low': [148.0, 153.0, 143.0]
        })
        df.set_index('Date', inplace=True)
        df.index = pd.to_datetime(df.index).date

        index = 1

        expected_result = {
            'Timestamp': '2023-05-25',
            'Symbol': 'AAPL',
            'Currency': 'USD',
            'Current_value': 155.0,
            'High_value': 157.0,
            'Low_value': 153.0,
        }

        result = generate_stock_data(symbol, df, index)

        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()
