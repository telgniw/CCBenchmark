/**
 * @author Yi Huang (Celia)
 */
package benchmark.storage.myblob;

import benchmark.storage.ActionStatus;
import java.io.IOException;
import java.util.Random;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import com.google.appengine.api.memcache.Expiration;
import com.google.appengine.api.memcache.MemcacheService;
import com.google.appengine.api.memcache.MemcacheServiceFactory;

public class InitServlet extends HttpServlet {
    private static final MemcacheService memcache;

    static {
        memcache = MemcacheServiceFactory.getMemcacheService("myblob-simulate");
    }

    protected void HandleRequest(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        int num = Integer.parseInt(request.getParameter("num"));
        int size = Integer.parseInt(request.getParameter("size"));
        for(int i=0; i<num; i++) {
            String objName = getCachedObjName(String.valueOf(i));
            if(!memcache.contains(objName)) {
                byte[] blob = getRandomBlob(size);
                memcache.put(objName, blob, Expiration.byDeltaSeconds(86400));
            }
        }
        response.getWriter().format("myblob init %s NUM(%d) SIZE(%d)", new Object[]{
            ActionStatus.SUCCESS, num, size
        });
    }

    public static String getCachedObjName(String id) {
        return "SimBlob" + id;
    }
    
    /** 
     * Handles the HTTP <code>GET</code> method.
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    @Override
    protected void doGet(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        HandleRequest(request, response);
    }

    /**
     * Handles the HTTP <code>POST</code> method.
     * @param request servlet request
     * @param response servlet response
     * @throws ServletException if a servlet-specific error occurs
     * @throws IOException if an I/O error occurs
     */
    @Override
    protected void doPost(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        HandleRequest(request, response);
    }

    private byte[] getRandomBlob(int size) {
        byte[] obj = new byte[size];
        new Random().nextBytes(obj);
        return obj;
    }

    /** 
     * Returns a short description of the servlet.
     * @return a String containing servlet description
     */
    @Override
    public String getServletInfo() {
        return "GAEBenchmark MyBlob SimInit";
    }
}
