// Define the threshold power (in watts)
const thresholdPower = 250;

// Define the duration of the intervals (in seconds)
const intervalDuration = 300;

// Define the number of intervals
const numIntervals = 5;

// Define the rest period between intervals (in seconds)
const restDuration = 60;

// Define the warm-up period (in seconds)
const warmupDuration = 600;

// Define the cool-down period (in seconds)
const cooldownDuration = 600;

// Define the total workout duration (in seconds)
const totalDuration = (numIntervals * intervalDuration) + ((numIntervals - 1) * restDuration) + warmupDuration + cooldownDuration;

// Define the power output for each interval (as a percentage of threshold power)
const intervalPower = 90;

// Define the power output for the rest period (as a percentage of threshold power)
const restPower = 50;

// Define the power output for the warm-up and cool-down periods (as a percentage of threshold power)
const warmupCoolDownPower = 60;

// Define a function to calculate the power output for each time interval
function calculatePowerOutput(currentTime) {
  let powerOutput;
  
  // Warm-up period
  if (currentTime < warmupDuration) {
    powerOutput = warmupCoolDownPower;
  }
  // Cool-down period
  else if (currentTime >= totalDuration - cooldownDuration) {
    powerOutput = warmupCoolDownPower;
  }
  // Intervals
  else {
    const intervalIndex = Math.floor((currentTime - warmupDuration) / (intervalDuration + restDuration));
    
    if (intervalIndex % 2 === 0) {
      powerOutput = intervalPower;
    } else {
      powerOutput = restPower;
    }
  }
  
  // Convert power output from a percentage of threshold power to watts
  powerOutput = thresholdPower * (powerOutput / 100);
  
  return powerOutput;
}

// Define a function to simulate the workout
function simulateWorkout() {
  // Set the initial time to zero
  let currentTime = 0;
  
  // Loop until the total duration of the workout is reached
  while (currentTime < totalDuration) {
    // Calculate the power output for the current time
    const powerOutput = calculatePowerOutput(currentTime);
    
    // Send the power output to the smart bike
    sendPowerOutputToBike(powerOutput);
    
    // Wait for one second before updating the current time
    await sleep(1000);
    
    // Update the current time
    currentTime += 1;
  }
  
  // Turn off the smart bike
  turnOffBike();
}

// Define a function to send the power output to the smart bike
function sendPowerOutputToBike(powerOutput) {
  // Send the power output to the smart bike
  // TODO: Implement this function
}

// Define a function to turn off the smart bike
function turnOffBike() {
  // Turn off the smart bike
  // TODO: Implement this function
}

// Define a function to pause execution for a given number of milliseconds
function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

// Call the simulateWorkout function to start the workout
simulateWorkout();
