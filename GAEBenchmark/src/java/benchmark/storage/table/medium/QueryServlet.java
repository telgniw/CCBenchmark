/**
 * @author Yi Huang (Celia)
 */
package benchmark.storage.table.medium;

import benchmark.storage.ActionStatus;
import benchmark.storage.PMF;
import java.io.IOException;
import java.util.List;
import javax.jdo.Query;
import javax.jdo.PersistenceManager;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class QueryServlet extends HttpServlet {
    protected void HandleRequest(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        long t1 = System.currentTimeMillis();
        PersistenceManager pm = PMF.getManager();
        int size = Integer.parseInt(request.getParameter("size"));
        int seed = Integer.parseInt(request.getParameter("seed"));
        String str = InitServlet.getRandomString(seed, size);
        try {
            Query query = pm.newQuery(MediumData.class);
            query.setFilter("data == str");
            query.declareParameters("String str");
            long t2 = System.currentTimeMillis();
            List<MediumData> list = (List<MediumData>) query.execute(str);
            for(int i=0; i<list.size(); i++)
                list.get(i);
            long t3 = System.currentTimeMillis();
            response.getWriter().format("table.medium query %s SEED(%d) %d %d %d", new Object[]{
                ActionStatus.SUCCESS, seed, t1, t2, t3
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
        return "GAEBenchmark Table Query";
    }
}
