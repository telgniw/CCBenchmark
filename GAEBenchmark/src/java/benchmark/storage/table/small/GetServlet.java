/**
 * @author Yi Huang (Celia)
 */
package benchmark.storage.table.small;

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

public class GetServlet extends HttpServlet {
    private static final Logger log = Logger.getLogger(GetServlet.class.getName());

    protected void HandleRequest(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        ActionStatus status = ActionStatus.FAILED;
        long t1 = System.currentTimeMillis();
        int size = Integer.parseInt(request.getParameter("size"));
        int seed = Integer.parseInt(request.getParameter("seed"));
        String str = InitServlet.getRandomString(seed, size);
        PersistenceManager pm = PMF.getManager();
        try {
            Query query = pm.newQuery(SmallData.class);
            query.setFilter("data == str");
            query.declareParameters("String str");
            long t2 = System.currentTimeMillis();
            List<SmallData> list = (List<SmallData>) query.execute(str);
            long t3 = System.currentTimeMillis();
            if(list.isEmpty() || list.get(0).getData().equals(str) == false)
                response.getWriter().format("table get %s", new Object[]{
                    ActionStatus.FAILED
                });
            else
                response.getWriter().format("table get %s %d %d %d", new Object[]{
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
        return "GAEBenchmark Table Get";
    }
}
