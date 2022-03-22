## Graph Processing

To construct various graph structures form C/C++, we use Eclipse CDT library and Joern to extract and integrate different graphs.

The specific steps of graph processing are as follows. **Don't forget to Modify the path with your own implementation.**



#### 1. Slice Data

In this part we extract the target functions in the sample files.

```
$ cd GraphProcessing/slicec_7edges_funcblock/bin
```

- Run slice.ClassifyFileOfProject to extract all the C files in function level from the SARD dataset.

```
$ java -cp ../bin:../lib/org/eclipse/cdt.core/5.6.0.201402142303/*:../lib/org/eclipse/equinox.common/3.6.200.v20130402-1505/*:../lib/com.ibm.icu-4.4.2.jar slice.ClassifyFileOfProject /data/sard ../../data/sard
```

> Replace "/data/sard" with your own path to the SARD dataset.

For the NVD dataset, run slice.NvdClassifyFile

- Run slice.Main to slice SARD C files in function level.

```
$ java -cp ../bin:../lib/org/eclipse/cdt.core/5.6.0.201402142303/*:../lib/org/eclipse/equinox.common/3.6.200.v20130402-1505/*:../lib/com.ibm.icu-4.4.2.jar slice.Main ../../data/sard ../../joern-cli/data
```

For the NVD dataset, run slice.NvdMain

This code will generate 2 folders in the path "../../joern-cli/data" which named "good" and "bad", where "bad" folder saves those functions which are vulnerable while "good" folder saves the rest.



#### 2. Extract Edges

We use Joern to parse AST, CFG, PDG dependencies and relationships for C/C++

```
$ cd GraphProcessing/joern-cli
```

##### 1) Parse code and generate CPG

```
$ mkdir parse_result
$ sh joern-parse data/good --out parse_result/good.bin
$ sh joern-parse data/bad --out parse_result/bad.bin
```

##### 2) Load CPG and generate various graphs

```
$ sh joern
joern> loadCpg("parse_result/good.bin")
joern> cpg.runScript("graph/ast.sc")
```

> The same for "parse_result/bad.bin"
>
> Please Modify the generated result path (i.e. raw_result/good_ast/) in ast.sc

##### 3) Concate and purify edge information

We use joern_relation.py to concate and purify edge information. Please modify data path (i.e. raw_result/good_ast) and output path (i.e. result/ast) in the script.



#### 3. Generate Graphs

We use Joern to extract edges of specific graphs and classify them by types. Then we traverse the source codes' AST nodes parsed by CDT library, and integrate edges with AST nodes to generate target graphs.

```
$ cd cd EdgeProcessing/slicec_7edges_funcblock/bin
```

- Run sevenEdges.Main to extract source codes' AST nodes and other information from the SARD dataset.

```
$ java -cp ../bin:../lib/org/eclipse/cdt.core/5.6.0.201402142303/*:../lib/org/eclipse/equinox.common/3.6.200.v20130402-1505/*:../lib/com.ibm.icu-4.4.2.jar sevenEdges.Main ../../joern-cli/data/good ../../../GraphModelClient/data/data/ast_graph
```

> The same for "../../joern-cli/data/bad"

For the NVD dataset, run sevenEdges.NvdMain

- Run sevenEdges.concateJoern to integrate nodes with edges.

```
$ java -cp ../bin:../lib/org/eclipse/cdt.core/5.6.0.201402142303/*:../lib/org/eclipse/equinox.common/3.6.200.v20130402-1505/*:../lib/com.ibm.icu-4.4.2.jar sevenEdges.concateJoern ../../../GraphModelClient/data/data/ast_graph ../../joern-cli/result/ast
```

The output result are .txt format text files, which are exactly the inputs of our model.

