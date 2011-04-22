/**
 * @author Yi Huang (Celia)
 */
package benchmark.storage.table;

import benchmark.storage.PMF;
import java.io.IOException;
import java.util.Random;
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
        PersistenceManager pm = PMF.getManager();
        for(int i=0; i<num; i++) {
            byte[] bytes = getRandomBytes(seed, size);
            pm.makePersistent(new SmallData(new String(bytes)));
        }
    }

    private byte[] getRandomBytes(int seed, int size) {
        byte[] obj = new byte[size];
        new Random(seed).nextBytes(obj);
        return obj;
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
