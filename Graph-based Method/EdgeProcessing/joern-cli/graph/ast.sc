/* 
生成ast图
*/

import gremlin.scala.{Edge, GremlinScala}

import io.shiftleft.codepropertygraph.generated.EdgeTypes

import scala.collection.mutable

import java.io.{PrintWriter, File => JFile}
import java.io.{File}

type aEdgeEntry = (AnyRef, AnyRef,Int)
type aVertexEntry = (AnyRef, String)
//type ast = (Option[String], List[aEdgeEntry], List[aVertexEntry])

//type r = (List[ast],List[cfg],List[pdg])
type r = (Option[String], List[aEdgeEntry], List[aVertexEntry])

private def astFromEdges(edges: GremlinScala[Edge]): (List[aEdgeEntry], List[aVertexEntry]) = {
  val filteredEdges = edges.filter(edge => edge.hasLabel(EdgeTypes.REACHING_DEF, EdgeTypes.AST)).dedup.l

  val (edgeResult, vertexResult) =
    filteredEdges.foldLeft((mutable.Set.empty[aEdgeEntry], mutable.Set.empty[aVertexEntry])) {
      case ((edgeList, vertexList), edge) =>
        val edgeEntry = (edge.inVertex().id, edge.outVertex().id,0)
        val inVertexEntry = (edge.inVertex().id, edge.inVertex().property("CODE").orElse(""))
        val outVertexEntry = (edge.outVertex().id, edge.outVertex().property("CODE").orElse(""))

        (edgeList += edgeEntry, vertexList ++= Set(inVertexEntry, outVertexEntry))
    }

  (edgeResult.toList, vertexResult.toList)
}

//type r = (Option[String], List[aEdgeEntry], List[aVertexEntry], List[cEdgeEntry], List[cVertexEntry],List[pEdgeEntry], List[pVertexEntry])


def result(methodRegex: String = ""): List[r] = {
  if (methodRegex.isEmpty) {
    val (aedgeEntries, avertexEntries) = astFromEdges(cpg.scalaGraph.E())
    List((None, aedgeEntries, avertexEntries))
  } else {
    cpg.method(methodRegex).l.map { method =>
      val methodFile = method.location.filename+"-"+method.name
      val (aedgeEntries, avertexEntries) = astFromEdges(method.asScala.out().flatMap(_.asScala.outE()))

      (Some(methodFile), aedgeEntries, avertexEntries)
    }
  }
}


@main def main()= {

  var item = 0
  val list = result(".*")
  println(list.length)
  //Please modify the path of the result
  val dirPath = "raw_nvd//bad_ast"
  val resultPath = new File(dirPath)
  resultPath.mkdirs()

  for (item <- list){
        var filename=BigInt(100, scala.util.Random).toString(36)
	val writer = new PrintWriter(new JFile(dirPath+"//"+filename+".txt"))
	writer.println(item)
        writer.close()
  }
  
}
