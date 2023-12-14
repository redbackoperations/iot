#!/usr/bin/env python
# coding: utf-8

# In[4]:


import pandas as pd
from MQTTDataFrameHandler import MQTTDataFrameHandler 

def print_received_data(data):
    print("Received Data:")
    print(data)

def main():
    broker_address = "test.mosquitto.org"
    topic = "test/topic"
    encryption_key = b'YourEncryptionKeyHere'  

    handler = MQTTDataFrameHandler(broker_address, topic, encryption_key=encryption_key)

    # Receive data
    received_data = handler.receive_data()

    if received_data is not None:
        # Decrypt and print received data
        decrypted_data = received_data.copy()
        if 'incline' in decrypted_data.columns:
            decrypted_data['incline'] = decrypted_data['incline'].apply(handler.decrypt_value)
        if 'resistance' in decrypted_data.columns:
            decrypted_data['resistance'] = decrypted_data['resistance'].apply(handler.decrypt_value)

        print_received_data(decrypted_data)
    else:
        print("Failed to receive data.")

if __name__ == "__main__":
    main()


# In[ ]:





# In[2]:





# In[ ]:




