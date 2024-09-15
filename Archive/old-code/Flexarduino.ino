#include <Wire.h>
#include <rgb_lcd.h>

int flexs = A0;
int data = 0;
int buzzer = 9;

rgb_lcd lcd;  // initialize LCD library

void setup() 
{
  Serial.begin(9600);
  pinMode(flexs, INPUT);

  pinMode(buzzer, OUTPUT);
  // initialize the LCD with 16 columns and 2 rows:
  lcd.begin(16, 2);
 
  // move cursor to upper left position (0, 0)
  lcd.setCursor(0, 0);
 
  // print text on the LCD
  lcd.print("Redback Posture");
 
 
  delay(1000);    // wait a second
}


void loop() 
{

  //lcd.setCursor(0, 1);  // move cursor to position (0, 1)

  lcd.setColor(GREEN);

  //char txt[] = "Posture detection system \0";
 
  //lcd.setCursor(0, 0);  // move cursor to second row
  //lcd.print(txt);       // print text array
  //delay(500);          // wait a second
 
  //while(txt[0] != '\0')
  //{
  //  byte i = 0;
  //  lcd.setCursor(0, 0);
  //  while(txt[i] != '\0') // shift the text array to the left by 1 position
  //  {
  //    lcd.write(txt[i]);  // print one character
  //    txt[i] = txt[i+1];  // shift the text array to the left
  //    i++;
  //  }
 
  //  lcd.write(' ');  // print a space
  //  delay(200);      // wait 200 milliseconds
  //}
 
  // print number of seconds since the lase reset
  //lcd.print( millis()/1000 );
 
  //delay(200);      // wait 200 milliseconds

  
  data = analogRead(flexs);
  Serial.println(data);
  

  //if(data > 280)
  //{
  //  Serial.println("Fix your posture");
  //}
  
  if(data< 140)
  {
    tone(buzzer, 50);
    lcd.clear();
    Serial.println("Fix Posture");
    lcd.setCursor(0,1);
    lcd.print("Fix Posture");
    
  }
  else
  {
    noTone(buzzer);
    //lcd.clear();
    lcd.setCursor(0,1);
    lcd.print("Nice Posture");
    lcd.print("Redback Posture");
  }
  delay(500);
  
}
