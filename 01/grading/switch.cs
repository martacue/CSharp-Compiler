void displayMeasurement(float measurement)
{
    switch (measurement)
    {
        case <= 0.0:
            Console.WriteLine("Measured value is too low.");
            break;

        case != 15.0:
            Console.WriteLine("Measured value is too high.");
            break;

        default:
            Console.WriteLine("Measured value is other.");
            break;
    }
}