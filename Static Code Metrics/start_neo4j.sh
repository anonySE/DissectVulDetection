# change the dir, e.g., /opt/SARD/
cd /path/to/dataset/
# do this for every partition
rm -rf ./.joernIndex/
# change the dir every time, e.g., /opt/SARD/000/001/
java -jar /opt/joern-0.3.1/bin/joern.jar /path/to/dataset/000/001/

cd $INSTALLDIR
rm -rf ./neo4j-community-2.1.8
tar -zxvf artifact.php\?name\=neo4j-community-2.1.8-unix.tar.gz
unzip neo4j-gremlin-plugin-2.1-SNAPSHOT-server-plugin.zip -d $Neo4jDir/plugins/gremlin-plugin
sed -i 's/#org.neo4j.server.webserver.address=0.0.0.0/org.neo4j.server.webserver.address=0.0.0.0/g' /opt/neo4j-community-2.1.8/conf/neo4j-server.properties
# change the dir to the dir of .joernIndex
sed -i 's/data\/graph.db/\/path\/to\/dataset\/.joernIndex\//g' /opt/neo4j-community-2.1.8/conf/neo4j-server.properties
sed -i 's/#org.neo4j.server.webserver.address/org.neo4j.server.webserver.address/g' /opt/neo4j-community-2.1.8/conf/neo4j-server.properties
./neo4j-community-2.1.8/bin/neo4j console