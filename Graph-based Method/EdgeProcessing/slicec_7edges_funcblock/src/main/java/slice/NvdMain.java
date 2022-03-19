package slice;

public class NvdMain {
	public static void main(String[] args) {

        String sourceFilePath = args[0];
        String storeFilePath = args[1];

        slice.AST_extract ast_extract = new slice.AST_extract();

        int batchsize = 10;
        int batchnum_lastrun = 0;

        //sard_good_bad
        ast_extract.AST_NvdGoodBad(sourceFilePath, storeFilePath,batchnum_lastrun,batchsize);
    }
}
