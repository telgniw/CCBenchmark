/**
 * @author Yi Huang (Celia)
 */
package benchmark.storage.myblob;

import benchmark.storage.PMF;
import java.io.IOException;
import java.util.Random;
import java.util.logging.Logger;
import javax.jdo.Query;
import javax.jdo.PersistenceManager;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class DeleteServlet extends HttpServlet {
    private static final Logger log = Logger.getLogger(DeleteServlet.class.getName());

    protected void HandleRequest(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
            PersistenceManager pm = PMF.getManager();
            Query query = pm.newQuery(MyBlobInfo.class);
            query.deletePersistentAll();
            log.info("delete SUCCESS");
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
        return "GAEBenchmark MyBlob SimDelete";
    }
}
