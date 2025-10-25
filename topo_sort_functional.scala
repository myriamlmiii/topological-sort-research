object TopologicalSortFunctional {

  /**
   * Finds a topological ordering of a DAG using Kahn's algorithm in a purely functional style.
   */
  def topologicalSort(graph: Vector[List[Int]]): Option[List[Int]] = {

    // Compute initial in-degrees
    val inDegree: Map[Int, Int] = graph.indices
      .flatMap(i => graph(i).map(to => (to, 1)))
      .groupMapReduce(_._1)(_ => 1)(_ + _)
      .withDefaultValue(0)
    val zeroInDegree = graph.indices.filter(i => inDegree(i) == 0).toList

    def process(queue: List[Int], deg: Map[Int, Int], acc: List[Int]): Option[List[Int]] = queue match {
      case Nil =>
        if (acc.length == graph.length) Some(acc.reverse) 
        else None 
      case head :: tail =>
        val neighbors = graph(head)
        val updatedDeg = neighbors.foldLeft(deg) { case (m, to) =>
          m.updated(to, m(to) - 1)
        }
        val newZeroInDegree = neighbors.filter(to => updatedDeg(to) == 0)
        process(tail ++ newZeroInDegree, updatedDeg, head :: acc)
    }

    process(zeroInDegree, inDegree, Nil)
  }
    // Papers I am interested to read
  def main(args: Array[String]): Unit = {
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
    val n = citations.length
    val graph: Vector[List[Int]] =
      Vector.tabulate(n)(i => edges.collect { case (from, to) if from == i => to })

    val startTime = System.nanoTime()

    topologicalSort(graph) match {
      case Some(order) =>
        println("Topological Order (indices): " + order.mkString(" "))
        println("Topological Order (citations): " + order.map(citations).mkString(" --> "))
      case None =>
        println("Graph contains a cycle.")
    }

    val endTime = System.nanoTime()
    val durationMs = (endTime - startTime) / 1e6 // convert ns to ms
    println(f"Topological sort took $durationMs%.3f ms")

    // Bulk testing the timing
    val iterations = 10000
    val startTimeBulk = System.nanoTime()

    for (_ <- 1 to iterations) {
      topologicalSort(graph)
    }

    val endTimeBulk = System.nanoTime()
    val totalMs = (endTimeBulk - startTimeBulk) / 1e6
    val avgMs = totalMs / iterations

    println(f"Ran topological sort $iterations times")
    println(f"Total time: $totalMs%.3f ms")
    println(f"Average time per run: $avgMs%.3f ms")

  }
}
