#!/usr/bin/env python
# coding: utf-8

# In[3]:


import pandas as pd
from datetime import datetime
from MQTTDataFrameHandler import MQTTDataFrameHandler  

def create_sample_dataframe():
    data = {
        'incline': [5.0, 6.5, 7.9],
        'resistance': [11.3, 11.5, 7.7]
    }
    return pd.DataFrame(data)

def main():
    broker_address = "test.mosquitto.org"
    topic = "test/topic"
    encryption_key = b'YourEncryptionKeyHere'  # Replace 'broker_address', 'topic', 'encryption_key' with the necessary configurations

    handler = MQTTDataFrameHandler(broker_address, topic, encryption_key=encryption_key)

    # Create sample data
    df = create_sample_dataframe()

    # Send data
    handler.send_data(df)

if __name__ == "__main__":
    main()


# In[ ]:





# In[2]:





# In[ ]:




