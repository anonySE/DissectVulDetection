package slice;

import java.io.*;
import java.util.UUID;

/**
 * Categorize the files in a project, such as all C language files, are placed in a new folder under the project
 *
 * @author xiaoH  2019/11/4  20:40
 */
public class ClassifyFileOfProject {

    private static void del(String sourcePath, String storePath) throws Exception {
        File file = new File(sourcePath);
        File[] fs = file.listFiles();
        for (File f : fs) {
            if (f.isDirectory()) {
                del(f.getAbsolutePath(), storePath);
            }
            
            boolean flag = false;
            String ends = ".c";
            if (f.isFile()) {
            	String[] filenames = f.toString().split("/");
            	String filename = filenames[filenames.length-1];
            	if (filename.equals("io.c") || filename.endsWith(".h"))
            		continue;
            	else {
					flag = true;
					if (filename.endsWith(".cpp"))
						ends = ".cpp";
				}
            }
            else {
				continue;
			}
            
            if (flag) {
                String store = storePath + "/" + UUID.randomUUID() + ends;

                if (!new File(storePath).exists()) {
                    new File(storePath).mkdirs();
                }
                if (!new File(store).exists()) {
                    new File(store).createNewFile();
                }

                FileReader fr = new FileReader(f);
                BufferedReader br = new BufferedReader(fr);

                FileWriter fw = new FileWriter(new File(store));
                BufferedWriter bw = new BufferedWriter(fw);

                String in;
                while ((in = br.readLine()) != null) {
                    bw.write(in + "\n");
                    bw.flush();
                }
            }
        }
    }

    public static void main(String[] args) {
        //.c
        String sourcePath = args[0];
        String storePath = args[1];
        try {
            ClassifyFileOfProject.del(sourcePath, storePath);
        } catch (Exception e) {
            e.printStackTrace();
        }

    }
}
