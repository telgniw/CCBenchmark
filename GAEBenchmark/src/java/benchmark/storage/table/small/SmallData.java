/**
 * @author Yi Huang (Celia)
 */
package benchmark.storage.table.small;

import javax.jdo.annotations.IdGeneratorStrategy;
import javax.jdo.annotations.Persistent;
import javax.jdo.annotations.PersistenceCapable;
import javax.jdo.annotations.PrimaryKey;
import com.google.appengine.api.datastore.Key;
import com.google.appengine.api.datastore.Text;

/**
 */
@PersistenceCapable
public class SmallData {
    @PrimaryKey
    @Persistent(valueStrategy = IdGeneratorStrategy.IDENTITY)
    private Key key;
    
    @Persistent
    private Text data;

    public SmallData(Text data) {
        this.data = data;
    }

    public Text getData() {
        return data;
    }
}
