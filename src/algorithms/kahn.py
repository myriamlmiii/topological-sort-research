"""
CHARVI - Kahn's Algorithm Implementation
Topological sort using queue-based approach with in-degree counting
"""

from collections import deque
from typing import Dict, List, Tuple
import time

def topological_sort_kahn(graph: Dict[str, List[str]]) -> Tuple[List[str], Dict]:
    """
    Perform topological sort using Kahn's algorithm.
    """
    if not graph:
        return [], {
            'execution_time_ms': 0.0,
            'vertices': 0,
            'edges': 0,
            'theoretical_operations': 0,
            'actual_operations': 0,
            'space_complexity': 0
        }
    
    start_time = time.perf_counter()
    
    # Initialize in-degree for all nodes
    in_degree = {}
    for node in graph:
        in_degree[node] = 0
    
    # Calculate actual in-degrees
    edge_count = 0
    for node in graph:
        for neighbor in graph[node]:
            in_degree[neighbor] = in_degree.get(neighbor, 0) + 1
            edge_count += 1
    
    # Initialize queue with nodes having 0 in-degree
    queue = deque([node for node in in_degree if in_degree[node] == 0])
    result = []
    
    # Process nodes in topological order
    processed_nodes = 0
    while queue:
        current = queue.popleft()
        result.append(current)
        processed_nodes += 1
        
        # Update in-degree of neighbors
        for neighbor in graph.get(current, []):
            in_degree[neighbor] -= 1
            if in_degree[neighbor] == 0:
                queue.append(neighbor)
    
    # Check for cycles
    if len(result) != len(in_degree):
        remaining = set(in_degree.keys()) - set(result)
        raise ValueError(f"Graph contains cycle involving nodes: {remaining}")
    
    end_time = time.perf_counter()
    execution_time = (end_time - start_time) * 1000
    
    # Calculate complexity metrics
    V = len(graph)
    E = edge_count
    actual_operations = V + E
    
    return result, {
        'execution_time_ms': execution_time,
        'vertices': V,
        'edges': E,
        'theoretical_operations': V + E,
        'actual_operations': actual_operations,
        'space_complexity': V
    }

def validate_topological_order(graph: Dict[str, List[str]], order: List[str]) -> Tuple[bool, str]:
    """
    Validate that a topological order satisfies all dependencies.
    """
    if not order:
        return True, "Empty order is valid for empty graph"
    
    position = {node: idx for idx, node in enumerate(order)}
    
    for node in graph:
        for neighbor in graph[node]:
            if position[node] >= position[neighbor]:
                return False, f"Invalid order: {node} (position {position[node]}) should come before {neighbor} (position {position[neighbor]})"
    
    return True, "Valid topological order"