/**
 * @author Yi Huang (Celia)
 */
package benchmark.storage.table;

import benchmark.storage.PMF;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import javax.jdo.PersistenceManager;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;

public class InitServlet extends HttpServlet {
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
        int num = Integer.parseInt(request.getParameter("num"));
        int size = Integer.parseInt(request.getParameter("size"));
        int seed = Integer.parseInt(request.getParameter("seed"));
        List<SmallData> list = new ArrayList<SmallData>(num);
        for(int i=0; i<num; i++) {
            list.add(new SmallData(getRandomString(seed, size)));
        }
        PersistenceManager pm = PMF.getManager();
        try {
            pm.makePersistentAll(list);
        } finally {
            pm.close();
        }
    }

    public static String getRandomString(int seed, int size) {
        StringBuilder sb = new StringBuilder();
        sb.append(seed);
        while(sb.length() < size) {
            sb.append('#');
        }
        return sb.toString();
    }

    /** 
     * Returns a short description of the servlet.
     * @return a String containing servlet description
     */
    @Override
    public String getServletInfo() {
        return "GAEBenchmark Table Init";
    }
}
