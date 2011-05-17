/**
 * @author Yi Huang (Celia)
 */
package benchmark.storage.table.medium;

import benchmark.storage.ActionStatus;
import benchmark.storage.PMF;
import java.io.IOException;
import javax.jdo.PersistenceManager;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class PutServlet extends HttpServlet {
    protected void HandleRequest(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        long t1 = System.currentTimeMillis();
        int size = Integer.parseInt(request.getParameter("size"));
        int seed = Integer.parseInt(request.getParameter("seed"));
        PersistenceManager pm = PMF.getManager();
        try {
            MediumData data = new MediumData(InitServlet.getRandomString(seed, size), new Long(seed));
            long t2 = System.currentTimeMillis();
            pm.makePersistent(data);
            long t3 = System.currentTimeMillis();
            response.getWriter().format("table put %s %d %d %d", new Object[]{
                ActionStatus.SUCCESS, t1, t2, t3
            });
        } finally {
            pm.close();
        }
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

    /** 
     * Returns a short description of the servlet.
     * @return a String containing servlet description
     */
    @Override
    public String getServletInfo() {
        return "GAEBenchmark Table Put";
    }
}
