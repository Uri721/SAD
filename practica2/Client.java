import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Client {

    private static final String REQUEST_ID = "$";

    private static MySocket socket;

    private static BufferedReader userInput;

    public static void main(String[] args) {

        socket = new MySocket(args[0], Integer.parseInt(args[1]));

        // Input Thread
        new Thread() {
            public void run() {

                String input = null;

                userInput = new BufferedReader(new InputStreamReader(System.in));

                try {
                    while ((input = userInput.readLine()) != null)
                        socket.sendMssg(input);
                } catch (IOException e) {
                    // e.printStackTrace();
                }

                System.out.println("\n>> Disconnected <<\n");
                socket.sendMssg(input);
                socket.close();
            }
        }.start();

        // Output Thread
        new Thread() {
            public void run() {

                String input = null;
                try {
                    while (!(input = socket.receiveMssg()).equals(null)) {

                        if (input.startsWith(REQUEST_ID))
                            System.out.println(input.substring(1));

                        else
                            System.out.println(input);

                    }
                } catch (NullPointerException e) {
                    // e.printStackTrace();
                }
                socket.close();
            }
        }.start();
    }
}