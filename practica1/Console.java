/**
 * @author Uri
 */

public class Console {

    private boolean inputMode;      // Input mode state [ True: Insert Mode - False: OW Mode ]

    public Console() {
        this.inputMode = false;
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
}
