// This #include statement was automatically added by the Particle IDE.
#include <LiquidCrystal.h>

// This #include statement was automatically added by the Particle IDE.
#include <ThingSpeak.h>

// This #include statement was automatically added by the Particle IDE.
#include <Grove-Ultrasonic-Ranger.h>

// This #include statement was automatically added by the Particle IDE.
//#include <HC_SR04.h>


LiquidCrystal lcd(5, 4, 3, 2, 1, 0);

TCPClient client;

unsigned long ThingSpeakChannelNum = 1736028;  ////////create your own thingspeakchannel and create a webhook in particle. 
///////https://docs.particle.io/tutorials/device-cloud/webhooks/#:~:text=create%20the%20webhook.-,Create%20the%20webhook,%22Webhook%22%20to%20get%20started.////


const char *APIWriteKey = "RVUPGLHPIMHDZFZ1";  /////This is the writekey in Thingspeak. Once the channel has benn created this can be found in API keys.


double inches = 0.0;
int LED = D7;
int repcount = 0; 
int led_counter = 1;




Ultrasonic ultrasonic(D8);


void setup() 
{
    
    // set up the LCD's number of columns and rows: 
    lcd.begin(16,2);
    // Print a message to the LCD.
    lcd.print("REDBACK OPS");
    
    
    
    ThingSpeak.begin(client);
   
    pinMode(LED, OUTPUT);
    digitalWrite(LED, LOW);
    
}

void loop() 
{
    double cm; 
    cm = ultrasonic.MeasureInCentimeters();

    if(cm> 5)
    {
        digitalWrite(LED, LOW);
        led_counter = 0;
        
        
    }
    else if(cm< 5 )
    {
        
        digitalWrite(LED, HIGH);
        
        if(led_counter == 0)
        {
            repcount = repcount +1;  
            Particle.publish("repcount", String(repcount), PRIVATE);
            
            ThingSpeak.setField(1, repcount);
            ThingSpeak.writeFields(ThingSpeakChannelNum, APIWriteKey);
            
            lcd.setCursor(0,1);
            lcd.print("Reps:");
            lcd.setCursor(14,1);
            lcd.print(repcount);
            
            delay(500);
            
        }
        else if(led_counter ==1)
        {
            repcount ==repcount;   
            
        }
        
        led_counter = 1;
        
    }


}


/*
Connect an HC-SR04 Range finder as follows:
Spark   HC-SR04
GND     GND
5V      VCC
D4      Trig
D5      Voltage divider output - see below

Echo --|
       >
       < 470 ohm resistor
       >
       ------ D5 on Spark
       >
       < 470 ohm resistor
       >
GND ---|

Test it using curl like this:
curl https://api.spark.io/v1/devices/<deviceid>/cm?access_token=<accesstoken>

The default usable rangefinder is 10cm to 250cm. Outside of that range -1 is returned as the distance.

You can change this range by supplying two extra parameters to the constructor of minCM and maxCM, like this:

HC_SR04 rangefinder = HC_SR04(trigPin, echoPin, 5.0, 300.0);

*/


    


