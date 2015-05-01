package write;

import java.io.BufferedWriter;
import java.io.File;
import java.io.FileOutputStream;
import java.io.IOException;
import java.io.OutputStreamWriter;

/**
 * Created by Hugo Silva on 30/04/2015.
 */

public class WriteFile {
    public static void stringBuilderToFile(StringBuilder sb, String filePath) {
        // Get the correct Line Separator for the OS (CRLF or LF)
        String nl = System.getProperty("line.separator");
        try {
            BufferedWriter out = new BufferedWriter(new OutputStreamWriter(new FileOutputStream(new File(filePath)), "UTF8"));
            String outText = sb.toString();
            out.write(outText);
            out.close();
            System.out.println("New file "+filePath+" created!");
        } catch (IOException e) {
            e.printStackTrace();
        }
    }
}
