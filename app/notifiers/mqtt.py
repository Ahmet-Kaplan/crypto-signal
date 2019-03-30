import json
from time import sleep

import paho.mqtt.client as paho


class MqttNotifier:

    def __init__(self, **kwargs):
        self._host = kwargs['host']
        self._port = kwargs['port']

        self.client = paho.Client()
        if kwargs.get(
                'username') is not None and kwargs.get('password') is not None:
            self.client.username_pw_set(
                kwargs.get('username'), kwargs.get('password'))

    def connect(self):
        self.client.connect(self._host, self._port)
        self.client.loop_start()

    def notify(self, exchange, key, time_span, indicator, message):
        topic = '/%s/%s/%s/%s/' % (
            exchange, key, time_span, indicator)
        data = {
            'last_status': message['last_status']
        }
        for key in message['values']:
            self.client.publish(
                topic + '%s/' % key, message['values'][key], retain=True)
            data[key] = message['values'][key]
        self.client.publish(
            topic, json.dumps({'status': message['status']}), retain=True)

        self.client.publish(
            topic + 'attributes/', json.dumps(data), retain=True)

    def disconnect(self):
        while len(self.client._out_messages) != 0:
            print("sending")
            sleep(1)
        self.client.loop_stop()
        self.client.disconnect()
