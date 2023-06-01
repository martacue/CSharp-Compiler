using System;

namespace Programa{
class A {
    private int x;
}
class Main {
    public static void main(){
        A a = new A();
        a.getType();
        Console.writeLine("Obtenido tipo de a");
        a.memberwiseClone();
        Console.writeLine("Clonado a");
    }
}
}