using System;

namespace Programa{
class Main {
    public static void main(){
    string name = "John";
    switch (name)
    {
        case "Peter":
            Console.writeLine("Name is Peter.");
            break;

        case "John":
            Console.writeLine("Name is John.");
            break;

        default:
            Console.writeLine("No match.");
            break;
    }
    }
}
}