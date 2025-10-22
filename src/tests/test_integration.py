"""
MERIEM - Integration Tests
Comprehensive testing of all algorithms together
"""

import sys
import os
import time
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

from algorithms.kahn import topological_sort_kahn, validate_topological_order
from algorithms.dfs import topological_sort_dfs
from algorithms.bfs import topological_sort_bfs
from data.research_data import get_citation_graph, get_paper_metadata

class TestIntegration:
    """Integration test suite for all topological sort algorithms"""
    
    def test_all_algorithms_consistency(self):
        """Test that all algorithms produce valid topological orders"""
        print("Testing algorithm consistency...")
        
        graph = get_citation_graph()
        
        algorithms = [
            ("Kahn's Algorithm", topological_sort_kahn),
            ("DFS Algorithm", topological_sort_dfs),
            ("BFS Algorithm", topological_sort_bfs)
        ]
        
        results = {}
        for name, algorithm in algorithms:
            try:
                if name == "BFS Algorithm":
                    result, levels, metrics = algorithm(graph)
                else:
                    result, metrics = algorithm(graph)
                
                is_valid, message = validate_topological_order(graph, result)
                results[name] = {
                    'result': result,
                    'valid': is_valid,
                    'message': message,
                    'length': len(result)
                }
                print(f"  ✓ {name}: {len(result)} papers, valid={is_valid}")
            except Exception as e:
                results[name] = {
                    'result': None,
                    'valid': False,
                    'message': str(e),
                    'length': 0
                }
                print(f"  ✗ {name}: ERROR - {e}")
        
        # All algorithms should produce valid results
        for name, data in results.items():
            assert data['valid'], f"{name} produced invalid order: {data['message']}"
            assert data['length'] == 10, f"{name} should process 10 papers"
        
        print("✓ All algorithms produce consistent valid results")
    
    def test_performance_comparison(self):
        """Compare performance of all three algorithms"""
        print("Running performance comparison...")
        
        graph = get_citation_graph()
        
        algorithms = [
            ("Kahn's Algorithm", topological_sort_kahn),
            ("DFS Algorithm", topological_sort_dfs),
            ("BFS Algorithm", topological_sort_bfs)
        ]
        
        performance_data = {}
        iterations = 100
        
        for name, algorithm in algorithms:
            times = []
            
            # Warm up
            for _ in range(10):
                if name == "BFS Algorithm":
                    result, levels, metrics = algorithm(graph)
                else:
                    result, metrics = algorithm(graph)
            
            # Performance measurement
            for _ in range(iterations):
                start_time = time.perf_counter()
                if name == "BFS Algorithm":
                    result, levels, metrics = algorithm(graph)
                else:
                    result, metrics = algorithm(graph)
                end_time = time.perf_counter()
                times.append((end_time - start_time) * 1_000_000)  # microseconds
            
            avg_time = sum(times) / len(times)
            performance_data[name] = {
                'avg_time_us': avg_time,
                'min_time_us': min(times),
                'max_time_us': max(times)
            }
            
            print(f"  {name}: {avg_time:.2f} μs average")
        
        # All algorithms should complete in reasonable time
        for name, data in performance_data.items():
            assert data['avg_time_us'] < 1000, f"{name} is too slow: {data['avg_time_us']:.2f} μs"
        
        print("✓ All algorithms perform within acceptable limits")
    
    def test_reading_schedule_generation(self):
        """Test generation of meaningful reading schedule"""
        print("Testing reading schedule generation...")
        
        graph = get_citation_graph()
        metadata = get_paper_metadata()
        
        # Generate reading schedule using Kahn's algorithm
        result, metrics = topological_sort_kahn(graph)
        
        # Validate the reading order makes sense
        is_valid, message = validate_topological_order(graph, result)
        assert is_valid, message
        assert len(result) == 10
        
        # Check that foundational papers exist and are in the order
        foundational = [paper for paper in graph if not graph[paper]]
        assert len(foundational) > 0, "Should have foundational papers"
        
        # All foundational papers should be in the result
        for foundation in foundational:
            assert foundation in result, f"Foundation paper {foundation} should be in reading order"
        
        print("✓ Reading schedule is logically structured")
    
    def test_dependency_level_analysis(self):
        """Test dependency level analysis for research papers"""
        print("Testing dependency level analysis...")
        
        graph = get_citation_graph()
        result, levels, metrics = topological_sort_bfs(graph)
        
        # Analyze level distribution
        from algorithms.bfs import analyze_dependency_levels
        level_groups = analyze_dependency_levels(levels)
        
        # Should have multiple dependency levels
        assert len(level_groups) > 1, "Research should have multiple dependency levels"
        
        # In BFS topological sort, level 0 contains the MOST DEPENDENT papers
        # (those that depend on many others), and higher levels contain more foundational papers
        max_level = max(level_groups.keys())
        level_max_papers = level_groups.get(max_level, [])
        assert len(level_max_papers) > 0, f"Should have papers at highest dependency level {max_level}"
        
        # Foundational papers (no dependencies) should be at the HIGHEST level
        foundational = [paper for paper in graph if not graph[paper]]
        for foundation in foundational:
            assert foundation in result, f"Foundation paper {foundation} should be in result"
            # Foundation papers should be at the highest level (most foundational)
            assert levels[foundation] == max_level, f"Foundation paper {foundation} should be at highest level {max_level}, but is at level {levels[foundation]}"
        
        print(f"  Dependency levels: {[f'Level {k}: {len(v)} papers' for k, v in level_groups.items()]}")
        print(f"  Highest level ({max_level}) contains foundational papers: {level_max_papers}")
        print("✓ Dependency level analysis works correctly")
    
    def test_error_handling(self):
        """Test error handling across all algorithms"""
        print("Testing error handling...")
        
        # Test cycle detection
        cyclic_graph = {
            'A': ['B'],
            'B': ['C'],
            'C': ['A']
        }
        
        algorithms = [
            ("Kahn's Algorithm", topological_sort_kahn),
            ("DFS Algorithm", topological_sort_dfs),
            ("BFS Algorithm", topological_sort_bfs)
        ]
        
        for name, algorithm in algorithms:
            try:
                if name == "BFS Algorithm":
                    result, levels, metrics = algorithm(cyclic_graph)
                else:
                    result, metrics = algorithm(cyclic_graph)
                assert False, f"{name} should have detected cycle"
            except ValueError as e:
                assert "cycle" in str(e).lower()
                print(f"  ✓ {name} correctly detects cycles")
        
        print("✓ All algorithms handle errors properly")

def run_integration_tests():
    """Run all integration tests"""
    print("=== RUNNING INTEGRATION TESTS ===")
    test_suite = TestIntegration()
    
    tests = [
        test_suite.test_all_algorithms_consistency,
        test_suite.test_performance_comparison,
        test_suite.test_reading_schedule_generation,
        test_suite.test_dependency_level_analysis,
        test_suite.test_error_handling
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
    success = run_integration_tests()
    if success:
        print("\nSUCCESS: All integration tests passed!")
        print("SYSTEM IS READY FOR PRODUCTION USE!")
    else:
        print("\nFAILURE: Some integration tests failed!")
        sys.exit(1)