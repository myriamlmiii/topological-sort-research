"""
MERIEM - DFS-based Algorithm Implementation
Topological sort using depth-first search with recursion stack
"""

from typing import Dict, List, Set, Tuple
import time

def topological_sort_dfs(graph: Dict[str, List[str]]) -> Tuple[List[str], Dict]:
    """
    Perform topological sort using DFS with cycle detection.
    """
    if not graph:
        return [], {
            'execution_time_ms': 0.0,
            'vertices': 0,
            'edges': 0,
            'theoretical_operations': 0,
            'actual_operations': 0,
            'space_complexity': 0,
            'recursion_depth': 0
        }
    
    start_time = time.perf_counter()
    
    visited: Set[str] = set()
    recursion_stack: Set[str] = set()
    result_stack: List[str] = []
    
    # Count operations for complexity analysis
    operations = 0
    edge_count = 0
    
    def dfs(node: str) -> None:
        nonlocal operations, edge_count
        
        # Cycle detection
        if node in recursion_stack:
            raise ValueError(f"Cycle detected involving node: {node}")
        
        if node in visited:
            return
        
        # Mark as visiting
        recursion_stack.add(node)
        visited.add(node)
        operations += 1
        
        # Recursively visit all neighbors
        for neighbor in graph.get(node, []):
            edge_count += 1
            dfs(neighbor)
        
        # Remove from recursion stack and add to result
        recursion_stack.remove(node)
        result_stack.append(node)
        operations += 1
    
    # Perform DFS from all unvisited nodes
    for node in list(graph.keys()):
        if node not in visited:
            dfs(node)
    
    # Reverse for topological order
    result = result_stack[::-1]
    
    end_time = time.perf_counter()
    execution_time = (end_time - start_time) * 1000
    
    # Calculate complexity metrics
    V = len(graph)
    E = edge_count
    actual_operations = operations
    
    return result, {
        'execution_time_ms': execution_time,
        'vertices': V,
        'edges': E,
        'theoretical_operations': V + E,
        'actual_operations': actual_operations,
        'space_complexity': V,
        'recursion_depth': len(recursion_stack)
    }