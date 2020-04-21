import java.io.InputStreamReader;

/**
 * @author Uri
 */

public class Test {
        
    public static void main(final String[] args) throws Exception {

        EditableBufferedReader in = new EditableBufferedReader(new InputStreamReader(System.in));
        Console c = new Console();

        while(true)
                c.print(in.readLine());
    }
}
