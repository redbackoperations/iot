using System;
using System.Threading;

class WorkoutScript
{
    static void Main()
    {
        Console.WriteLine("Welcome to your workout!");
        Console.WriteLine("Press any key to start the timer.");

        // Wait for the user to start the timer
        Console.ReadKey();

        // Set the duration of the workout in seconds
        int duration = 300; // 5 minutes

        Console.WriteLine($"Workout started. Duration: {duration / 60} minutes.");

        // Start the timer
        for (int i = duration; i >= 0; i--)
        {
            Console.WriteLine($"{i / 60}:{i % 60:00}");
            Thread.Sleep(1000); // wait for 1 second
        }

        Console.WriteLine("Workout finished!");
    }
}
