import os
import re
import numpy as np
import traceback

"""
After joern processes the c code, use this code;
0 represents AST, 1 represents CFG, 2 represents PDG
"""


def graphRelation(rootpath, pathdir, tag, edgetypes):
    files = os.listdir(rootpath)
    for file in files:
        nodeRelation = []
        nodeInformation = []
        path = rootpath + '/' + file
        try:
            with open(path, 'r', encoding='utf-8') as f:
                lines = str(f.read())
                alllist = lines.split("),List(")
                # Determine whether the data is empty
                node1 = []
                node2 = []
                relation = []
                if (alllist[1] != ""):
                    filename = alllist[0].split("/")[-1]
                    # add edge
                    if len(edgetypes) >= 1:
                        nodeRelation.append(alllist[1])  # 1graph
                    if len(edgetypes) >= 2:
                        nodeRelation.append(alllist[3])  # 2graph
                    if len(edgetypes) >= 3:
                        nodeRelation.append(alllist[5])  # 3graph
                    # add
                    if len(edgetypes) >= 1:
                        nodeInformation.append(alllist[2])  # 1graph
                    if len(edgetypes) >= 2:
                        nodeInformation.append(alllist[4])  # 2graph
                    if len(edgetypes) >= 3:
                        nodeInformation.append(alllist[6])  # 3graph
                    # Regular processing
                    nodeRelation = re.findall(r"\(\d*,\d*,\d*\)", str(nodeRelation))
                    nodeInformation = re.findall(r"\(\d*,.*?\)", str(nodeInformation))
                    # Remove duplicate nodes
                    nodeInformation = list(set(nodeInformation))

                    # Extract the contents of each column into list => batch processing
                    nodeRelation = ' '.join(nodeRelation)
                    b = re.findall('\d+', nodeRelation)
                    for i in range(0, len(b), 3):
                        node1.append(b[i])
                        node2.append(b[i + 1])
                        relation.append(b[i + 2])
                    # relation_matrix = np.vstack([node1, node2, relation]).T

                    nodes = []
                    means = []
                    for i in nodeInformation:
                        node = re.search('\d+(?=,)', i)
                        mean = re.search('(?<=,).*', i)
                        nodes.append(node.group())
                        means.append(mean.group())
                    # feature_matrix = np.vstack([nodes,means]).T

                    # Replace node numbers
                    new_node1 = []
                    new_node2 = []
                    new_nodes = list(range(0, len(nodes)))
                    for x in node1:
                        for i in range(len(nodes)):
                            if x == nodes[i]:
                                # new_node1.append(x.replace(str(x), str(i)))
                                new_node1.append(str(i))
                                break
                    for x in node2:
                        for i in range(len(nodes)):
                            if x == nodes[i]:
                                # new_node2.append(x.replace(str(x), str(i)))
                                new_node2.append(str(i))
                                break

                    # write to file
                    if os.path.exists(pathdir) == False:
                        os.makedirs(pathdir)
                    with open(pathdir + '/' + filename + ".txt", 'w', encoding='utf-8') as f1:
                        for x, y, z in zip(new_node1, new_node2, relation):
                            # for x, y, z in zip(node1, node2, relation):
                            f1.write('(' + x + ',' + y + ',' + z + ')')
                            # f1.write(x + ',' + y + ',' + z)
                            f1.write("\n")
                        f1.write("-----------------------------------")
                        f1.write("\n")
                        for x, y in zip(new_nodes, means):
                            # for x, y in zip(nodes, means):
                            f1.write('(' + str(x) + ',' + y)
                            # f1.write(str(x) + ',' + y)
                            f1.write(("\n"))
                        f1.write('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
                        f1.write("\n")
                        if tag == 'good':
                            f1.write('0')
                        elif tag == 'bad':
                            f1.write('1')
        except Exception as e:
            print(path)
            print(e)
            print(traceback.print_exc())


if __name__ == '__main__':
    dataPath = r"raw_result/bad_ast_pdg"
    outPath = r"result/ast_pdg"
    # bad or good
    dataTag = 'bad'
    edge_types = ['ast', 'pdg']
    graphRelation(dataPath, outPath, dataTag, edge_types)
    print("ooooooooooooooover")
