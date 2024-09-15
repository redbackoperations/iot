#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
import paho.mqtt.client as mqtt
import json
import time
import base64
import hashlib
from datetime import datetime
from cryptography.fernet import Fernet

encryption_key = Fernet.generate_key()
cipher_suite = Fernet(encryption_key)

class MQTTDataFrameHandler:
    def __init__(self, broker_address, topic, max_retries=3, retry_interval=5):
        self.broker_address = broker_address
        self.topic = topic
        self.client = mqtt.Client()
        self.client.on_message = self._on_message
        self.data = None
        self.error = None
        self.max_retries = max_retries
        self.retry_interval = retry_interval

    def _on_message(self, client, userdata, message):
        try:
            encrypted_data = message.payload
            data_json = cipher_suite.decrypt(encrypted_data).decode('utf-8')
            self.data = pd.read_json(data_json)
            self.data['timestamp'] = time.time()
        except Exception as e:
            self.error = str(e)

    def encrypt_value(self, value):
        return cipher_suite.encrypt(str(value).encode('utf-8'))

    def decrypt_value(self, encrypted_value):
        return cipher_suite.decrypt(encrypted_value).decode('utf-8')

    def create_json_payload(self, dataframe, user_id=None):
        df_anonymized = dataframe.copy()

        if 'incline' in df_anonymized.columns:
            df_anonymized['incline'] = df_anonymized['incline'].apply(lambda x: self.encrypt_value(x) if x else x)

        if 'resistance' in df_anonymized.columns:
            df_anonymized['resistance'] = df_anonymized['resistance'].apply(lambda x: self.encrypt_value(x) if x else x)

        data_json = df_anonymized.to_json(orient='split')

        payload = {
            'timestamp': datetime.utcnow().isoformat(),
            'data': json.loads(data_json)
        }

        if user_id:
            payload['user_id'] = user_id

        return json.dumps(payload)

    def receive_data(self, timeout=10):
        retries = 0
        while retries < self.max_retries:
            try:
                self.client.connect(self.broker_address, 1883, 60)
                self.client.subscribe(self.topic)
                self.client.loop_start()
                start_time = time.time()
                while self.data is None and (time.time() - start_time) < timeout:
                    if self.error:
                        print(f"Error while receiving data: {self.error}")
                        break
                self.client.loop_stop()
                return self.data
            except Exception as e:
                print(f"Connection error: {e}. Retrying in {self.retry_interval} seconds...")
                retries += 1
                time.sleep(self.retry_interval)
        print("Max retries reached. Failed to receive data.")
        return None

    def send_data(self, df, user_id=None):
        retries = 0
        while retries < self.max_retries:
            try:
                json_payload = self.create_json_payload(df, user_id)
                self.client.connect(self.broker_address, 1883, 60)
                self.client.publish(self.topic, json_payload)
                self.client.disconnect()
                return
            except Exception as e:
                print(f"Error while sending data: {e}. Retrying in {self.retry_interval} seconds...")
                retries += 1
                time.sleep(self.retry_interval)
        print("Max retries reached. Failed to send data.")

def main():
    broker_address = "test.mosquitto.org"
    topic = "test/topic"

    handler = MQTTDataFrameHandler(broker_address, topic)

if __name__ == "__main__":
    main()


# In[ ]:




