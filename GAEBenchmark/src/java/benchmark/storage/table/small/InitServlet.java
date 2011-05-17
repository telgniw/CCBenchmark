/**
 * @author Yi Huang (Celia)
 */
package benchmark.storage.table.small;

import benchmark.storage.ActionStatus;
import benchmark.storage.PMF;
import java.io.IOException;
import java.util.ArrayList;
import java.util.List;
import javax.jdo.PersistenceManager;
import javax.servlet.ServletException;
import javax.servlet.http.HttpServlet;
import javax.servlet.http.HttpServletRequest;
import javax.servlet.http.HttpServletResponse;
import com.google.appengine.api.datastore.Text;
import com.google.appengine.api.memcache.MemcacheService;
import com.google.appengine.api.memcache.MemcacheServiceFactory;

public class InitServlet extends HttpServlet {
    private static final MemcacheService memcache;

    static {
        memcache = MemcacheServiceFactory.getMemcacheService("table");
    }

    protected void HandleRequest(HttpServletRequest request, HttpServletResponse response)
            throws ServletException, IOException {
        int max = Integer.parseInt(request.getParameter("max"));
        int num = Integer.parseInt(request.getParameter("num"));
        int size = Integer.parseInt(request.getParameter("size"));
        int seed = Integer.parseInt(request.getParameter("seed"));
        List<SmallData> list = new ArrayList<SmallData>(max*num);
        for(int i=0; i<max; i++) {
            String str = getRandomString(seed+i, size);
            for(int j=0; j<num; j++) {
                list.add(new SmallData(new Text(str)));
            }
        }
        PersistenceManager pm = PMF.getManager();
        try {
            pm.makePersistentAll(list);
        } finally {
            pm.close();
        }
        response.getWriter().format("table init %s MAX(%d) NUM(%d) SIZE(%d) SEED(%d)", new Object[]{
            ActionStatus.SUCCESS, max, num, size, seed
        });
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

    public static String getRandomString(int seed, int size) {
        String key = "table".concat(Integer.toString(size));
        String tmp = null;
        if(memcache.contains(key))
            tmp = (String) memcache.get(key);
        if(tmp == null || tmp.length() != size) {
            StringBuilder sb = new StringBuilder();
            while(sb.length() < size) {
                sb.append('#');
            }
            tmp = sb.toString();
            memcache.put(key, tmp);
        }
        return Integer.toString(seed).concat(tmp).substring(0, size);
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
