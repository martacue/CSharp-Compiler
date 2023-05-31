using System;

namespace Programa{
class A {
    private int num;
    public void bigMethod(){
        float p = 3.2;
        num = 3;
        Console.writeLine("Asignado num");
        Console.writeLine(num);
        int time = 20;
        if (time <= 18) {
            Console.writeLine("Good morning");
        }
        else {
            Console.writeLine("Good afternoon!");
        }
        while (num != 4 && time == 20) {
            Console.writeLine(num);
            num = num + 1;
        }
    }
}
class Main {
    public static void main(){
        A a = new A();
        a.bigMethod();
    }
}
}