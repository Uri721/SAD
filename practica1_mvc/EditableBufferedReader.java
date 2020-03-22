package practica1;

import java.io.*;
import java.util.ArrayList;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * @author Uri
 */

public class EditableBufferedReader extends BufferedReader{

    private final int INT_ENTER = 13;
    private final int INT_ESC = 27;
    private final int INT_BACKSPACE = 127;
    private final int INT_INS = 300;
    private final int INT_DELETE = 301;
    private final int INT_UP = 302;
    private final int INT_DOWN = 303;
    private final int INT_RIGHT = 304;
    private final int INT_LEFT = 305;
    private final int INT_END = 306;
    private final int INT_HOME = 307;

    private final int T_RIGHT = 0;
    private final int T_LEFT = 1;
    private final int T_HOME = 2;
    private final int T_END = 3;

    private Line line;
    private int intInput;
    public Console console;

    public EditableBufferedReader(final InputStreamReader in) {
        super(in);
        this.line = new Line();
        this.console= new Console(line);
        line.addObserver(console);
    }

    // Characters buffered internally until carriage return
    public void setRaw() {

        final String[] command = { "/bin/sh", "-c", "stty -echo raw </dev/tty" };
        try {
            Runtime.getRuntime().exec(command).waitFor();
        } catch (final Exception e) {
            Logger.getLogger(EditableBufferedReader.class.getName()).log(Level.SEVERE, null, e);
        }
    }

    // Characters not processed by the terminal driver
    public void unsetRaw() {

        final String[] command = { "/bin/sh", "-c", "stty sane </dev/tty" };
        try {
            Runtime.getRuntime().exec(command).waitFor();
        } catch (final Exception e) {
            Logger.getLogger(EditableBufferedReader.class.getName()).log(Level.SEVERE, null, e);
        }
    }

    @Override
    public int read() throws IOException {

        this.intInput = super.read();

        while (super.ready()) {

            this.intInput = super.read();

            switch (this.intInput) {
                case 50:
                   // System.out.println("INS");
                    return this.INT_INS;
                case 51:
                   // System.out.println("DELETE");
                    return this.INT_DELETE;
                case 65:
                  //  System.out.println("UP");
                    return this.INT_UP;
                case 66:
                   // System.out.println("DOWN");
                    return this.INT_DOWN;
                case 67:
                   // System.out.println("RIGHT");
                    return this.INT_RIGHT;
                case 68:
                   // System.out.println("LEFT");
                    return this.INT_LEFT;
                case 70:
                   // System.out.println("END");
                    return this.INT_END;
                case 72:
                   // System.out.println("HOME");
                    return this.INT_HOME;
            }
        }
        return this.intInput;
    }

    @Override
    public String readLine() throws IOException {

        int readInt = 0;

        while(readInt != this.INT_ENTER){
            
            this.setRaw();
            readInt = this.read();
            this.unsetRaw();

            switch(readInt) {
                case INT_ENTER:
                    break;
                case INT_ESC:
                    break;
                case INT_INS: 
                    this.line.switchInsMode();
                    //console.insert(true);
                    break;
                case INT_DELETE:
                    this.line.delete(true);
                    //console.supr();
                    break;
                case INT_BACKSPACE:
                    this.line.delete(false);
                    //console.backspace();
                    break;
                case INT_RIGHT:
                    this.line.setTargetPos(this.T_RIGHT);
                    //console.right();
                    break;
                case INT_LEFT:
                    this.line.setTargetPos(this.T_LEFT);
                    //console.left();
                    break;
                case INT_END:
                    this.line.setTargetPos(this.T_END);
                    //String fin = "" + (line.getTargetPos()+1);
                    //console.fin(fin);
                    break;
                case INT_HOME:
                    this.line.setTargetPos(this.T_HOME);
                    //console.inicio();
                    break;
                default:
                    this.line.updateBuffer(readInt);
                    //String lletra = ""+(char)readInt;
                    //console.imprimir(lletra);
                    break;
            }
        }
        System.out.print('\n'+"Data:");
        return this.line.getData();

    }
}
