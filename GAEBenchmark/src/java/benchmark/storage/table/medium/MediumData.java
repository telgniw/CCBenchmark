/**
 * @author Yi Huang (Celia)
 */
package benchmark.storage.table.medium;

import javax.jdo.annotations.IdGeneratorStrategy;
import javax.jdo.annotations.Persistent;
import javax.jdo.annotations.PersistenceCapable;
import javax.jdo.annotations.PrimaryKey;
import com.google.appengine.api.datastore.Key;
import com.google.appengine.api.datastore.Text;

/**
 */
@PersistenceCapable
public class MediumData {
    @PrimaryKey
    @Persistent(valueStrategy = IdGeneratorStrategy.IDENTITY)
    private Key key;
    
    @Persistent
    private Text data;

    @Persistent
    private Long serial;

    public MediumData(Text data, Long serial) {
        this.data = data;
        this.serial = serial;
    }

    public Text getData() {
        return data;
    }

    public Long getSerial() {
        return serial;
    }
}
