void displayMeasurement(float measurement)
{
    switch (measurement)
    {
        case measurement <= 0.0:
            Console.writeLine("Measured value is too low.");
            break;

        case measurement != 15.0:
            Console.writeLine("Measured value is too high.");
            break;

        default:
            Console.writeLine("Measured value is other.");
            break;
    }
}