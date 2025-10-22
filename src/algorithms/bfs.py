"""
LOREENA - BFS-based Algorithm Implementation
Topological sort using breadth-first search with level tracking
"""

from collections import deque
from typing import Dict, List, Tuple
import time

def topological_sort_bfs(graph: Dict[str, List[str]]) -> Tuple[List[str], Dict[str, int], Dict]:
    """
    Perform topological sort using BFS with level tracking.
    
    Time Complexity Analysis:
    - Initialization: O(V) for in-degree initialization
    - In-degree calculation: O(E) for processing all edges
    - Level-based processing: O(V + E) for processing all nodes and edges
    - Total: O(V + E)
    
    Space Complexity: O(V) for in-degree storage, queue, and level tracking
    """
    if not graph:
        return [], {}, {}
    
    start_time = time.perf_counter()
    
    # Initialize in-degree for all nodes: O(V)
    in_degree = {}
    for node in graph:
        in_degree[node] = 0
    
    # Calculate actual in-degrees: O(E)
    edge_count = 0
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] = in_degree.get(neighbor, 0) + 1
            edge_count += 1
    
    # Initialize queue with nodes having 0 in-degree: O(V)
    queue = deque([node for node in in_degree if in_degree[node] == 0])
    result = []
    levels = {node: 0 for node in in_degree}
    
    # Process nodes level by level: O(V + E)
    current_level = 0
    processed_nodes = 0
    max_queue_size = len(queue)
    
    while queue:
        level_size = len(queue)
        max_queue_size = max(max_queue_size, len(queue))
        
        # Process all nodes at current level
        for _ in range(level_size):
            current = queue.popleft()
            result.append(current)
            levels[current] = current_level
            processed_nodes += 1
            
            # Update neighbors: O(degree(current))
            for neighbor in graph.get(current, []):
                in_degree[neighbor] -= 1
                if in_degree[neighbor] == 0:
                    queue.append(neighbor)
        
        current_level += 1
    
    # Check for cycles
    if len(result) != len(in_degree):
        raise ValueError("Graph contains a cycle - topological sort impossible")
    
    end_time = time.perf_counter()
    execution_time = (end_time - start_time) * 1000
    
    # Calculate complexity metrics
    V = len(graph)
    E = edge_count
    actual_operations = V + E
    
    return result, levels, {
        'execution_time_ms': execution_time,
        'vertices': V,
        'edges': E,
        'theoretical_operations': V + E,
        'actual_operations': actual_operations,
        'space_complexity': V,
        'max_level': current_level - 1,
        'max_queue_size': max_queue_size
    }

def analyze_dependency_levels(levels: Dict[str, int]) -> Dict[int, List[str]]:
    """Analyze and group nodes by their dependency levels."""
    level_groups = {}
    for node, level in levels.items():
        if level not in level_groups:
            level_groups[level] = []
        level_groups[level].append(node)
    return level_groups