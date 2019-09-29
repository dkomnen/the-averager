import pytest
from averager.averager import AveragerPlugin


def test_user_message():
    mock_message_data = {'client_msg_id': '429bef68-5354-4666-a4a9-f11559a7724f', 'suppress_notification': False,
                         'type': 'message', 'text': 'great', 'user': 'UNU9B2UHJ', 'team': 'TNWJRPTC7',
                         'user_team': 'TNWJRPTC7', 'source_team': 'TNWJRPTC7', 'channel': 'CNWV2DME2',
                         'event_ts': '1569760795.004100', 'ts': '1569760795.004100'}
    plg = AveragerPlugin()
    plg.process_message(mock_message_data)