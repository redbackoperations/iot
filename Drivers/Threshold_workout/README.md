# Description:
The goal of a threshold workout is to improve individual's anaerobic threshold, also known as lactate threshold.
This is the exercise intensity at which lactic acid starts to accumulate in the blood at a faster rate than it can be removed, leading to fatigue and a decrease in performance.
By training at or near this threshold, the user teach their body to become more efficient at processing lactic acid, thereby delaying the onset of fatigue

# How to Run:
- Kickr script (/iot/scripts/./start_kickr.sh) must be executed, and a successful connection between Pi and Kickr must be established for this device to work as intended.
- Navigate to iot/Drivers/Threshold_workout and execute the script via
  'python Threshold_workout.py a b c d', where: <br />
  a -> number of interval <br />
  b -> duration of each interval (in minutes) <br />
  c -> rest between each interval (in seconds) <br />
  d -> threshold power (in Watts)
- Successful connection will be demonstrated by the start of threshold workout countdown
- Upon finishing the workout, total distance travelled and total calories burnt will be displayed in the terminal
