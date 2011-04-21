/**
 * @author Yi Huang (Celia)
 */
package benchmark.storage.myblob;

import javax.jdo.annotations.IdGeneratorStrategy;
import javax.jdo.annotations.Persistent;
import javax.jdo.annotations.PersistenceCapable;
import javax.jdo.annotations.PrimaryKey;
import com.google.appengine.api.datastore.Key;
import com.google.appengine.api.datastore.Blob;

/**
 */
@PersistenceCapable
public class MyBlobInfo {
    @PrimaryKey
    @Persistent(valueStrategy = IdGeneratorStrategy.IDENTITY)
    private Key key;
    
    @Persistent
    private String name;

    @Persistent
    private String type;

    @Persistent
    private Integer size;

    @Persistent
    private Blob blob;

    public MyBlobInfo(String name, String type, int size, Blob blob) {
        this.name = name;
        this.type = type;
        this.size = new Integer(size);
        this.blob = blob;
    }

    public String getName() {
        return name;
    }
    public String getType() {
        return type;
    }
    public int getSize() {
        return size.intValue();
    }
    public Blob getBlob() {
        return blob;
    }
}
