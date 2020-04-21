package practica2;

import java.net.Socket;
import java.net.SocketAddress;
import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.io.PrintWriter;

public class MySocket {

    Socket mySocket;
    BufferedReader input;
    PrintWriter output;
    InputStreamReader reader;
    String nick;

    public MySocket(String host, int port) throws IOException { // Crea MySocket
        this.mySocket= new Socket(host,port);
        this.reader= new InputStreamReader(this.mySocket.getInputStream());
        this.input = new BufferedReader(this.reader);
        this.output = new PrintWriter(this.mySocket.getOutputStream());
    }

    public MySocket(Socket s) throws IOException {
        this.mySocket=s;
        this.reader= new InputStreamReader(this.mySocket.getInputStream());
        this.input = new BufferedReader(this.reader);
        this.output = new PrintWriter(this.mySocket.getOutputStream());
    }

    public Socket getSocket() {
        return this.mySocket;
    }

    public BufferedReader getInputStream() {
        return this.input;
    }

    public PrintWriter getOutputStream() {
        return this.output;
    }


    public String readLine() throws IOException {
        return this.input.readLine();
    }

    public void writeLine(String s) {
        this.output.write(s);
    }

    public void println(String s) {
        this.output.println(s);
    }

    public void close() throws IOException {
        mySocket.close();
        input.close();
        output.close();
    }

    public String getNick(){
        return nick;
    }

    public void setNick(String nick){
        this.nick=nick;
    }
}
