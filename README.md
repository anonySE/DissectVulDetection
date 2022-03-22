# DissectVulDetection


# Graph-based Method

Combining multi graph structure and utilizing graph neural networks to learn detection models for vulnerability classification. This is one of the implementations of the graph-based method .

The basic idea of this part of the experiment is to combine different type of code graph structures, to find out if the composite graphs outperform single graph structures and how much. We selected AST, CFG, PDG and their various combinations as our experimental targets, and we extract these graph structures from C/C++ source code utilizing the code analysis tool Joern.



## Contents

- Getting Started
  - Requirements
    - Softwares
    - Python Libraries
  - Setup
- Multi Graph Model
  - Basic Structure
  - Graph Processing
  - Model Training
  - Results
- Contact



## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.

### Requirements

Install the necessary dependencies before running the project. All these softwares and libraries are needed in our project during implementing the graph processing and model training module.

##### Softwares

- [Joern](https://joern.io/)
- [Python (==3.7)](https://www.python.org/downloads/)
- [Java (==11.0)](https://www.oracle.com/java/technologies/downloads/)

##### Python Libraries

- [Tensorflow (>=2.0.0)](https://tensorflow.google.cn/)

- Please reference ```requirements.txt``` for more details



### Setup

Clone this project,  deploy on your own local machine, and get ready for your first running.

##### 1) Clone this Repo

```
$ 
```

##### 2) Install Prerequisites

```
$ pip install -r requirements.txt
```

##### 3) Compile Java Source Code

```
$ cd MultiGraphModel/GraphProcessing/slicec_7edges_funcblock
$ javac -cp lib/org/eclipse/cdt.core/5.6.0.201402142303/*:lib/org/eclipse/equinox.common/3.6.200.v20130402-1505/*:lib/com.ibm.icu-4.4.2.jar -d bin src/main/java/slice/*.java src/main/java/sevenEdges/*.java src/main/java/sevenEdges/treeview/*.java src/main/java/sevenEdges/treeview/ast/*.java src/main/java/sevenEdges/nodeTraversal/*.java
```





## Multi Graph Model

This part is an instruction of our graph-based model, which leverages the advances in graph neural networks(GNNs) to develop a learning method to capture the potential code patterns under composite graph structures.

### Basic Structure

```
├── README.md                       <- The top-level README for developers using this project.
├── requirements.txt                <- The necessary python environments.
|
├── GraphModelClient				<- The model training module
│   ├── cli     
│   │   ├── train.py		    	<- The entrance of training models.	
│   │   ├── test.py		     		<- Testing the specified model using data.
│   │   ├── __init__.py
│   ├── cli_utils     
│   │   ├── default_hypers	
│   │   ├── dataset_utils.py	
│   │   ├── model_utils.py	
│   │   ├── param_helpers.py	
│   │   ├── task_utils.py
│   │   ├── training_utils.py
│   │   ├── __init__.py	
│   ├── data                       
│   │   ├── data	
│   │   │   ├── data_preprocess.py
│   │   │   ├── our_map_all.txt
│   │   │   ├── __init__.py
│   │   ├── graph_dataset.py	
│   │   ├── jsonl_graph_dataset.py	
│   │   ├── jsonl_graph_property_dataset.py	
│   │   ├── __init__.py	
│   ├── layers                      
│   │   ├── message_passing	
│   │   │   ├── ggnn.py
│   │   │   ├── gnn_edge_mlp.py
│   │   │   ├── gnn_film.py
│   │   │   ├── message_passing.py
│   │   │   ├── __init__.py
│   │   ├── gnn.py
│   │   ├── graph_global_exchange.py	
│   │   ├── nodes_to_graph_representation.py
│   │   ├── __init__.py	
│   ├── models   
│   │   ├── graph_binary_classification_task.py
│   │   ├── graph_regression_task.py
│   │   ├── graph_task_model.py 
│   │   ├── node_multiclass_task.py
│   │   ├── __init__.py	
│   ├── utils                          
│   │   ├── activation.py
│   │   ├── constants.py
│   │   ├── gather_dense_gradient.py
│   │   ├── param_helpers.py
│   └── └── __init__.py	
│   └── __init__.py
|
├── GraphProcessing					<- The graph processing module.
│   ├── README.md					<- The README for developers extracting various graphs.
│   ├── joern-cli					<- Use Joern library to extract different graph edges.
│   │   ├── bin
│   │   ├── lib
│   │   ├── data
│   │   ├── graph					<- Scripts to generate various graphs.
│   │   │   ├── ast.sc				<- Scripts to generate AST graph.
│   │   │   ├── ast+cfg.sc			<- Scripts to generate AST+CFG combined graph.
│   │   │   ├── all.sc				<- Scripts to generate AST+CFG+PDG composite graph.
│   │   ├── parse_result
│   │   ├── raw_result
│   │   ├── result
│   │   ├── joern
│   │   ├── joern-parse
│   ├── slicec_7edges_funcblock		<- Utils for extracting graphs.
│   │   ├── bin
│   │   ├── lib
│   │   ├── src
```

### Graph Processing

To construct various graph structures form C/C++, we use Eclipse CDT library and Joern to extract and integrate different graphs.

<u>For more details, please reference ```GraphProcessing/README```.</u>

##### 1) Slice Data

We use CDT library to extract the target functions in sample files.

```
$ cd MultiGraphModel/GraphProcessing/slicec_7edges_funcblock
```

- Run slice.ClassifyFileOfProject to extract all the C file from the SARD dataset / Run slice.NvdClassifyFile for the NVD dataset.
- Run slice.Main to slice SARD data in function level / slice.NvdMain for the NVD dataset.

##### 2) Extract different edge relationships

We use Joern to extract edges of specific graphs and classify them by types. Then we traverse the source codes' AST nodes parsed by CDT library, and integrate edges with AST nodes to generate target graphs.

```
$ cd MultiGraphModel/GraphProcessing/slicec_7edges_funcblock
```

- Use Joern to get all the specific edge relationships(i.e. control flows and data flows)
- Run sevenEdges.Main to extract source codes' AST nodes from SARD / sevenEdges.NvdMain for the NVD dataset.
- Run sevenEdges.concateJoern to integrate nodes with edges.

### Model Training

This part of the code provides a user-friendly interface. For a quick start, you can simply run the command below:

```
$ CUDA_VISIBLE_DEVICES=0 python train.py GGNN GraphBinaryClassification ../data/data/ast_graph
```

### Results

Train/Val/Test ratios - 0.8/0.1/0.1





## Contact





