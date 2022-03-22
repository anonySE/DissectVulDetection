# Directory structure of the repo

```
.
│  cal.py							# extract metrics of every function slices
│  env_config.sh					# scripts for environment configuration
│  README.md
│  Result.xlsx
│  start_neo4j.sh					# scripts for start neo4j service
│
├─nvd_process
│  │  data(NEW).csv
│  │  data(OLD).csv
│  │  data.csv
│  │  out.txt
│  │  to_csv.py						# Convert txt file to csv file for the input of ML
│  │
│  └─models							# machine learning models
│          AdaBoost.py
│          Bayesian.py
│          GradientBoosting.py
│          KNN.py
│          RandomForest.py
│          SVM.py
│
└─sard_process
    │  data（去除io.c）.csv
    │  data（完整版）.csv
    │  data（最终版）.csv
    │  out.txt
    │  SARD_testcaseinfo.txt		# the line numbers of vulnerable lines
    │  to_csv1.py					# Convert txt file to csv file for input of ML
    │  to_csv2.py					# Convert txt file to csv file for input of ML
    │
    └─models						# machine learning models
            AdaBoost.py
            Bayesian.py
            GradientBoosting.py
            KNN.py
            RandomForest.py
            SVM.py
```

## Environment

Tested on ubuntu 20.04

* joern 0.3.1
* neo4j 2.1.8
* python 3.8
* python 2.7
* py2neo 2.0

> Note1: Please follow the instructions in `config.sh`. Don't run it directly as it contains some branching instructions and something wrong may happen. Read and follow it.
>
> Note2: A higher version of py2neo may be required when installing some dependencies. After that, please make sure py2neo is back to 2.0 version.

## Data preprocess

Copy the required files to the dataset directory. 

```shell
cp ./cal.py /path/to/dataset/cal.py
cp ./start_neo4j.sh /path/to/dataset/start_neo4j.sh
cd /path/to/dataset/
```

On screen A: generate function slices and start neo4j service

> Note1: Everytime after you finish processing a batch (dir_xxx), you should run `start_neo4j.sh` to restart the neo4j service, otherwise the indexing will be problematic.
>
> Note2: Recommended to split source code files into multiple batches, otherwise neo4j service may shut down.
>
> Note3: Read the script before run it. Please follow the instructions to edit the dataset path.

```shell
source start_neo4j.sh
```

On screen B: extract metrics of every function slices

```shell
python2 cal.py
```

The output is a file named `out.txt`.

## Machine learning model

### For SARD

```shell
mv out.txt <repo_path>/sard_process/out.txt
cd <repo_path>/sard_process/
```

You can run `to_csv1.py` or `to_csv2.py` to convert txt file to csv file for the input of ML.

> to_csv1.py: Remove all the files named "io.c".
> to_csv2.py: Remove all the files named "io.c" and choose only those function slices with absolutely correct labels.

```shell
python to_csv1.py
# python to_csv2.py
```

The output is a csv file named `data.csv`.

You can use one of the six machine learning models in `models`, or prepare your own models for training.

```
cd ./models
python AdaBoost.py
```

### For NVD

```shell
mv out.txt <repo_path>/nvd_process/out.txt
cd <repo_path>/nvd_process/
```

You can run `to_csv.py` to convert txt file to csv file for the input of ML.

```shell
python to_csv.py
```

The output is a csv file named `data.csv`.

You can use one of the six machine learning models in `models`, or prepare your own models for training.

```
cd ./models
python AdaBoost.py
```







