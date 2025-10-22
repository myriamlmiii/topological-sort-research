"""
MERIEM - Unit Tests for DFS-based Algorithm
Comprehensive testing with cycle detection and validation
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from algorithms.dfs import topological_sort_dfs
from algorithms.kahn import validate_topological_order

class TestDFSAlgorithm:
    """Test suite for DFS-based topological sort algorithm"""
    
    def test_linear_dependencies(self):
        """Test simple linear dependency chain"""
        graph = {
            'A': ['B'],
            'B': ['C'],
            'C': []
        }
        result, metrics = topological_sort_dfs(graph)
        is_valid, message = validate_topological_order(graph, result)
        assert is_valid, message
        assert len(result) == 3
        print("✓ Linear dependencies test passed")
    
    def test_multiple_valid_orders(self):
        """Test graphs with multiple valid topological orders"""
        graph = {
            'A': ['C'],
            'B': ['C'],
            'C': []
        }
        result, metrics = topological_sort_dfs(graph)
        is_valid, message = validate_topological_order(graph, result)
        assert is_valid, message
        assert len(result) == 3
        print("✓ Multiple valid orders test passed")
    
    def test_cycle_detection(self):
        """Test cycle detection using recursion stack"""
        graph = {
            'A': ['B'],
            'B': ['C'],
            'C': ['A']
        }
        try:
            topological_sort_dfs(graph)
            assert False, "Should have detected cycle"
        except ValueError as e:
            assert "cycle" in str(e).lower()
            print("✓ Cycle detection test passed")
    
    def test_self_loop(self):
        """Test self-loop cycle detection"""
        graph = {'A': ['A']}
        try:
            topological_sort_dfs(graph)
            assert False, "Should have detected self-loop"
        except ValueError as e:
            assert "cycle" in str(e).lower()
            print("✓ Self-loop detection test passed")
    
    def test_complex_structure(self):
        """Test complex graph structure"""
        graph = {
            'A': ['B', 'C'],
            'B': ['D'],
            'C': ['E', 'F'],
            'D': ['G'],
            'E': ['G'],
            'F': ['H'],
            'G': [],
            'H': []
        }
        result, metrics = topological_sort_dfs(graph)
        is_valid, message = validate_topological_order(graph, result)
        assert is_valid, message
        assert len(result) == 8
        print("✓ Complex structure test passed")
    
    def test_disconnected_graph(self):
        """Test graph with disconnected components"""
        graph = {
            'A': ['B'],
            'B': ['C'],
            'C': [],
            'D': ['E'],
            'E': []
        }
        result, metrics = topological_sort_dfs(graph)
        is_valid, message = validate_topological_order(graph, result)
        assert is_valid, message
        assert len(result) == 5
        print("✓ Disconnected graph test passed")
    
    def test_research_data(self):
        """Test algorithm on actual research citation graph"""
        from data.research_data import get_citation_graph
        
        graph = get_citation_graph()
        result, metrics = topological_sort_dfs(graph)
        
        is_valid, message = validate_topological_order(graph, result)
        assert is_valid, message
        assert len(result) == 10
        print("✓ Research data test passed")
    
    def test_performance_metrics(self):
        """Test that performance metrics are collected correctly"""
        graph = {
            'A': ['B', 'C'],
            'B': ['D'],
            'C': ['D'],
            'D': []
        }
        result, metrics = topological_sort_dfs(graph)
        
        assert 'execution_time_ms' in metrics
        assert 'vertices' in metrics
        assert 'edges' in metrics
        assert 'actual_operations' in metrics
        assert metrics['vertices'] == 4
        assert metrics['edges'] == 4
        print("✓ Performance metrics test passed")

def run_all_tests():
    """Run all DFS algorithm tests"""
    print("=== RUNNING DFS ALGORITHM TESTS ===")
    test_suite = TestDFSAlgorithm()
    
    tests = [
        test_suite.test_linear_dependencies,
        test_suite.test_multiple_valid_orders,
        test_suite.test_cycle_detection,
        test_suite.test_self_loop,
        test_suite.test_complex_structure,
        test_suite.test_disconnected_graph,
        test_suite.test_research_data,
        test_suite.test_performance_metrics
    ]
    
    passed = 0
    for test in tests:
        try:
            test()
            passed += 1
        except Exception as e:
            print(f"✗ {test.__name__} failed: {e}")
    
    print(f"\nTEST RESULTS: {passed}/{len(tests)} tests passed")
    return passed == len(tests)

if __name__ == "__main__":
    success = run_all_tests()
    if success:
        print("\nSUCCESS: All DFS algorithm tests passed!")
    else:
        print("\nFAILURE: Some tests failed!")
        sys.exit(1)