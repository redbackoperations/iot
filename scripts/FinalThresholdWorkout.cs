using System;
using System.Threading.Tasks;

class ThresholdWorkout {
    // Define the constants for the workout
    const int IntervalDuration = 30; // in seconds
    const int NumIntervals = 2;
    const int RestDuration = 20; // in seconds
    const int WarmupDuration = 25; // in seconds
    const int CooldownDuration = 15; // in seconds

    // Define the power output for each part of the workout
    static int ThresholdPower;
    static int IntervalPower = 0; // initialize to 0
    const int RestPower = 100; // in watts
    const int WarmupPower = 45; // in watts
    const int CooldownPower = 55; // in watts

    // Define a function to calculate the power output for a given time during the workout
    static int CalculatePowerOutput(int time) {
        if (time < WarmupDuration) {
            return WarmupPower;
        } else if (time < WarmupDuration + NumIntervals * (IntervalDuration + RestDuration)) {
            int intervalIndex = (time - WarmupDuration) / (IntervalDuration + RestDuration);
            int intervalStartTime = WarmupDuration + intervalIndex * (IntervalDuration + RestDuration);
            int intervalElapsedTime = time - intervalStartTime;
            return (intervalElapsedTime < IntervalDuration) ? IntervalPower : RestPower;
        } else {
            return CooldownPower;
        }
    }

    // Define a function to simulate the workout
    static async Task SimulateWorkout() {
        Console.WriteLine("Starting workout...");
        await Task.Delay(2000); // Wait for 2 seconds before starting to simulate the workout

        int currentTime = 0;
        int TotalDuration = (NumIntervals * IntervalDuration) + (NumIntervals - 1) * RestDuration + WarmupDuration + CooldownDuration; // Declare TotalDuration before it is used

        while (currentTime < TotalDuration) {
            int powerOutput = CalculatePowerOutput(currentTime);
            Console.WriteLine($"Power output for time {currentTime} is {powerOutput}");

            await Task.Delay(1000); // Wait for 1 second
            currentTime += 1;
        }

        Console.WriteLine("Workout complete!");
    }

    // Define a function to turn off the smart bike
    static void TurnOffBike() {
        Console.WriteLine("Smart bike turned off.");
    }

    // Main function
    static async Task Main() {
        // Take input from user
        Console.Write("Enter the threshold power (in watts): ");
        ThresholdPower = int.Parse(Console.ReadLine());
        IntervalPower = ThresholdPower;

        // Simulate the workout
        await SimulateWorkout();

        // Turn off the smart bike
        TurnOffBike();
    }
}
