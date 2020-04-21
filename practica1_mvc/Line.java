import java.util.ArrayList;
import java.util.Observable;

public class Line extends Observable {

    private final int PRT_ID = 0;   // Print command ID
    private final int DEL_ID = 1;   // Delete command ID
    private final int BCK_ID = 2;   // Backspace command ID
    private final int TRG_ID = 3;   // Target command ID
    private final int INS_ID = 4;   // Insert command ID
    private final int RST_ID = 5;   // Reprint command ID
    private final int CLC_ID = 6;   // Reprint command ID

    private final int T_RIGHT = 0;          // Target right from target position
    private final int T_LEFT = 1;           // Target left from target position
    private final int T_UP = 2;             // Target up from target position
    private final int T_DOWN = 3;           // Target down from target position
    private final int T_HOME = 4;           // Target start of line
    private final int T_END = 5;            // Target end of line

    private final ArrayList<ArrayList<Integer>> buffer;  // Input data memory

    private Console console;                    // Line console view
    private int lineT;                          // Buffer pointing position [ Line ]
    private int columnT;                        // Buffer pointing position [ Column ]
    private boolean inputMode;                  // Input mode state [ True: Insert Mode - False: OW Mode ]
    private String aux;

    public Line() {
        
        this.buffer = new ArrayList<ArrayList<Integer>>();
        this.buffer.add(new ArrayList<Integer>());
        this.lineT = 0;
        this.columnT = 0;
        this.inputMode = false;
        this.console= new Console(this);
        this.addObserver(console);
    }

    // Adds to buffer processed input data
    public void updateBuffer(final int input) {

        // Check for null pointers on buffer line
        if(this.buffer.get(lineT).isEmpty() || this.columnT == this.buffer.get(lineT).size()) 
            this.buffer.get(lineT).add(input);
        
        else {    
            if(this.inputMode)   // Insert mode
                this.buffer.get(lineT).add(columnT, input);
            else            // Overwrite mode
                this.buffer.get(lineT).set(columnT, input);
        }
        this.aux = Character.toString((char)input);
        this.setChanged();
        this.notifyObservers(Integer.toString(this.PRT_ID) + aux);  // Print notification
        this.columnT++;   // Increase one unit column target position
        this.setChanged();
        this.notifyObservers(Integer.toString(this.TRG_ID) + this.intConversion(lineT) + this.intConversion(columnT));  // Target notification
    }

    // Deletes data on given target
    public void delete(final boolean currentTarget) {
        
        if(currentTarget) {
            this.setChanged();
            this.notifyObservers(Integer.toString(this.DEL_ID));
        } else {
            this.setChanged();
            this.notifyObservers(Integer.toString(this.BCK_ID));
        }

        // Check if there is buffer data to delete 
        if((!this.buffer.get(lineT).isEmpty())) {
            if(!currentTarget && this.columnT > 0) // Deletes data on left from current target position
                this.buffer.get(lineT).remove(columnT - 1);
            else                                     // Deletes data on current target position
                this.buffer.get(lineT).remove(columnT);

                if(this.columnT > 0)
                this.columnT--;   // Decrease one unit target column position
        }

        // Check for empty line
        if(this.buffer.get(lineT).isEmpty() && this.buffer.size() > 1) { 
            this.buffer.remove(lineT);  // Remove empty line
            this.lineT--;           // Decrease one unit target line position
            this.columnT = this.buffer.get(lineT).size(); // Set target to last position
            this.aux = this.intConversion(lineT) + this.intConversion(this.buffer.get(lineT).size());   // Set target position
            this.setChanged();
            this.notifyObservers(Integer.toString(this.RST_ID) + this.aux + this.getData());
        }
    }

    // Switches to the other input mode from current mode
    public void switchInsMode() {
        this.inputMode = !this.inputMode;

        if(this.inputMode) {
            this.setChanged();
            this.notifyObservers(Integer.toString(this.INS_ID) + "T");
        } else {
            this.setChanged();
            this.notifyObservers(Integer.toString(this.INS_ID) + "F");
        }
    }

    // Sets target position to the given position
    public void setTargetPos(final int target) {
        
        switch(target){
            // Set target position right from current position
            case T_RIGHT:
                if(this.columnT < this.buffer.get(lineT).size()) { // Check if position exists
                    this.columnT++;
                    this.setChanged();
                    this.notifyObservers(Integer.toString(this.TRG_ID) + this.intConversion(lineT) + this.intConversion(columnT));  // Target notification
                }
                break;
            // Set target position left from current position
            case T_LEFT:
                if(this.columnT > 0) {  // Check if position exists
                    this.columnT--;
                    this.setChanged();
                    this.notifyObservers(Integer.toString(this.TRG_ID) + this.intConversion(lineT) + this.intConversion(columnT));  // Target notification
                }
                break;
            // Set target position up from current position
            case T_UP:
                if(this.lineT > 0) {  // Check if position exists
                    this.lineT--;
                    if(this.columnT > this.buffer.get(lineT).size()) // Check for correct positioning
                        this.columnT = this.buffer.get(lineT).size();
                    this.setChanged();
                    this.notifyObservers(Integer.toString(this.TRG_ID) + this.intConversion(lineT) + this.intConversion(columnT));  // Target notification
                }
                break;
            // Set target position down from current position
            case T_DOWN:
                if(this.lineT < this.buffer.size() - 1) {  // Check if position exists
                    this.lineT++;
                    if(this.columnT > this.buffer.get(lineT).size()) // Check for correct positioning
                        this.columnT = this.buffer.get(lineT).size();
                    this.setChanged();
                    this.notifyObservers(Integer.toString(this.TRG_ID) + this.intConversion(lineT) + this.intConversion(columnT));  // Target notification
                }
                break;
            // Set target position to first position
            case T_HOME:
                this.columnT = 0;
                this.setChanged();
                this.notifyObservers(Integer.toString(this.TRG_ID) + this.intConversion(lineT) + this.intConversion(columnT));  // Target notification
                break;
            // Set target position to last position
            case T_END:
                this.columnT = this.buffer.get(lineT).size();
                this.setChanged();
                this.notifyObservers(Integer.toString(this.TRG_ID) + this.intConversion(lineT) + this.intConversion(columnT));  // Target notification
                break;
            default:
                System.out.println("Invalid target position");
                break;
        }
    }

    // Creates a new line in the buffer
    public void newBufLine() {
        this.buffer.add(new ArrayList<Integer>());
        this.columnT = 0;
        this.lineT++;
        this.setChanged();
        this.notifyObservers(Integer.toString(this.TRG_ID) + this.intConversion(lineT) + this.intConversion(columnT));  // Target notification
    }

    // Finishes processing line and resets the line
    public void finish() {
        System.out.println();
        System.out.println("Line processed");
        System.out.println("Reseting line...");
        try{ Thread.sleep(5000); } catch(Exception e) { System.out.println("Thread exception"); }
        this.buffer.clear();
        this.buffer.add(new ArrayList<Integer>());
        this.lineT = 0;
        this.columnT = 0;
        this.inputMode = false;
        this.setChanged();
        this.notifyObservers(Integer.toString(this.CLC_ID));
    }

    // Converts integer to string 3 digits format
    public String intConversion(int i) {

        if(i < 10)
            return "00" + Integer.toString(i);
        else if(i < 100)
            return "0" + Integer.toString(i);
        else
            return Integer.toString(i);
    }

    // Returns data buffer lines in string format to print
    public String getData() {
        
        String str = new String();
        int aux;

        for(int i = 0; i < this.buffer.size(); i++) {
            for(int k = 0; k < this.buffer.get(i).size(); k++) {
                aux = this.buffer.get(i).get(k);
                str = str + Character.toString((char)aux);
            }
            str = str + "\n";
        }
        return str;
    }
}
