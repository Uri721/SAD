package practica2;

import java.io.IOException;
import java.net.ServerSocket;
import java.net.Socket;

public class MyServerSocket {

    ServerSocket myServerSocket;
    int portNum;

    public MyServerSocket(int port) throws IOException {
        myServerSocket= new ServerSocket(port);
    }    

    public ServerSocket getSocket() {
        return this.myServerSocket;
    }


    public void close() throws IOException {
        myServerSocket.close();
    }

	public MySocket accept() throws IOException {
        Socket s= myServerSocket.accept();
        return new MySocket(s);
	}
}
