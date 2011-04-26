/**
 * @author Yi Huang (Celia)
 */
package benchmark.storage.myblob;

import benchmark.storage.ActionStatus;
import benchmark.storage.PMF;
import java.io.IOException;
import java.util.List;
import java.util.logging.Level;
import java.util.logging.Logger;
import javax.jdo.Query;
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
public class DownloadServlet extends HttpServlet {
    private static final Logger log = Logger.getLogger(DownloadServlet.class.getName());
    private static final MemcacheService memcache;

    static {
        memcache = MemcacheServiceFactory.getMemcacheService("myblob-simulate");
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
        long t1 = System.currentTimeMillis();
        PersistenceManager pm = PMF.getManager();
        Query query = pm.newQuery(MyBlobInfo.class);
        try {
            String name = InitServlet.getCachedObjName(request.getParameter("id"));
            query.setFilter("name == blobName");
            query.declareParameters("String blobName");
            List<MyBlobInfo> list = (List<MyBlobInfo>) query.execute(name);
            MyBlobInfo blobInfo = list.get(0);
            long t2 = System.currentTimeMillis();
            Blob blob = blobInfo.getBlob();
            response.setStatus(HttpServletResponse.SC_FOUND);
            long t3 = System.currentTimeMillis();
            log.log(Level.INFO, "myblob download {0} {1} {2} {3}", new Object[]{
                ActionStatus.SUCCESS, name, t3-t1, t2-t1
            });
        } catch(ArrayIndexOutOfBoundsException e) {
            log.log(Level.INFO, "myblob download {0}", ActionStatus.FAILED);
            response.setStatus(HttpServletResponse.SC_NOT_FOUND);
        } finally {
            query.closeAll();
            pm.close();
        }
    } 

    /** 
     * Returns a short description of the servlet.
     * @return a String containing servlet description
     */
    @Override
    public String getServletInfo() {
        return "GAEBenchmark MyBlob SimDownload";
    }
}
