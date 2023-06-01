using System;

namespace Programa{
class A {
    public void metodoa(){
        Console.writeLine("Metodo clase A");
    }
    public void metodoa2(){
        Console.writeLine("Metodo 2 clase A");
    }
}

class B : A {
    private string nombre = "b";
}

class C : B {
    private string nombre = "c";
}

class Main {
    public static void main(){
        B b = new B();
        b.metodoa();
        C c = new C();
        c.metodoa2();
    }
}
}