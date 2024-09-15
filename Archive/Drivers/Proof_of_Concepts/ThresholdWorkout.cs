using System;
using System.Threading.Tasks;

class ThresholdWorkout {
    // Define the constants for the workout
    const int IntervalDuration = 20; // in seconds
    static int NumIntervals ;
    const int RestDuration = 15; // in seconds
    const int WarmupDuration = 20; // in seconds
    const int CooldownDuration = 10; // in seconds

    // Define the power output percentages for each part of the workout
    static int ThresholdPower;
    const double IntervalPowerPercentage = 0.90; // 90% of the threshold power
    const double RestPowerPercentage = 0.50; // 50% of the threshold power
    const double WarmupPowerPercentage = 0.30; // 30% of the threshold power
    const double CooldownPowerPercentage = 0.30; // 30% of the threshold power

    // Define a function to calculate the power output for a given time during the workout
    static int CalculatePowerOutput(int time) {
        if (time < WarmupDuration) {
            return (int)(ThresholdPower * WarmupPowerPercentage);
        } else if (time < WarmupDuration + NumIntervals * (IntervalDuration + RestDuration)) {
            int intervalIndex = (time - WarmupDuration) / (IntervalDuration + RestDuration);
            int intervalStartTime = WarmupDuration + intervalIndex * (IntervalDuration + RestDuration);
            int intervalElapsedTime = time - intervalStartTime;
            if (intervalElapsedTime < IntervalDuration) {
                return (int)(ThresholdPower * IntervalPowerPercentage);
            } else {
                return (int)(ThresholdPower * RestPowerPercentage);
            }
        } else {
            return (int)(ThresholdPower * CooldownPowerPercentage);
        }
    }

    // Define a function to simulate the workout
    static async Task SimulateWorkout() {
        Console.WriteLine("Starting workout...");
        await Task.Delay(2000); // Wait for 2 seconds before starting to simulate the workout

        int currentTime = 0;
        int TotalDuration = (NumIntervals * IntervalDuration) + (NumIntervals - 1) * RestDuration + WarmupDuration + CooldownDuration;

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
        // Take input from user about the threshold power
        Console.Write("Enter the threshold power (in watts): ");
        int.TryParse(Console.ReadLine(), out ThresholdPower);
        // Take input from user about number of intervals
        Console.Write("Please enter the number of intervals for the workout");
        int.TryParse(Console.ReadLine(), out NumIntervals );

        // Simulate the workout
        await SimulateWorkout();

        // Turn off the smart bike
        TurnOffBike();
    }
}
