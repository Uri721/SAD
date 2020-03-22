package practica1;

import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.io.Reader;
import java.lang.Integer;
import java.util.ArrayList;
/**
 *
 * @author Uri
 */
public class Test {
        
    public static void main(final String[] args) throws Exception {

        noMVCTest();
    }

    public static void noMVCTest() throws Exception {
        
        EditableBufferedReader in = new EditableBufferedReader(new InputStreamReader(System.in));
        
        while(true) {
            System.out.println(in.readLine());
        }
    }
}
