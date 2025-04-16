public class OtraClase {

    public static void metodoEstatico() {
        System.out.println("Metodo estatico");
    }

    public static void condicional() {
        
        int x = 15;
        int y = 18;

        if (x > 10) {
            System.out.println("x es mayor que 10");
        } else {
            System.out.println("x es menor o igual a 10");
        }

        if (y > 10) {
            System.out.println("x es mayor que 10");
        } else if (y == 10) {
            System.out.println("x es igual a 10");
        } else {
            System.out.println("x es menor que 10");
        }
    }

    public static void bucle() {
        
        int x = 0;

        while (x < 10) {
            x = x + 2;
            System.out.println(x);
        }
    }

    public static void bucle() {

        for (int i = 0; i < 3; i++) {
            System.out.println("Contador: " + i);
        }
    }

}