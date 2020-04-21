import java.util.Observable;
import java.util.Observer;

public class Console implements Observer {

    private final int PRT_ID = 0;   // Print command ID
    private final int DEL_ID = 1;   // Delete command ID
    private final int BCK_ID = 2;   // Backspace command ID
    private final int TRG_ID = 3;   // Target command ID
    private final int INS_ID = 4;   // Insert command ID
    private final int RST_ID = 5;   // Reprint command ID
    private final int CLC_ID = 6;   // Reprint command ID

    private boolean inputMode;      // Input mode state [ True: Insert Mode - False: OW Mode ]
    private Line line;
    private String aux;
    private int auxL;
    private int auxC;

    public Console(Line l) {
        this.inputMode = false;
        this.line = l;
    }

    // Set cursor target to specified line and column
    public void setTarget(int l, int c) {
        System.out.print("\033[" + Integer.toString(l + 1) + ";" + Integer.toString(c + 1) + "f");
    }

    // Set input mode
    public void insert(final boolean insert) {
        this.inputMode = insert;
    }

    // Delete data left from current position
    public void backspace() {
        System.out.print("\b\033[P");
    }

    // Delete data on current target position
    public void delete() {
        System.out.print("\033[P");
    }

    // Print data on terminal
    public void print(final String p) {
        if (this.inputMode)     // Insert mode
            System.out.print("\033[4h" + p + "\033[4l");
        else                    // Overwrite mode
            System.out.print(p);
    }

    // Reprint data on terminal
    public void reprint(final String p) {
        System.out.print("\033[H\033[2J");
        System.out.print(p);
    }

    // Clear data on terminal
    public void clear() {
        System.out.print("\033[H\033[2J");
    }

    @Override
    public void update(Observable obs, Object o) {
        
        aux = o.toString();

        if(this.line == obs)
            switch(Character.getNumericValue(aux.charAt(0))) {
                case PRT_ID:
                    this.print(aux.substring(1));
                    break;
                case DEL_ID:
                    this.delete();
                    break;
                case BCK_ID:
                    this.backspace();
                    break;
                case TRG_ID:
                    this.auxL = Integer.parseInt(aux.substring(1,4));
                    this.auxC = Integer.parseInt(aux.substring(4,7));
                    this.setTarget(this.auxL, this.auxC);
                    break;
                case INS_ID:
                    if(aux.charAt(1) == 'T')
                        this.insert(true);
                    else
                        this.insert(false);
                    break;
                case RST_ID:
                    this.auxL = Integer.parseInt(aux.substring(1,4));
                    this.auxC = Integer.parseInt(aux.substring(4,7));
                    this.reprint(aux.substring(7));
                    this.setTarget(this.auxL, this.auxC);
                    break;
                case CLC_ID:
                    this.clear();
                    break;
                default:
                    System.out.println("Invalid command");
                    break;
            }
    }
}
