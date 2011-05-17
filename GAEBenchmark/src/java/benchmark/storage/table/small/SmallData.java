/**
 * @author Yi Huang (Celia)
 */
package benchmark.storage.table.small;

import javax.jdo.annotations.IdGeneratorStrategy;
import javax.jdo.annotations.Persistent;
import javax.jdo.annotations.PersistenceCapable;
import javax.jdo.annotations.PrimaryKey;
import com.google.appengine.api.datastore.Key;

/**
 */
@PersistenceCapable
public class SmallData {
    @PrimaryKey
    @Persistent(valueStrategy = IdGeneratorStrategy.IDENTITY)
    private Key key;
    
    @Persistent
    private String data;

    public SmallData(String data) {
        this.data = data;
    }

    public String getData() {
        return data;
    }
}
