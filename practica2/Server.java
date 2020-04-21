package practica2;

import java.io.IOException;
import java.net.Socket;
import java.util.HashMap;

public class Server {
    int portNum;
    static HashMap<String, Socket> clients = new HashMap<String, Socket>();

    public static void main(final String args[]) throws NumberFormatException, IOException {
        final MyServerSocket ss = new MyServerSocket(Integer.parseInt(args[0]));

        while (true) {
            final MySocket s = ss.accept();

            new Thread() {
                public void run() {
                    String nick;
                    
                    while (true) {
                        s.println("NICK: ");
                        try {
                            nick = s.readLine();
                            if (nick == null) {
                                return;
                            }
                            if (!clients.containsKey(nick)) {// afegeix clients
                                s.setNick(nick);
                                clients.put(nick,s.getSocket());
                                break;
                            }
                        } catch (IOException e) {
                            // TODO Auto-generated catch block
                            e.printStackTrace();
                        }
                    }

                                            
                        //escoltar missatges
                        while(true){
                            try {
                                String line = s.readLine();
                                if(line==null){//control+d sortir del xat
                                    return;
                                }
                                s.println("LINE: "+line);

                            } catch (IOException e) {
                                // TODO Auto-generated catch block
                                e.printStackTrace();
                            }
                            try {
                                s.close();
                            } catch (IOException e) {
                                // TODO Auto-generated catch block
                                e.printStackTrace();
                            }
                        }
                }
            }.start();
        }
    }
}
