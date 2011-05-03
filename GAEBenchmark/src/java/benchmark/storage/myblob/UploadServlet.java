/**
 * @author Yi Huang (Celia)
 */
package benchmark.storage.myblob;

import benchmark.storage.ActionStatus;
import benchmark.storage.PMF;
import java.io.IOException;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.jdo.PersistenceManager;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import com.google.appengine.api.datastore.Blob;
import com.google.appengine.api.memcache.MemcacheService;
import com.google.appengine.api.memcache.MemcacheServiceFactory;

/**
 */
public class UploadServlet extends HttpServlet {
    private static final Logger log = Logger.getLogger(UploadServlet.class.getName());
    private static final MemcacheService memcache;

    static {
        memcache = MemcacheServiceFactory.getMemcacheService("myblob-simulate");
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
        long t1 = System.currentTimeMillis();
        PersistenceManager pm = PMF.getManager();
        try {
            String name = InitServlet.getCachedObjName(request.getParameter("id"));
            byte[] obj = (byte[])memcache.get(name);
            long t2 = System.currentTimeMillis();
            Blob blob = new Blob(obj);
            pm.makePersistent(new MyBlobInfo(name, "text/plain", obj.length, blob));
            long t3 = System.currentTimeMillis();
            log.log(Level.INFO, "myblob upload {0} {1} {2} {3} {4} {5}", new Object[]{
                ActionStatus.SUCCESS, name, t3-t1, t3-t2, t1, t3
            });
        } finally {
            pm.close();
        }
        response.sendRedirect("/myblob");
    }
    
    /** 
     * Returns a short description of the servlet.
     * @return a String containing servlet description
     */
    @Override
    public String getServletInfo() {
        return "GAEBenchmark MyBlob SimUpload";
    }
}
