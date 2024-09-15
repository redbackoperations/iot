/* Module: Fake_Gas_Sensor
 *  
 * Generate fake O2, CO2 and airflow data representing a breathing pattern.
 * and publish the results through the serial port.
 */

// The number of milliseconds between publishing readings
#define PUBLISH_PERIOD 100
// The time the last reading was published
long lastPublished;

// The sensor takes 20 seconds (20000 ms) before beginning operation
#define CO2_WARM_UP_PERIOD 20000
bool isCO2Available;
long timeCO2Available;

// The times for each portion of the breathing cycle in ms
long inspirationEnd = 1666;
long expirationEnd = 5000;
// True values for O2, CO2 and airflow during inspiration and expiration
long inspiredO2 = 210000;
long expiredO2 = 150000;
long inspiredCO2 = 400;
long expiredCO2 = 52632;
long inspiredFlow = 18000;
long expiredFlow = 9000;

// setup - Initialise the hardware
// Params: None
// Returns: Nothring
// Get the serial port ready for communication
void setup() {
  Serial.begin(9600);
  // The program should begin publishing data straight away
  lastPublished = millis() - PUBLISH_PERIOD;
  // but the CO2 sensor will take some time to warm up
  isCO2Available = false;
  timeCO2Available = lastPublished + CO2_WARM_UP_PERIOD;
}

// loop - Generate and publish fake CO2 data
// Params: None
// Returns: Nothing
// The normal breathing pattern is 12-20 breaths per minute, and expired CO2 in the range 35-45 mmHg.
// As atmospheric pressure is usually 760 mmHg, the expected value in ppm will be 40/760*1000000 = 52631.5789474
// Inspired air has 0.04% CO2, or 400 ppm.
//
// For this simulation, assume the breathing pattern uses 1/3 of the time for inspiration and 2/3 for expiration at 12 breaths per minute
// and CO2 transitions immediately from 0 to 52632. In reality there would be some measurement error, and the CO2 takes 20 seconds to reach 90% of the changed value
//
//
// CO2
//      |----------|     |----------|         52632 ppm
//      |          |     |          |
// _____|          |-----|          |-----    400 ppm
// 0    1.66       5     6.66       10    (seconds)
//
// For Oxygen, the inspired air contains 21% (210000 ppm), and expired air about 15% oxygen (150000 ppm)
// Again assume immediate transition between the values.
//
// O2
// -----|          |-----|          |-----  210000 ppm 
//      |          |     |          |
//      |----------|     |----------|       150000 ppm
// 0    1.66       5     6.66       10    (seconds)
//
// For Airflow, the normal resting ventilation is 500 ml.
// Using a triangular pattern, the airflow will be 500 ml/1.66 sec* 60 sec/min = 18000 mL/min during inspiration
// and -500/3.33*60 = -9000 ml/min during expiration
// Because the sensors don't read negative numbers, we will have two sensors set up,
// so during inspiration one will read +18000 and the other 0 ml/min,
// and during expiration one will read 0 ml/min and the other 9000 ml/min
//
// Airflow
// -----|          |-----|          |-----  18000 ml/min 
//      |          |     |          |
//      |----------|     |----------|       -9000 L/min
// 0    1.66       5     6.66       10    (seconds)
//
// Possible Extensions:
// For additional realism, monitor the response time (T90), noise in the sensor (possibly up to 2%) and quantization errors (ADC returns 0-1023) 
// Also add adjustments for the effects of temperature and pressure (currently 20C and 1 atmosphere assumed)
// Determine the maximum samping rate for each sensor and use that rather than 10Hz sampling
void loop() {
  long currentTime = millis();
  if ((currentTime - lastPublished) >= PUBLISH_PERIOD) {
    char buffer[128];

    // Flag that CO2 is available once the warm up period has elapsed
    if (!isCO2Available && ((currentTime - timeCO2Available) >= 0))
        isCO2Available = true;

    // Determine the period of time within the current breathing cycle
    long breathTime = currentTime % expirationEnd;

    if (isCO2Available) {
      if (breathTime < inspirationEnd) {
        snprintf(buffer, sizeof(buffer), "Time: %ld ms, O2: %ld ppm, CO2: %ld ppm, Inflow: %ld mL/min, Outflow: %ld mL/min", currentTime, inspiredO2, inspiredCO2, inspiredFlow, 0L);
      } else {
        snprintf(buffer, sizeof(buffer), "Time: %ld ms, O2: %ld ppm, CO2: %ld ppm, Inflow: %ld mL/min, Outflow: %ld mL/min", currentTime, expiredO2, expiredCO2, 0L, expiredFlow);
      }
    } else {
      if (breathTime < inspirationEnd) {
        snprintf(buffer, sizeof(buffer), "Time: %ld ms, O2: %ld ppm, CO2: -- ppm, Inflow: %ld mL/min, Outflow: %ld mL/min", currentTime, inspiredO2, inspiredFlow, 0L);
      } else {
        snprintf(buffer, sizeof(buffer), "Time: %ld ms, O2: %ld ppm, CO2: -- ppm, Inflow: %ld mL/min, Outflow: %ld mL/min", currentTime, expiredO2, 0L, expiredFlow);
      }
    }
    Serial.println(buffer);

    lastPublished = currentTime;
  }
}
