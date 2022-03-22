from joern.all import JoernSteps
from py2neo.packages.httpstream import http
import os
import sys

sys.setrecursionlimit(1000000)
http.socket_timeout = 9999
dfsnum = 0
flag = []
everpass = []
ch = []

def getALLFuncNode(db):
    query_str = "queryNodeIndex('type:Function')"
    results = db.runGremlinQuery(query_str)
    return results

def loopsnum(db,num):
    query_str="queryNodeIndex('functionId:(%s) AND type:(ForStatement WhileStatement DoStatement)').groupBy{it.functionId}{it.id}" % (num)
    results = db.runGremlinQuery(query_str)
    return len(results)

def ifwithoutelse(db,num):
    query_str="queryNodeIndex('functionId:(%s) AND type:Condition').parents().filter{it.type=='IfStatement'}.as('x').ithChildren('0').as('y').select{it}{it}" % (num)
    results = db.runGremlinQuery(query_str)
    return len(results)
    
def paravar(db,num):
    query_str="g.v(%d).out('IS_FUNCTION_OF_CFG').out('CONTROLS').filter{ it.type == 'Parameter' }.id" % (num)
    results = db.runGremlinQuery(query_str)
    # print results
    return len(results) 

def calleeparavar(db,num):
    query_str="queryNodeIndex('type:Callee AND functionId:%d')" % (num)
    results = db.runGremlinQuery(query_str)
    parnum = 0
    for node in results:
    	parnum += paravar(db,node._id)
    return parnum

def pointerscore(db,num):
    query_str="queryNodeIndex('functionId:(%s) AND type:PtrMemberAccess').functionId.groupCount()" % (num)
    results = len(db.runGremlinQuery(query_str))
    print >>f,"The num of pointer arithmetic:",results
    query_str="queryNodeIndex('functionId:(%s) AND type:PtrMemberAccess').out('USE').groupBy{it.functionId}{it.code}" % (num)
    results = len(db.runGremlinQuery(query_str))
    print >>f,"The num of variables involved in pointer arithmetic:",results
    
    query_str="queryNodeIndex('functionId:(%s) AND type:UnaryOp').as('op').children().filter{it.type=='UnaryOperator' && it.code=='&'}.back('op').astNodes().filter{it.type=='Identifier'}.code.as('sys').select" % (num)
    results = len(db.runGremlinQuery(query_str))

    query_str="queryNodeIndex('functionId:(%s)')" % (num)
    sen = db.runGremlinQuery(query_str)
    num = 0
    for i in sen:
    	i = str(i)
    	if 'Expression' in i:
    	    continue
    	if '*' in i:
    	    num += 1
    results +=num*2
    print >>f,"Max pointer arithmetic a variable is involved in:",results
    return 0

def varsincontrolpred(db,num):
    query_str="queryNodeIndex('functionId:(%s) AND type: Condition').out().filter{it.type=='Symbol'}.dedup()" % num
    sen = db.runGremlinQuery(query_str)
    #for i in sen:
    #    query_str="queryNodeIndex('astNodes(%s)')" % i
    #    print db.runGremlinQuery(query_str)
    #query_str="queryNodeIndex('functionId:(%s) AND isCFGNode:True').as('x').outE('REACHES').as('y').select{it}{it}" % num
    #results = db.runGremlinQuery(query_str)
    #return results
    return len(sen)
    
def varmaxpointerinv(db,num):
    caldict={}
    maxnum=0
    query_str="queryNodeIndex('functionId:(%s) AND type:(RelationalExpression EqualityExpression AdditiveExpression)').as('x').children().filter{it.type=='Identifier'}.code" % num
    results=db.runGremlinQuery(query_str)
    for i in results:
        #print i
        if i in caldict:
            caldict[i] += 1
        else:
            caldict[i] = 1
    for i in caldict.keys():
        if maxnum < caldict[i]:
            maxnum = caldict[i]
    return maxnum


#query_str = "g.v(%d).out('FLOWS_TO').id" % start
#tmp = db.runGremlinQuery(query_str)  

def dfs(db,start,end):
    global dfsnum
    global everpass
    if start == end : 
    	dfsnum += 1
    	return
    query_str = "g.v(%d).out('FLOWS_TO').id" % start
    tmp = db.runGremlinQuery(query_str)
    for i in tmp:
        if i in everpass:
            dfsnum += 1
        else:
            if i != end:
                everpass.append(i)
            dfs(db,i,end)
            if i != end:
                everpass.remove(i)
    return
            
def cyclomaticmetrics(db,num):
    #query_str="queryNodeIndex('functionId:(%s) AND isCFGNode:True').as('x').outE('FLOWS_TO').id.as('y').select{it.functionId}{it}.groupBy{it[0]}{it[1]}{it.size()}" % (num)
    #query_str="queryNodeIndex('functionId:(%s) AND isCFGNode:True')" % (num)
    global dfsnum
    global everpass
    while len(everpass) > 0 : 
    	everpass.pop()
    dfsnum = 0
    everpass = []
    query_str="queryNodeIndex('functionId:(%s) AND isCFGNode:True AND type:CFGEntryNode').id" % (num)
    startid = db.runGremlinQuery(query_str)
    
    query_str="queryNodeIndex('functionId:(%s) AND isCFGNode:True AND type:CFGExitNode').id" % (num)
    endid = db.runGremlinQuery(query_str)
    #print startid,endid
    #print '----'
    results = dfs(db,startid[0],endid[0])
    return results

def datadependent(db,num):
    query_str="queryNodeIndex('functionId:(%s) AND type: Condition').out().filter{it.type=='Symbol'}.code" % num
    results = db.runGremlinQuery(query_str)
    numdict = {}
    large = 0
    for i in results:
        if i in numdict:
            numdict[i] += 1
        else:
            numdict[i] =1
    
    for i in numdict:
        if large < numdict[i]:
            large = numdict[i]
        
    #print results
    return large

def nestedloops(db,num):
    query_str="queryNodeIndex('functionId:(%s) AND type:(ForStatement WhileStatement DoStatement)').id" % (num)
    all_loops_node = db.runGremlinQuery(query_str)
    all_loops_node.sort()
    dict1=dict().fromkeys(tuple(all_loops_node),1)
    dict2=dict().fromkeys(tuple(all_loops_node),1)
    for node1 in all_loops_node:
    	query_str=query = """ idListToNodes(%s).as("x").astNodes().as("y").select{it.id}{it.id}.groupBy{it[0]}{it[1]}.cap """ % (node1)
    	b = db.runGremlinQuery(query_str)
    	c=str(b) 
    	for node2 in all_loops_node:
    		if (node2>node1)and(str(node2) in c):
    			dict1[node2]=dict1[node1]+1
    			dict2[node1]=0
    num1=0
    num2=0
    for node1 in all_loops_node:
    	if (dict1[node1]>1)and(dict2[node1]==1):
    		num1=num1+1
    	if (dict1[node1]>num2):
    		num2=dict1[node1]
    print >>f,"The num of nested loops:",num1	
    print >>f,"Maximum nesting level of loops:",num2
    return 0

def nested_control_structures(db,num):
    query_str="""OR(queryNodeIndex("functionId:(%s) AND type:Condition").in("IS_AST_PARENT"),queryNodeIndex("functionId:%s AND type:ForStatement")).dedup().id""" % (num,num)
    all_control_node = db.runGremlinQuery(query_str)
    all_control_node.sort()
    dict1=dict().fromkeys(tuple(all_control_node),1)
    dict2=dict().fromkeys(tuple(all_control_node),1)
    for node1 in all_control_node:
    	query_str=query = """ idListToNodes(%s).as("x").astNodes().as("y").select{it.id}{it.id}.groupBy{it[0]}{it[1]}.cap """ % (node1)
    	b = db.runGremlinQuery(query_str)
    	c=str(b) 
    	for node2 in all_control_node:
    		if (node2!=node1)and(str(node2) in c):
    			dict1[node2]=dict1[node1]+1
    			dict2[node1]=0
    num1=0
    num2=0
    for node1 in all_control_node:
    	if (dict1[node1]>1)and(dict2[node1]==1):
    		num1=num1+1
    	if (dict1[node1]>num2):
    		num2=dict1[node1]
    print >>f,"The num of nested control structures:",num1	
    print >>f,"Maximum nesting level of control structures:",num2
    return 0
    
def complexitymetrics(db,num):
    cyclomaticmetrics(db,num)
    score = dfsnum
    return score

def vulnerabilitymetrics(db,num):
    score = ifwithoutelse(db,num) + paravar(db,num) + pointerscore(db,num) + \
            varsincontrolpred(db,num) + varmaxpointerinv(db,num) +  \
            nested_control_structures(db,num) + control_dependent(db,num) + datadependent(db,num)
    return score

def dfs_find_maxnum_control(db,x):
	global flag
	global ch
	flag.append(x)
	num=1
	query_str="""g.v(%s).out('CONTROLS').id"""%(x)
	child_node = db.runGremlinQuery(query_str)
	for node in child_node:
		if (node in ch)and(not(node in flag)):
			num+=dfs_find_maxnum_control(db,node)		
	return num
			 
def  control_dependent(db,num):
    query_str="queryNodeIndex('functionId:(%s) AND isCFGNode:True AND type:CFGEntryNode').id" % (num)
    startid = db.runGremlinQuery(query_str) 
    #print startid
    query_str="""getNodesWithType("Condition").id""" 
    results = db.runGremlinQuery(query_str) 
    global ch
    ch=results
    query_str="""g.v(%s).out('CONTROLS').id""" % (startid[0]) 
    results = db.runGremlinQuery(query_str)
    ans=0
    for node in results:
    	if (node in ch):
		    ans=max(ans,dfs_find_maxnum_control(db,node))
    return ans
def getFuncFile(db, func_id):
    query_str = "g.v(%d).in('IS_FILE_OF').filepath" % func_id
    ret = db.runGremlinQuery(query_str)
    print >>f,ret
    #print ret
    return ret[0]


if __name__ == '__main__':
    f = open("out.txt", "a+")
    j = JoernSteps()
    j.connectToDatabase()
    all_func_node = getALLFuncNode(j)
    for node in all_func_node:
    	print >>f,node
    	getFuncFile(j, node._id)
    	print >>f,"Cyclomatic complexity:",complexitymetrics(j,node._id)
    	print >>f,"The num of loops:",loopsnum(j,node._id)
    	nestedloops(j,node._id)
    	print >>f,"The num of parameter variables:",paravar(j,node._id)
    	print >>f,"The num of variables as parameters for callee function:",calleeparavar(j,node._id)
    	print >>f,"The num of if structures without else:",ifwithoutelse(j,node._id)
    	
    	pointerscore(j,node._id)
    	nested_control_structures(j,node._id)
    	#cyclomaticmetrics(j,node._id)
    	print >>f,"Maximum of control-dependent control structures:",control_dependent(j,node._id)
    	print >>f,"Maximum of data-dependent control structures:",datadependent(j,node._id)
    	print >>f,"of variables involved in control predicates:",varsincontrolpred(j,node._id)
    f.close
