import unittest
from unittest.mock import patch

# Importar las funciones que se van a probar
from stream_consumer_upper import get_shard_iterator


class TestStreamConsumer(unittest.TestCase):

    @patch('stream_consumer_upper.kinesis_client')
    def test_get_shard_iterator(self, mock_kinesis_client):
        stream_name = 'bollinger_stream'
        shard_id = 'shardId-000000000000'
        expected_iterator = 'example_shard_iterator'

        mock_kinesis_client.get_shard_iterator.return_value = {
            'ShardIterator': expected_iterator}
        result = get_shard_iterator(stream_name, shard_id)

        self.assertEqual(result, expected_iterator)
        mock_kinesis_client.get_shard_iterator.assert_called_once_with(
            StreamName=stream_name,
            ShardId=shard_id,
            ShardIteratorType='TRIM_HORIZON'
        )


if __name__ == '__main__':
    unittest.main()
