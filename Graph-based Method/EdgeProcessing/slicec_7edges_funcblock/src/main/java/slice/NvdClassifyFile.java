package slice;

import java.io.BufferedReader;
import java.io.BufferedWriter;
import java.io.File;
import java.io.FileReader;
import java.io.FileWriter;
import java.util.UUID;
import java.util.regex.Pattern;

public class NvdClassifyFile {
	private static int count_good = 0;
	private static int count_bad = 0;
	
	private static void del(String sourcePath, String storePath) throws Exception {
        File file = new File(sourcePath);
        File[] fs = file.listFiles();
        for (File f : fs) {
            if (f.isDirectory()) {
                del(f.getAbsolutePath(), storePath);
            }
            
            boolean flag = false;
            String ends = ".c";
            String type = "Unknown";
            if (f.isFile()) {
            	String[] filenames = f.toString().split("/");
            	String filename = filenames[filenames.length-1];
            	if (filename.equals("io.c") || filename.endsWith(".h") || filename.endsWith(".cpp"))
            		continue;
            	else {
					flag = true;
					if (filename.endsWith(".cpp"))
						ends = ".cpp";
					
					Pattern bad = Pattern.compile(".*[Oo][Ll][Dd].*");
                    Pattern good = Pattern.compile(".*[Nn][Ee][Ww].*");
                    
                    if (good.matcher(filename).matches() && (!bad.matcher(filename).matches())) {
                    	type = "Good";
                    	count_good += 1;
                    }
                    if (bad.matcher(filename).matches() && (!good.matcher(filename).matches())) {
                    	type = "Bad";
                    	count_bad += 1;
                    }
				}
            }
            else {
				continue;
			}
            
            if (flag) {
                String store = storePath + "/" + UUID.randomUUID() + "-" + type + ends;

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
            NvdClassifyFile.del(sourcePath, storePath);
        } catch (Exception e) {
            e.printStackTrace();
        }
        System.out.println("vul_files: " + count_bad + ",    non_vul_files: " + count_good);
    }
}
