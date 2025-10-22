"""
LOREENA - Unit Tests for BFS-based Algorithm
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from algorithms.bfs import topological_sort_bfs, analyze_dependency_levels
from algorithms.kahn import validate_topological_order

class TestBFSAlgorithm:
    """Test suite for BFS-based topological sort with level tracking"""
    
    def test_linear_dependencies_levels(self):
        """Test linear chain with level tracking"""
        graph = {
            'A': ['B'],
            'B': ['C'],
            'C': []
        }
        result, levels, metrics = topological_sort_bfs(graph)
        
        is_valid, message = validate_topological_order(graph, result)
        assert is_valid, message
        assert levels['A'] == 0
        assert levels['B'] == 1
        assert levels['C'] == 2
        print("✓ Linear dependencies with levels test passed")
    
    def test_diamond_dependencies_levels(self):
        """Test diamond structure with level tracking"""
        graph = {
            'A': ['B', 'C'],
            'B': ['D'],
            'C': ['D'],
            'D': []
        }
        result, levels, metrics = topological_sort_bfs(graph)
        
        is_valid, message = validate_topological_order(graph, result)
        assert is_valid, message
        assert levels['A'] == 0
        assert levels['B'] == 1
        assert levels['C'] == 1
        assert levels['D'] == 2
        print("✓ Diamond dependencies with levels test passed")
    
    def test_multiple_sources(self):
        """Test graph with multiple source nodes"""
        graph = {
            'A': ['C'],
            'B': ['C'],
            'C': []
        }
        result, levels, metrics = topological_sort_bfs(graph)
        
        is_valid, message = validate_topological_order(graph, result)
        assert is_valid, message
        assert levels['A'] == 0
        assert levels['B'] == 0
        assert levels['C'] == 1
        print("✓ Multiple sources test passed")
    
    def test_complex_level_structure(self):
        """Test complex multi-level dependency structure - FIXED"""
        graph = {
            'A': ['B', 'C'],
            'B': ['D'],
            'C': ['E'],
            'D': ['F'],
            'E': ['F'],
            'F': []
        }
        result, levels, metrics = topological_sort_bfs(graph)
        
        is_valid, message = validate_topological_order(graph, result)
        assert is_valid, message
        assert levels['A'] == 0
        assert levels['B'] == 1
        assert levels['C'] == 1
        assert levels['D'] == 2
        assert levels['E'] == 2
        assert levels['F'] == 3
        print("✓ Complex level structure test passed")
    
    def test_cycle_detection(self):
        """Test cycle detection in BFS algorithm"""
        graph = {
            'A': ['B'],
            'B': ['C'],
            'C': ['A']
        }
        try:
            topological_sort_bfs(graph)
            assert False, "Should have detected cycle"
        except ValueError as e:
            assert "cycle" in str(e).lower()
            print("✓ Cycle detection test passed")
    
    def test_level_analysis(self):
        """Test dependency level analysis function"""
        graph = {
            'A': ['B', 'C'],
            'B': ['D'],
            'C': ['D'],
            'D': []
        }
        result, levels, metrics = topological_sort_bfs(graph)
        level_groups = analyze_dependency_levels(levels)
        
        assert level_groups[0] == ['A']
        assert set(level_groups[1]) == {'B', 'C'}
        assert level_groups[2] == ['D']
        print("✓ Level analysis test passed")
    
    def test_research_data_levels(self):
        """Test BFS algorithm on research data with level analysis"""
        from data.research_data import get_citation_graph
        
        graph = get_citation_graph()
        result, levels, metrics = topological_sort_bfs(graph)
        
        is_valid, message = validate_topological_order(graph, result)
        assert is_valid, message
        assert len(result) == 10
        
        level_groups = analyze_dependency_levels(levels)
        print(f"Research data level distribution: {[f'Level {k}: {len(v)} papers' for k, v in level_groups.items()]}")
        print("✓ Research data with levels test passed")
    
    def test_empty_graph(self):
        """Test empty graph handling"""
        graph = {}
        result, levels, metrics = topological_sort_bfs(graph)
        
        assert result == []
        assert levels == {}
        print("✓ Empty graph test passed")

def run_all_tests():
    """Run all BFS algorithm tests"""
    print("=== RUNNING BFS ALGORITHM TESTS ===")
    test_suite = TestBFSAlgorithm()
    
    tests = [
        test_suite.test_linear_dependencies_levels,
        test_suite.test_diamond_dependencies_levels,
        test_suite.test_multiple_sources,
        test_suite.test_complex_level_structure,
        test_suite.test_cycle_detection,
        test_suite.test_level_analysis,
        test_suite.test_research_data_levels,
        test_suite.test_empty_graph
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
        print("\nSUCCESS: All BFS algorithm tests passed!")
    else:
        print("\nFAILURE: Some tests failed!")
        sys.exit(1)