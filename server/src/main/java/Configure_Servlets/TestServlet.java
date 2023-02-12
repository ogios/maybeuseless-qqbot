package Configure_Servlets;

import javax.servlet.ServletException;
import javax.servlet.ServletOutputStream;
import javax.servlet.annotation.WebServlet;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import java.io.File;
import java.io.FileInputStream;
import java.io.IOException;
import java.io.PrintWriter;
import java.net.FileNameMap;
import java.net.URLConnection;
import java.util.Enumeration;
import java.util.Random;


@WebServlet(value = "/test", loadOnStartup = 1)
public class TestServlet extends HttpServlet {

    TestWebSocket testWebSocket;

    public String  checkType(File file){
        FileNameMap fileNameMap = URLConnection.getFileNameMap();
        return fileNameMap.getContentTypeFor(file.getPath());
    }

    public void sendPic(HttpServletResponse resp, File file){
        ServletOutputStream outputStream = null;
        FileInputStream inputStream = null;
        resp.setContentType(checkType(file));
        resp.setHeader("FileName", file.getName());
        try {
            outputStream = resp.getOutputStream();
            inputStream = new FileInputStream(file);
            byte[] tmp = new byte[1024];
            int length = 0;
            int read;
            while (true){
                read = inputStream.read(tmp);
                if (read == -1){
                    break;
                }
                length += read;
                outputStream.write(tmp, 0, read);
            }
            resp.setContentLength(length);
            outputStream.flush();
            outputStream.close();
            inputStream.close();
        } catch (IOException e) {
            throw new RuntimeException(e);
        }
    }


    public String getRemoteHost(javax.servlet.http.HttpServletRequest request){
        String ip = request.getHeader("x-forwarded-for");
        if(ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)){
            ip = request.getHeader("Proxy-Client-IP");
        }
        if(ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)){
            ip = request.getHeader("WL-Proxy-Client-IP");
        }
        if(ip == null || ip.length() == 0 || "unknown".equalsIgnoreCase(ip)){
            ip = request.getRemoteAddr();
        }
        return ip.equals("0:0:0:0:0:0:0:1")?"127.0.0.1":ip;
    }


    @Override
    protected void doGet(HttpServletRequest req, HttpServletResponse resp) throws ServletException, IOException {
        String ipAddr = getRemoteHost(req);
        System.out.println("ipAddr = " + ipAddr);
        String ticket = req.getParameter("ticket");
        if (ticket != null && !ticket.equals("")){
            File file = testWebSocket.checkTicket(ticket);
            if (file != null){
                System.out.println("TICKET: OK");
                sendPic(resp, file);
            } else {
                System.out.println("TICKET: BAD");
            }
        } else {
            System.out.println("TICKET: BAD");
        }
    }

    @Override
    public void init() throws ServletException {
        super.init();
        testWebSocket = new TestWebSocket(8082);
        Thread th = new Thread(()->{
            testWebSocket.run();
        });
        th.setDaemon(true);
        th.start();
    }
}
