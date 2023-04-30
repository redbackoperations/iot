from mqtt_client import MQTTClient
from FTP_class import FTP

# Create unit test for FTP class

def unit_test(foo):
    assert foo.duration == 0
    assert foo.ftp == 0
    

def main():
    foo = FTP()
    unit_test(foo)
    
if __name__ == "__main__" :
    main()