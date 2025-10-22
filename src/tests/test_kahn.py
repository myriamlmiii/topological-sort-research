"""
CHARVI - Unit Tests for Kahn's Algorithm
Comprehensive testing with various graph structures
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from algorithms.kahn import topological_sort_kahn, validate_topological_order

class TestKahnAlgorithm:
    """Test suite for Kahn's topological sort algorithm"""
    
    def test_linear_dependencies(self):
        """Test simple linear dependency chain A→B→C"""
        graph = {
            'A': ['B'],
            'B': ['C'], 
            'C': []
        }
        result, metrics = topological_sort_kahn(graph)
        is_valid, message = validate_topological_order(graph, result)
        assert is_valid, message
        assert len(result) == 3
        print("✓ Linear dependencies test passed")
    
    def test_diamond_dependencies(self):
        """Test diamond-shaped dependencies A→B→D, A→C→D"""
        graph = {
            'A': ['B', 'C'],
            'B': ['D'],
            'C': ['D'],
            'D': []
        }
        result, metrics = topological_sort_kahn(graph)
        is_valid, message = validate_topological_order(graph, result)
        assert is_valid, message
        assert result[0] == 'A'
        assert result[-1] == 'D'
        print("✓ Diamond dependencies test passed")
    
    def test_multiple_components(self):
        """Test graph with disconnected components"""
        graph = {
            'A': ['B'],
            'B': [],
            'C': ['D'],
            'D': []
        }
        result, metrics = topological_sort_kahn(graph)
        is_valid, message = validate_topological_order(graph, result)
        assert is_valid, message
        assert len(result) == 4
        print("✓ Multiple components test passed")
    
    def test_cycle_detection(self):
        """Test that cycles are properly detected"""
        graph = {
            'A': ['B'],
            'B': ['C'],
            'C': ['A']  # Cycle: A→B→C→A
        }
        try:
            topological_sort_kahn(graph)
            assert False, "Should have detected cycle"
        except ValueError as e:
            assert "cycle" in str(e).lower()
            print("✓ Cycle detection test passed")
    
    def test_empty_graph(self):
        """Test empty graph handling"""
        graph = {}
        result, metrics = topological_sort_kahn(graph)
        assert result == []
        print("✓ Empty graph test passed")
    
    def test_single_node(self):
        """Test graph with single node"""
        graph = {'A': []}
        result, metrics = topological_sort_kahn(graph)
        assert result == ['A']
        print("✓ Single node test passed")
    
    def test_complex_dag(self):
        """Test complex directed acyclic graph"""
        graph = {
            'A': ['B', 'C'],
            'B': ['D', 'E'],
            'C': ['F'],
            'D': ['G'],
            'E': ['G'],
            'F': ['G'],
            'G': []
        }
        result, metrics = topological_sort_kahn(graph)
        is_valid, message = validate_topological_order(graph, result)
        assert is_valid, message
        assert len(result) == 7
        print("✓ Complex DAG test passed")
    
    def test_research_data(self):
        """Test algorithm on actual research citation graph"""
        from data.research_data import get_citation_graph
        
        graph = get_citation_graph()
        result, metrics = topological_sort_kahn(graph)
        
        is_valid, message = validate_topological_order(graph, result)
        assert is_valid, message
        assert len(result) == 10
        print("✓ Research data test passed")

def run_all_tests():
    """Run all Kahn's algorithm tests"""
    print("=== RUNNING KAHN'S ALGORITHM TESTS ===")
    test_suite = TestKahnAlgorithm()
    
    tests = [
        test_suite.test_linear_dependencies,
        test_suite.test_diamond_dependencies,
        test_suite.test_multiple_components,
        test_suite.test_cycle_detection,
        test_suite.test_empty_graph,
        test_suite.test_single_node,
        test_suite.test_complex_dag,
        test_suite.test_research_data
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
        print("\nSUCCESS: All Kahn's algorithm tests passed!")
    else:
        print("\nFAILURE: Some tests failed!")
        sys.exit(1)