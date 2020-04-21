import java.io.InputStreamReader;

/**
 * @author Uri
 */

public class Test {
        
    public static void main(final String[] args) throws Exception {

        EditableBufferedReader in = new EditableBufferedReader(new InputStreamReader(System.in));
        
        System.out.print("\033[H\033[2J");
        
        while(true)
            in.readLine();
    }
}
