function startWorkout(duration) {
  console.log('Workout started. Duration: ' + duration / 60 + ' minutes.');

  // Set the start time
  const startTime = new Date().getTime();

  // Set the end time
  const endTime = startTime + duration * 1000;

  // Update the timer every second
  const timerInterval = setInterval(() => {
    // Calculate the remaining time
    const currentTime = new Date().getTime();
    const remainingTime = Math.round((endTime - currentTime) / 1000);

    // If the remaining time is less than or equal to 0, stop the timer
    if (remainingTime <= 0) {
      clearInterval(timerInterval);
      console.log('Workout finished!');
      return;
    }

    // Format the remaining time as minutes and seconds
    const minutes = Math.floor(remainingTime / 60);
    const seconds = remainingTime % 60;

    console.log(`${minutes}:${seconds.toString().padStart(2, '0')}`);
  }, 1000); // Update the timer every second (1000ms)
}
