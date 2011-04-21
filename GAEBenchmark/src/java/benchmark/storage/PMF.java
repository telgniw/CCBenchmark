/**
 * @author Yi Huang (Celia)
 */
package benchmark.storage;

import javax.jdo.JDOHelper;
import javax.jdo.PersistenceManager;
import javax.jdo.PersistenceManagerFactory;

/**
 */
public final class PMF {
    private static final PersistenceManagerFactory instance =
        JDOHelper.getPersistenceManagerFactory("transactions-optional");

    public static PersistenceManagerFactory getInstance() {
        return instance;
    }

    public static PersistenceManager getManager() {
        return instance.getPersistenceManager();
    }

    private PMF() {
        /* empty */
    }
}

