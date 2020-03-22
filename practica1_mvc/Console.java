package practica1;

import java.util.Observable;
import java.util.Observer;

public class Console implements Observer {

    public boolean insert;
    private Line line;

    public Console(Line l) { // Constructor
        insert = false;
        this.line=l;
    }

    /*public void right() {
        System.out.print("\033[C"); // Move cursor right
    }

    public void left() {
        System.out.print("\033[D"); // Move cursor left
    }

    public void insert(boolean ins) {
        insert = ins;
    }

    public void supr() {
        System.out.print("\033[P"); // Delete characters on current line
    }

    public void inicio() {
        System.out.print("\033[G"); // Move cursor to indicated column in current row.
    }

    public void fin(String linea) {
        System.out.print("\033[" + linea + "G");
    }

    public void backspace() {
        System.out.print("\b" + "\033[P");
    }

    public void imprimir(String impr) {
        if (insert)
            System.out.print(impr);
        else
            System.out.print("\033[4h" + impr + "\033[4l"); 
    }
*/
    @Override
    public void update(Observable o, Object arg) {
        if(o==line){
            System.out.print(arg);
        }

    }
}
