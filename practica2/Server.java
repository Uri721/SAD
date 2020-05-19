import java.io.IOException;
import java.time.Instant;
import java.time.ZoneId;
import java.time.format.DateTimeFormatter;
import java.util.Map;
import java.util.concurrent.ConcurrentHashMap;
import java.util.concurrent.ExecutorService;
import java.util.concurrent.Executors;

public class Server {

    static ConcurrentHashMap<String, Handler> clients = new ConcurrentHashMap<String, Handler>();

    public static void main(final String args[]) throws NumberFormatException, IOException {

        final MyServerSocket ss = new MyServerSocket(Integer.parseInt(args[0]));

        System.out.println(Integer.parseInt(args[0]));

        ExecutorService pool = Executors.newFixedThreadPool(250);

        System.out.println("\n>> Server Initialized <<\n");

        // System.out.println(ss.getInetAddress().getLocalHost());

        while (true)
            pool.execute(new Handler(ss.accept()));
    }

    private static class Handler implements Runnable {

        private String username;
        private MySocket socket;

        private String rcv;

        private DateTimeFormatter instantFormatter = DateTimeFormatter.ofPattern("uuuu.MM.dd HH:mm:ss")
                .withZone(ZoneId.systemDefault());

        private Handler(MySocket s) {
            this.socket = s;
        }

        public void run() {

            this.clientInitialization();

            while ((this.rcv = this.socket.receiveMssg()) != null) {

                for (Handler h : Server.clients.values())
                    if (!h.username.equals(this.username))
                        h.socket.sendMssg(">> " + getTime() + " " + username + " : " + rcv);

            }

            clients.remove(this.username);

            for (Handler h : Server.clients.values())
                h.socket.sendMssg(">> " + getTime() + " " + username + " has left the chat <<");

            System.out.println(username + " Has Abandoned The System - Users In The System: " + clients.size() + "\n");
            this.socket.close();
        }

        private void clientInitialization() {

            while (true) {

                this.socket.sendMssg("$Enter username:");

                if (!clients.containsKey(this.username = this.socket.receiveMssg())) {

                    clients.put(this.username, this);
                    for (Handler h : Server.clients.values())
                        if (!h.username.equals(this.username))
                            h.socket.sendMssg(">> " + getTime() + "  " + username + " has joined the chat <<");
                    break;

                } else
                    this.socket.sendMssg(">> System Error: Name Already Taken");
            }
            this.socket.sendMssg(">> User " + this.getTime() + "  " + this.username + " Initialization Completed <<");
            System.out.println("\n" + this.username + " Is In The System\n");
        }

        private String getTime() {
            return instantFormatter.format(Instant.now()).substring(11);
        }
    }
}