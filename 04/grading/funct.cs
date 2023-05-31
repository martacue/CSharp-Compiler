using System;

namespace Programa{
class Main {
    public static void main(){
        Funct<int, int> f = x => x * x;
        Console.writeLine(f(3));
    }
}
}