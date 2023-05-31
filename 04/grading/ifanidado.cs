using System;

namespace Programa{
class Main {
    public static void main(){
        bool respondido = false;
        if (!respondido) {
            Console.writeLine("Paso 1");
            string texto1 = "hola";
            string texto2 = "hola";
            if (texto1 == texto2) {
               Console.writeLine("textos iguales"); 
            }
            else {
                Console.writeLine("textos distintos"); 
            }
        }
        else {
            Console.writeLine("finalizado");
        }
    }
}
}