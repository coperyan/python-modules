import os
import json
import requests

from config import CHANNELS

CHANNEL_LIST = list(CHANNELS.keys())


class MSTeamsMessage:
    def __init__(self, channel: str):
        self.channel = channel
        self._validate_channel()
        self.msg_url = CHANNELS.get(self.channel).get("url")
        self.msg_body = CHANNELS.get(self.channel).get("body")
        self.kwargs = None

    def _validate_channel(self):
        if self.channel not in CHANNEL_LIST:
            raise ValueError("Channel not in config.py!")

    def _build_msg_body(self, in_d: dict, kwargs: dict):
        for k, v in in_d.items():
            if isinstance(v, str):
                in_d[k] = v.format_map(kwargs)
            elif isinstance(v, dict):
                self._build_msg_body(v, kwargs)
            elif isinstance(v, list):
                for o in v:
                    if isinstance(o, dict):
                        self._build_msg_body(o, kwargs)

    def send(self, **kwargs):
        body = self.msg_body.copy()
        self._build_msg_body(body, kwargs)

        resp = requests.post(
            self.msg_url,
            headers={"Accept": "*/*", "Content-Type": "application/json"},
            json=body,
        )
        if resp.status_code != 200:
            print(resp.status_code)
            print("\n")
            print(body)
            print(resp.text)


test = MSTeamsMessage("DC3Analytics")
test.send(
    job_name="DC3Test",
    run_time="7/4/1776 12:00 AM",
    failure_time="12/1/1783 12:00 PM",
    run_time_min="10000",
    retries="5",
    step_num="99",
    step_name="Test",
    message="SELECT * FROM sys.tables;",
)
