#!/bin/bash

# =========================== #
# ==== setup environment ==== #
# =========================== #
echo 'INSTALLDIR=/opt/' >> ~/.bashrc
echo 'JOERN=/opt/joern-0.3.1' >> ~/.bashrc
source ~/.bashrc
sudo chmod 777 -R /opt

# update apt
sudo apt-get -y update

# install dependencies
sudo apt-get -y install git
sudo apt-get -y install python-setuptools python-dev
sudo apt-get -y install graphviz libgraphviz-dev graphviz-dev
sudo apt-get -y install pkg-config
sudo apt-get -y install openjdk-8-*
sudo apt-get -y install ant
sudo apt-get -y install unzip
sudo apt-get -y install p7zip-full
sudo apt-get -y install python-pip
sudo apt-get -y install python3-pip
sudo apt-get -y install python-igraph

# build joern
cd $INSTALLDIR
wget https://github.com/fabsx00/joern/archive/0.3.1.tar.gz
tar xfzv 0.3.1.tar.gz
cd joern-0.3.1/
wget http://mlsec.org/joern/lib/lib.tar.gz
tar xfzv lib.tar.gz
sudo ant
sudo ant tools
echo "alias joern='java -jar /opt/joern-0.3.1/bin/joern.jar'" >> ~/.bashrc
source ~/.bashrc

# build neo4j
cd $INSTALLDIR
wget http://neo4j.com/artifact.php?name=neo4j-community-2.1.8-unix.tar.gz
tar -zxvf artifact.php\?name\=neo4j-community-2.1.8-unix.tar.gz
echo "export Neo4jDir='/opt/neo4j-community-2.1.8/'" >> ~/.bashrc
source ~/.bashrc
wget http://mlsec.org/joern/lib/neo4j-gremlin-plugin-2.1-SNAPSHOT-server-plugin.zip
unzip neo4j-gremlin-plugin-2.1-SNAPSHOT-server-plugin.zip -d $Neo4jDir/plugins/gremlin-plugin

# build py2neo
cd $INSTALLDIR
wget https://github.com/nigelsmall/py2neo/archive/py2neo-2.0.tar.gz
tar zxvf py2neo-2.0.tar.gz
cd /opt/py2neo-py2neo-2.0/
pip uninstall py2neo # uninstall existing one if there's any
sudo python setup.py install
# adding this to make sure you install py2neo 2.0
# note: this may fail, but it doesn't matter
pip install py2neo==2.0

# build python-joern
cd $INSTALLDIR
git clone https://github.com/fabsx00/python-joern.git
pip install py2neo
cd python-joern/
pip install pyparsing
sudo python setup.py install

# build joern-tools
cd $INSTALLDIR
git clone https://github.com/fabsx00/joern-tools
pip install pygraphviz
cd joern-tools/
sudo python setup.py install

# install other dependencies
pip install xlrd
pip3 install gensim==3.8.3
pip3 install imbalanced-learn==0.4.0
pip3 install scikit-learn==0.19.1