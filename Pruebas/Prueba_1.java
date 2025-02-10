public class EjemploPatterns {
    public static void main(String[] args) {
        // Variables
        String nombre = "Juan";
        int edad = 30;
        double salario = 2500.75;

        // Imprimir mensaje con printf
        System.out.printf("Nombre: %s | Edad: %d | Salario: %.2f%n", nombre, edad, salario);

        // Condicional
        if (edad > 18) {
            System.out.println("Mayor de edad");
        } else {
            System.out.println("Menor de edad");
        }

        // Bucle for
        for (int i = 0; i < 3; i++) {
            System.out.println("Contador: " + i);
        }

        // Comentarios
        // Este es un comentario de una sola línea
        /* Este es un comentario
           de multiples lineas */
    }
}
