import java.io.IOException;
import java.time.Instant;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class Server {

    static ConcurrentHashMap<String, Handler> clients = new ConcurrentHashMap<String, Handler>();

    public static ArrayList<Client> cl = new ArrayList<>();

    public static void main(final String args[]) throws NumberFormatException, IOException {

        final MyServerSocket ss = new MyServerSocket(Integer.parseInt(args[0]));

        System.out.println(Integer.parseInt(args[0]));

        ExecutorService pool = Executors.newFixedThreadPool(250);

        System.out.println("\n>> Server Initialized <<\n");

        while (true)
            pool.execute(new Handler(ss.accept()));
    }

    private static class Handler implements Runnable {

        private String username;
        private MySocket socket;
        Client c = new Client(this.username);
        private String rcv;

        private DateTimeFormatter instantFormatter = DateTimeFormatter.ofPattern("uuuu.MM.dd HH:mm:ss")
                .withZone(ZoneId.systemDefault());

        private Handler(MySocket s) {
            this.socket = s;
        }

        public void run() {

            this.clientInitialization();

            while (!c.getState().equals("OFF")) {
                System.out.print(c.getState());
                if (c.getState().equals("ENVIANT")) {
                    this.rcv = c.getReceived();

                    for (int i = 0; i < cl.size(); i++) {
                        cl.get(i).send(">> " + getTime() + " " + username + " : " + rcv);
                    }
                    c.setState("");
                }

            }

            clients.remove(this.username);
            Client cremove = new Client("");
            for (int i = 0; i < cl.size(); i++) {
                if (cl.get(i).getName().equals(this.username)) {
                    cremove = cl.get(i);
                }
            }
            cl.remove(cremove);
            for (int i = 0; i < cl.size(); i++) {
                cl.get(i).updateUserList(cl);
            }

            for (int i = 0; i < cl.size(); i++) {
                cl.get(i).send(">> " + getTime() + " " + username + " has left the chat <<");
            }
            System.out.println(username + " Has Abandoned The System - Users In The System: " + clients.size() + "\n");
            this.socket.close();

        }

        private void clientInitialization() {
            while (true) {

                this.socket.sendMssg("$Enter username:");

                if (!clients.containsKey(this.username = this.socket.receiveMssg())) {

                    clients.put(this.username, this);

                    c = new Client(this.username);
                    c.frame.setVisible(true);
                    cl.add(c);

                    for (int i = 0; i < cl.size(); i++) {
                        cl.get(i).updateUserList(cl);
                    }

                    for (Handler h : Server.clients.values())
                        if (!h.username.equals(this.username))

                            for (int i = 0; i < cl.size(); i++) {
                                cl.get(i).send(">> " + getTime() + "  " + username + " has joined the chat <<");
                            }
                    break;

                } else
                    this.socket.sendMssg(">> System Error: Name Already Taken");
            }

            this.socket.sendMssg(">> User " + this.getTime() + "  " + this.username + " Initialization Completed <<");
            System.out.println(this.username + " Is In The System\n");
        }

        private String getTime() {
            return instantFormatter.format(Instant.now()).substring(11);
        }
    }

}