void setup() {
 Serial.begin(9600);
}

void loop() {
 // simply read the anolog signal from A0 pin and print it out to the Serial connection
 Serial.println(analogRead(A0));

 // TODO: delay 500 ms for now, subject to change later 
 delay(500);
}
