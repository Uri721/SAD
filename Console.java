package practica1;

public class Console {

    public boolean ins;

    public Console() { // Constructor
        ins = false;
    }

    public void right() {
        System.out.println("\033[C"); // Move cursor right
    }

    public void left() {
        System.out.println("\033[D"); // Move cursor left
    }

    public void insert(boolean ins) {
        insert = ins;
    }

    public void supr() {
        System.out.println("\033[P"); // Delete characters on current line
    }

    public void inicio() {
        System.out.println("\033[G"); // Move cursor to indicated column in current row.
    }

    public void fin(String linea) {
        System.out.println("\033[" + linea + "G");
    }

    public void backspace() {
        System.out.println("\b" + "\033[P");
    }

    public void imprimir(String impr) {
        if (insert)
            System.out.println(impr);
        else
            System.out.println("\033[4h" + impr + "\033[4l");
    }
}