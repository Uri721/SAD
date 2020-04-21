import java.io.*;
import java.util.logging.Level;
import java.util.logging.Logger;

/**
 * @author Uri
 */

public class EditableBufferedReader extends BufferedReader {

    private final int INT_S_EOF = 19;       // End of file idetification [ ctrl + s]
    private final int INT_ENTER = 13;       // Enter key identification
    private final int INT_ESC = 27;         // Escape key identification
    private final int INT_BACKSPACE = 127;  // Backspace key identification
    private final int INT_INS = 300;        // Insert key identification
    private final int INT_DELETE = 301;     // Delete key identification
    private final int INT_UP = 302;         // Up arrow key identification
    private final int INT_DOWN = 303;       // Down arrow key identification
    private final int INT_RIGHT = 304;      // Right arrow key identification
    private final int INT_LEFT = 305;       // Left arrow key identification
    private final int INT_END = 306;        // End key identification
    private final int INT_HOME = 307;       // Home key identification

    private final int T_RIGHT = 0;          // Target right from target position
    private final int T_LEFT = 1;           // Target left from target position
    private final int T_UP = 2;             // Target up from target position
    private final int T_DOWN = 3;           // Target down from target position
    private final int T_HOME = 4;           // Target start of line
    private final int T_END = 5;            // Target end of line

    private Line line;
    private int intInput;


    public EditableBufferedReader(final InputStreamReader in) {
        super(in);
        this.line = new Line();
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

    // Processes last user terminal input
    // Returns integer associated to the user key input on terminal
    @Override
    public int read() throws IOException {

        // Read and process input
        this.intInput = super.read();

        // Check for more input to process
        while (super.ready()) {

            this.intInput = super.read();

            switch (this.intInput) {
                case 50:
                    return this.INT_INS;
                case 51:
                    return this.INT_DELETE;
                case 65:
                    return this.INT_UP;
                case 66:
                    return this.INT_DOWN;  
                case 67:
                    return this.INT_RIGHT;
                case 68:
                    return this.INT_LEFT;
                case 70:
                    return this.INT_END;
                case 72:
                    return this.INT_HOME;
            }
        }
        return this.intInput;
    }

    // Processes user key input until [ ctrl + s ] or ESC
    // Returns processed data
    @Override
    public String readLine() throws IOException {

        int readInt = 0;

        while(readInt != this.INT_S_EOF && readInt != this.INT_ESC) {
            
            // Input process
            this.setRaw();
            readInt = this.read();
            this.unsetRaw();

            // Process data given the input
            switch(readInt) {
                case INT_S_EOF:
                    this.line.finish();
                    break;
                case INT_ESC:
                    this.line.finish();
                    break;
                case INT_ENTER:
                    this.line.newBufLine();
                    break;
                case INT_INS:
                    this.line.switchInsMode();
                    break;
                case INT_DELETE:
                    this.line.delete(true);
                    break;
                case INT_BACKSPACE:
                    this.line.delete(false);
                    break;
                case INT_RIGHT:
                    this.line.setTargetPos(this.T_RIGHT);
                    break;
                case INT_LEFT:
                    this.line.setTargetPos(this.T_LEFT);
                    break;
                case INT_END:
                    this.line.setTargetPos(this.T_END);
                    break;
                case INT_HOME:
                    this.line.setTargetPos(this.T_HOME);
                    break;
                case INT_UP:
                    this.line.setTargetPos(this.T_UP);
                    break;
                case INT_DOWN:
                    this.line.setTargetPos(this.T_DOWN);
                    break;    
                default:
                    this.line.updateBuffer(readInt);
                    break;
            }
        }
        return this.line.getData();
    }
}
