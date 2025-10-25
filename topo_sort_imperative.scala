import scala.collection.mutable

object TopologicalSortKahn {

  /**
   * Finds a topological ordering of a directed acyclic graph.
   * 
   */
  def findTopologicalOrdering(g: Array[List[Int]]): Option[List[Int]] = {
    val n = g.length
    val inDegree = Array.fill(n)(0)
    for (i <- 0 until n; to <- g(i)) {
      inDegree(to) += 1
    }
    val q = scala.collection.mutable.Queue[Int]()
    for (i <- 0 until n if inDegree(i) == 0) {
      q.enqueue(i)
    }
    val order = scala.collection.mutable.ListBuffer[Int]()
    var index = 0

    // Process queue
    while (q.nonEmpty) {
      val at = q.dequeue()
      order += at
      index += 1

      for (to <- g(at)) {
        inDegree(to) -= 1
        if (inDegree(to) == 0) q.enqueue(to)
      }
    }
    if (index != n) None else Some(order.toList)
  }

  // ---------- Example ----------
  def main(args: Array[String]): Unit = {
    val n = 10
    val graph = Array.fill(n)(List[Int]())
    
    val citations = Array(
        "Shcherbakova, 2017", 
        "Kah, 2019", 
        "Mittal, 2020", 
        "Wang, 2021", 
        "Nongbet, 2022", 
        "Mohammadi, 2023", 
        "Goyal, 2023", 
        "Mgadi, 2024", 
        "Arora, 2024",
        "Quintarelli, 2024"
        )
        
    
    val edges = List(
      (9,8),
      (9,7),
      (7,5),
      (5,3),
      (6,4),
      (7,6),
      (6,1),
      (4,2),
      (4,0),
      (2,1),
      (1,0)  
    )

    for ((u, v) <- edges) {
      graph(u) = graph(u) :+ v
    }

    findTopologicalOrdering(graph) match {
      case Some(order) =>
        println("Topological Order: " + order.mkString(" "))
        for (index <- order) {
                print(citations(index) + " --> ")
         }

      case None =>
        println("Graph contains a cycle")
    }
        // Bulk testing the timing
        val iterations = 10000
        val startTimeBulk = System.nanoTime()

        for (_ <- 1 to iterations) {
        findTopologicalOrdering(graph)
        }

        val endTimeBulk = System.nanoTime()
        val totalMs = (endTimeBulk - startTimeBulk) / 1e6
        val avgMs = totalMs / iterations

        println(f"Ran topological sort $iterations times")
        println(f"Total time: $totalMs%.3f ms")
        println(f"Average time per run: $avgMs%.3f ms")
  }

}
