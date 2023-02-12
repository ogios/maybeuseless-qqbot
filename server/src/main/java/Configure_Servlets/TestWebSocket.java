package Configure_Servlets;

import org.json.JSONObject;

import java.io.*;
import java.net.ServerSocket;
import java.net.Socket;
import java.net.SocketException;
import java.util.*;
//import org.json.


public class TestWebSocket {

    ServerSocket serverSocket;

//    private LinkedList<HashMap> mapList;
    private HashMap<String, HashMap<String, Object>> hashMap;

    String path;
    Random random = new Random();

    public File getPic(String path){
        File dir = new File(path);
        if (dir.exists()){
            if (dir.isDirectory()){
                File[] pics = dir.listFiles();
                if (pics != null) {
                    int pos = random.nextInt(0, pics.length);
                    return pics[pos];
                }
            }
        }
        return null;
    }

    public String  recvTicket(Socket socket) {
        InputStream inputStream = null;
        try {
            inputStream = socket.getInputStream();
            DataInputStream dataInputStream = new DataInputStream(new BufferedInputStream(inputStream));
            StringBuilder stringBuilder = new StringBuilder();
            byte[] tmp = new byte[1024];
            int read;
            while (true) {
                read = dataInputStream.read(tmp);
                if (read == -1) {
                    break;
                }
                stringBuilder.append(new String(tmp, 0, read));
            }
            String tickets = stringBuilder.toString();
            JSONObject jsonObject = new JSONObject(tickets);
            File pic = getPic(path);
            HashMap<String, Object> map = new HashMap<>();
            map.put("timeout", jsonObject.getLong("timeout"));
            map.put("filePath", pic.getPath());
            hashMap.put(jsonObject.getString("ticket"), map);
            return jsonObject.getString("ticket");
        } catch (IOException e) {
            e.printStackTrace();
            return "";
        }
    }

//    public static void main(String[] args) {
//        TestWebSocket testWebSocket = new TestWebSocket(8082);
//        testWebSocket.run();
//    }

    public int checkSystem() {
        String osname = System.getProperty("os.name").toLowerCase();
        if (osname.contains("linux")) {
            return 1;
        } else if (osname.contains("windows")) {
            return 2;
        } else {
            return 0;
        }
    }

    public TestWebSocket(int port) {
        switch (checkSystem()){
            case 1 -> path = "/root/resources/web/";
            case 2 -> path = "E:\\图片\\猫猫头";
        }
        try {
            serverSocket = new ServerSocket(port);
            hashMap = new HashMap<>();
            Thread th = new Thread(this::flushTicket);
            th.setDaemon(true);
            th.start();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }

    public void run(){
        while (true) {
            try {
                System.out.println("SOCKET is waiting for connection");
                Socket socket = serverSocket.accept();
                System.out.println("SOCKET connected");
                String ipAddr = new String(socket.getInetAddress().toString());
                System.out.println("ipAddr = " + ipAddr);
                String ticket = recvTicket(socket);
                if (!ticket.equals("")) {
                    long timeout = (long) hashMap.get(ticket).get("timeout");
                    String filePath = (String) hashMap.get(ticket).get("filePath");
                    System.out.println("ticket = " + ticket);
                    System.out.println("timeout = " + timeout);
                    System.out.println("filePath = " + filePath);
                }
                socket.close();
                Thread.sleep(100);
            } catch (InterruptedException | IOException e) {
                e.printStackTrace();
                return;
            }

        }
    }


    public File checkTicket(String ticket){
        if (hashMap.containsKey(ticket)){
            long timeout = (long) hashMap.get(ticket).get("timeout");
            if (timeout < System.currentTimeMillis()){
                hashMap.remove(ticket);
                return null;
            } else {
                String filePath = (String) hashMap.get(ticket).get("filePath");
                return new File(filePath);
            }
        } else {
            return null;
        }
    }

    private void flushTicket(){
        while (true){
            Set<Map.Entry<String, HashMap<String, Object>>> entrySet = hashMap.entrySet();
            Iterator<Map.Entry<String, HashMap<String, Object>>> iterator = entrySet.iterator();
            while (iterator.hasNext()){
                Map.Entry<String, HashMap<String, Object>> entry = iterator.next();
                long timeout = (long) entry.getValue().get("timeout");
                if (timeout < System.currentTimeMillis()){
                    iterator.remove();
                }
            }
            try {
                Thread.sleep(60000);
            } catch (InterruptedException e) {
                throw new RuntimeException(e);
            }
        }
    }

}
