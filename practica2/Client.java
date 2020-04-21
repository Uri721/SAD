package practica2;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;

public class Client {

    int portNum;
    String nick;

    public Client() {

    }

     public static void main(String[] args) throws NumberFormatException, IOException {
        MySocket sc = new MySocket(args[0], Integer.parseInt(args[1]));

        // input thread
        new Thread() {
            public void run() {
                String line;
                BufferedReader kbd = new BufferedReader(new InputStreamReader(System.in));
                try {
                    while ((line = kbd.readLine()) != null) {
                        sc.println(line);
                    }
                } catch (IOException e) {
                    // TODO Auto-generated catch block
                    e.printStackTrace();
                }
        }
    }.start();

    //output thread
    new Thread(){
        public void run(){
            String line;
            try {
                while ((line = sc.readLine()) != null) {
                    System.out.println(line);
                }
            } catch (IOException e) {
                // TODO Auto-generated catch block
                e.printStackTrace();
            }
        }
    }.start();
}
}
