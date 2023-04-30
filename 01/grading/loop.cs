int[] numbers = new int[] { 3, 14 };
int num = 0;
foreach (int item in numbers)
{
    item = num++;
}
int n = 0;
while (n <= 5)
{
    Console.write(n);
    n++;
}