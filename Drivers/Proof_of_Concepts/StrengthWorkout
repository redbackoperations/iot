using System;
using System.Threading;

class Program
{
    static void Main(string[] args)
    {
        Console.WriteLine("Welcome to the Strength Workout!");

        int duration = 0;
        bool validDuration = false;

        // loop until user enters a valid duration
        while (!validDuration)
        {
            Console.WriteLine("Please enter the duration of your workout in minutes (maximum 20 minutes): ");
            duration = Convert.ToInt32(Console.ReadLine());

            // validate workout duration is between 1 and 20 minutes
            if (duration >= 1 && duration <= 20)
            {
                validDuration = true;
            }
            else
            {
                Console.WriteLine("Invalid duration. Please enter a duration between 1 and 20 minutes.");
            }
        }

        // Set up a flag for termination
        bool terminate = false;

        // Start a separate thread to listen for termination key
        Thread terminationThread = new Thread(() =>
        {
            while (true)
            {
                // Read a key from the console input
                ConsoleKeyInfo key = Console.ReadKey();

                // Check if the key is the termination key (e.g., 'T' key)
                if (key.KeyChar == 'T' || key.KeyChar == 't')
                {
                    terminate = true;
                    break;
                }
            }
        });

        terminationThread.Start();

        while (true)
        {
            // Check if the termination flag is set
            if (terminate)
            {
                Console.WriteLine("Workout terminated by user.");
                break;
            }

            Console.WriteLine("Please enter your desired resistance level (1-20): ");
            int resistance = Convert.ToInt32(Console.ReadLine());

            // limit resistance to 20
            resistance = Math.Min(resistance, 20);

            Console.WriteLine("Please enter your desired incline or decline level (0 to 20): ");
            int incline = Convert.ToInt32(Console.ReadLine());

            // limit incline and decline to -10 to 10
            incline = Math.Max(Math.Min(incline, 20), 0);

            Console.WriteLine("Get ready to start your workout!");

            for (int i = 0; i < duration * 60; i++)
            {
                // Check if the termination flag is set
                if (terminate)
                {
                    Console.WriteLine("Workout terminated by user.");
                    break;
                }

                Console.WriteLine($"Time remaining: {duration * 60 - i} seconds");
                Console.WriteLine("Press T anytime to terminate the workout");
                // allow the user to adjust resistance and incline during the workout
                if (i % 60 == 0)
                {
                    Console.WriteLine("You can adjust your resistance and incline level now.");
                    Console.WriteLine("Press '+' to increase resistance, '-' to decrease resistance, 'i' to increase incline, and 'd' to decrease incline.");

                    // read the user input
                    char userInput = Console.ReadKey().KeyChar;

                    // adjust resistance based on user input
                    if (userInput == '+')
                    {
                        resistance = Math.Min(resistance + 1, 20);
                        Console.WriteLine($"Resistance increased to {resistance}.");
                    }
                    else if (userInput == '-')
                    {
                        resistance = Math.Max(resistance - 1, 1);
                        Console.WriteLine($"Resistance decreased to {resistance}.");
                    }

                    // adjust incline based on user input
                    else if (userInput == 'i')
                    {
                        incline = Math.Min(incline + 1, 10);
                        Console.WriteLine($"Incline increased to {incline}.");
                    }
                    else if (userInput == 'd')
                    {
                        incline = Math.Max(incline - 1, -10);
                        Console.WriteLine($"Incline decreased to {incline}.");
                    }
                }
                Thread.Sleep(1000);
            }

            // Check if the termination flag is set
            if (terminate)
            {
                Console.WriteLine("Workout terminated by user.");
                break;
            }

            Console.WriteLine("Workout complete! Would you like to start another workout? (y/n)");

            // read the user input
            char repeat = Console.ReadKey().KeyChar;

            if (repeat != 'y')
            {
                break;
            }
        }

        // Ensure that the termination thread is stopped
        terminationThread.Join();

        Console.WriteLine($"Summary...... Workout Time: {duration} minutes");
        Console.WriteLine("Thank you for using the Smart Bike!");
    }
}
