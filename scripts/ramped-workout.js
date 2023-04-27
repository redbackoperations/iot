function startRampedWorkout(totalDuration, rampDuration, sets) {
    console.log('Ramped workout started. Total duration: ' + totalDuration / 60 + ' minutes.');
  
    // Calculate the duration of each set
    const setDuration = (totalDuration - rampDuration) / (sets - 1);
  
    // Set the start time
    const startTime = new Date().getTime();
  
    // Calculate the end time of each set
    const endTimes = [];
    for (let i = 0; i < sets; i++) {
      endTimes.push(startTime + rampDuration * 1000 + setDuration * i * 1000);
    }
  
    // Start the ramp-up period
    console.log('Ramp-up period started. Duration: ' + rampDuration + ' seconds.');
    const rampInterval = setInterval(() => {
      // Calculate the remaining ramp-up time
      const currentTime = new Date().getTime();
      const remainingRampTime = Math.round((endTimes[0] - currentTime) / 1000);
  
      // If the ramp-up period is over, start the sets
      if (remainingRampTime <= 0) {
        clearInterval(rampInterval);
        console.log('Ramp-up period finished. Starting sets.');
        startSets();
        return;
      }
  
      console.log('Ramp-up period: ' + remainingRampTime + ' seconds remaining.');
    }, 1000); // Update the timer every second (1000ms)
  
    // Start the sets
    function startSets() {
      let currentSet = 1;
      console.log(`Set ${currentSet} started. Duration: ${setDuration} seconds.`);
  
      // Start the timer for the current set
      const setInterval = setInterval(() => {
        // Calculate the remaining set time
        const currentTime = new Date().getTime();
        const remainingSetTime = Math.round((endTimes[currentSet] - currentTime) / 1000);
  
        // If the current set is over, start the next set or stop the workout
        if (remainingSetTime <= 0) {
          clearInterval(setInterval);
          if (currentSet === sets - 1) {
            console.log('Workout finished!');
            return;
          } else {
            currentSet++;
            console.log(`Set ${currentSet} started. Duration: ${setDuration} seconds.`);
            setInterval();
            return;
          }
        }
  
        console.log(`Set ${currentSet}: ${remainingSetTime} seconds remaining.`);
      }, 1000); // Update the timer every second (1000ms)
    }
  }
  