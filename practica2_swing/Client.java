import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStreamReader;
import java.util.ArrayList;
import java.awt.*;
import java.awt.event.*;
import javax.swing.*;
import javax.swing.event.*;
import javax.swing.border.TitledBorder;

public class Client implements ActionListener {

    private static final String REQUEST_ID = "$";

    private static MySocket socket;

    private static BufferedReader userInput;

    private String name;

    JFrame frame;
    JTextField entry;
    JList<String> messages;
    JList<String> users;
    DefaultListModel<String> messagesModel;
    DefaultListModel<String> usersModel;
    JPanel out = new JPanel(new BorderLayout());
    JPanel inp = new JPanel(new BorderLayout());
    JPanel usr = new JPanel(new BorderLayout());
    JButton send;

    private String missat = "";
    private String state = "";

    public Client(String nick) {

        name = nick;
        frame = new JFrame(nick);

        // MESSAGES
        TitledBorder messagesBorder = new TitledBorder("Messages:");
        messagesModel = new DefaultListModel<>();
        messages = new JList<>(messagesModel);
        messages.setBorder(messagesBorder);
        JScrollPane messagesScrollPane = new JScrollPane(messages);
        out.add(messagesScrollPane);
        // USERS
        TitledBorder usersBorder = new TitledBorder("Users:");
        usersModel = new DefaultListModel<>();
        users = new JList<>(usersModel);
        users.setBorder(usersBorder);
        JScrollPane usersScrollPane = new JScrollPane(users);
        usr.add(usersScrollPane, BorderLayout.WEST);
        // ENTRY BUTTON TEXT FIELD
        inp.setLayout(new BoxLayout(inp, BoxLayout.LINE_AXIS)); // els widgets s afegiran horitzontalment d esquerra a
                                                                // dreta
        entry = new JTextField();
        send = new JButton("Send");
        entry.addActionListener(this);
        send.addActionListener(this);
        inp.add(entry);
        inp.add(send);

        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (Exception e) {
        }
        JFrame.setDefaultLookAndFeelDecorated(true);

        frame.addWindowListener(new java.awt.event.WindowAdapter() {
            public void windowClosing(WindowEvent winEvt) {
                state = "OFF";
            }
        });
        frame.add(out, BorderLayout.CENTER);
        frame.add(usr, BorderLayout.EAST);
        frame.add(inp, BorderLayout.PAGE_END);
        frame.setPreferredSize(new Dimension(500, 400));
        frame.pack();
        frame.setLocationRelativeTo(null);

    }

    public void actionPerformed(ActionEvent event) {
        Object source = event.getSource();
        String text = entry.getText();
        entry.setText("");
        missat = text;
        state = "ENVIANT";
    }

    public String getReceived() {
        return missat;
    }

    public String getName() {
        return this.name;
    }

    public void updateUserList(ArrayList<Client> cl) {
        usersModel.clear();
        for (int i = 0; i < cl.size(); i++) {
            usersModel.addElement(cl.get(i).getName());

        }
    }

    public void send(String m) {
        messagesModel.addElement(m);

    }

    public String getState() {
        return state;
    }

    public void setState(String a) {
        state = a;
    }

    public static void main(String[] args) {

        socket = new MySocket(args[0], Integer.parseInt(args[1])); // host port

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