/**
 * @author Yi Huang (Celia)
 */
package benchmark.storage.table.medium;

import javax.jdo.annotations.IdGeneratorStrategy;
import javax.jdo.annotations.Persistent;
import javax.jdo.annotations.PersistenceCapable;
import javax.jdo.annotations.PrimaryKey;
import com.google.appengine.api.datastore.Key;

/**
 */
@PersistenceCapable
public class MediumData {
    @PrimaryKey
    @Persistent(valueStrategy = IdGeneratorStrategy.IDENTITY)
    private Key key;
    
    @Persistent
    private String data;

    @Persistent
    private Long serial;

    public MediumData(String data, Long serial) {
        this.data = data;
        this.serial = serial;
    }

    public String getData() {
        return data;
    }

    public Long getSerial() {
        return serial;
    }
}
