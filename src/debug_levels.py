"""
Everyone
Debug script to check BFS levels for research papers
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.bfs import topological_sort_bfs, analyze_dependency_levels
from data.research_data import get_citation_graph, get_paper_metadata

def debug_levels():
    """Debug the BFS level assignment"""
    graph = get_citation_graph()
    metadata = get_paper_metadata()
    
    print("DEBUG: CITATION GRAPH")
    print("=" * 60)
    for paper, deps in graph.items():
        title_short = metadata[paper]['title'][:40] + "..." if len(metadata[paper]['title']) > 40 else metadata[paper]['title']
        print(f"{paper}: {deps} - {title_short}")
    
    print("\nDEBUG: BFS LEVEL ANALYSIS")
    print("=" * 60)
    result, levels, metrics = topological_sort_bfs(graph)
    
    level_groups = analyze_dependency_levels(levels)
    
    for level in sorted(level_groups.keys()):
        papers = level_groups[level]
        print(f"\nLEVEL {level} ({len(papers)} papers):")
        for paper in papers:
            title_short = metadata[paper]['title'][:50] + "..." if len(metadata[paper]['title']) > 50 else metadata[paper]['title']
            dependencies = graph[paper]
            print(f"  {paper}: depends on {dependencies} - {title_short}")
    
    # Check foundational papers
    foundational = [paper for paper in graph if not graph[paper]]
    print(f"\nFOUNDATIONAL PAPERS (no dependencies): {foundational}")
    for paper in foundational:
        print(f"  {paper}: level {levels[paper]}")

if __name__ == "__main__":
    debug_levels()