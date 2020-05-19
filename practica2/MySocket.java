import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;
import java.net.Socket;
import java.net.SocketAddress;

public class MySocket extends Socket {

    private Socket socket;

    private BufferedReader in;
    private PrintWriter out;

    public MySocket(String host, int port) {

        try {
            this.socket = new Socket(host, port);
            this.in = new BufferedReader(new InputStreamReader(this.socket.getInputStream()));
            this.out = new PrintWriter(this.socket.getOutputStream(), true);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public MySocket(Socket s) {

        try {
            this.socket = s;
            this.in = new BufferedReader(new InputStreamReader(this.socket.getInputStream()));
            this.out = new PrintWriter(this.socket.getOutputStream(), true);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void connect(SocketAddress endpoint) {
        try {
            this.socket.connect(endpoint);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public void close() {
        try {
            this.socket.close();
            this.in.close();
            this.out.close();
        } catch (IOException e) {
            // e.printStackTrace();
        }
    }

    public String receiveMssg() {
        try {
            return this.in.readLine();
        } catch (IOException e) {
            // e.printStackTrace();
        }
        return null;
    }

    public void sendMssg(String message) {

        this.out.print(message + "\n");
        this.out.flush();
    }
}