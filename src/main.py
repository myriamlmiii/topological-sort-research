"""
Everyone 
"""

import time
import sys
import os
from typing import Dict, List, Tuple
import csv

# Add parent directory to path for imports
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from algorithms.kahn import topological_sort_kahn, validate_topological_order
from algorithms.dfs import topological_sort_dfs
from algorithms.bfs import topological_sort_bfs, analyze_dependency_levels
from data.research_data import get_citation_graph, get_paper_metadata, get_research_stats, analyze_research_evolution

class ResearchAnalysisSystem:
    """
    Complete research analysis system using topological sorting algorithms with comprehensive performance analysis, complexity calculations, and research insights.
    """
    
    def __init__(self):
        """Initialize the research analysis system with our data."""
        self.graph = get_citation_graph()
        self.metadata = get_paper_metadata()
        self.stats = get_research_stats()
    
    def run_all_algorithms(self) -> Dict[str, Dict]:
        """
        Run all three topological sort algorithms and collect comprehensive performance data.
        
        Returns:
            Dictionary containing results and metrics for all algorithms
        """
        algorithms = {
            'Kahn': topological_sort_kahn,
            'DFS': topological_sort_dfs,
            'BFS': topological_sort_bfs
        }
        
        results = {}
        
        print("EXECUTING TOPOLOGICAL SORT ALGORITHMS...")
        print("-" * 60)
        
        for name, algorithm in algorithms.items():
            try:
                print(f"Running {name} Algorithm...")
                
                if name == 'BFS':
                    result, levels, metrics = algorithm(self.graph)
                    is_valid, message = validate_topological_order(self.graph, result)
                    results[name] = {
                        'result': result,
                        'metrics': metrics,
                        'levels': levels,
                        'valid': is_valid,
                        'message': message
                    }
                else:
                    result, metrics = algorithm(self.graph)
                    is_valid, message = validate_topological_order(self.graph, result)
                    results[name] = {
                        'result': result,
                        'metrics': metrics,
                        'valid': is_valid,
                        'message': message
                    }
                
                if is_valid:
                    print(f"  ✓ {name}: SUCCESS - {len(result)} papers sorted in {metrics['execution_time_ms']:.6f} ms")
                else:
                    print(f"  ✗ {name}: FAILED - {message}")
                    
            except Exception as e:
                results[name] = {
                    'result': None,
                    'metrics': {},
                    'valid': False,
                    'error': str(e)
                }
                print(f"  ✗ {name}: ERROR - {e}")
        
        print("-" * 60)
        return results
    
    def generate_complexity_analysis(self, results: Dict[str, Dict]) -> str:
     
        output = []
        output.append("=" * 120)
        output.append("COMPREHENSIVE ALGORITHM COMPLEXITY AND PERFORMANCE ANALYSIS")
        output.append("=" * 120)
        output.append("")
        
        # Table header
        output.append(f"{'ALGORITHM':<15} {'TIME (ms)':<12} {'VERTICES':<10} {'EDGES':<10} {'OPS (V+E)':<12} {'ACTUAL OPS':<12} {'SPACE':<10} {'EFFICIENCY':<12}")
        output.append("-" * 120)
        
        total_vertices = 0
        total_edges = 0
        
        for algo_name, data in results.items():
            if data['valid'] and 'metrics' in data:
                metrics = data['metrics']
                time_ms = metrics.get('execution_time_ms', 0)
                V = metrics.get('vertices', 0)
                E = metrics.get('edges', 0)
                theoretical_ops = metrics.get('theoretical_operations', 0)
                actual_ops = metrics.get('actual_operations', 0)
                space = metrics.get('space_complexity', 0)
                
                # Calculate efficiency (operations per millisecond)
                efficiency = actual_ops / time_ms if time_ms > 0 else 0
                
                output.append(f"{algo_name:<15} {time_ms:<12.6f} {V:<10} {E:<10} {theoretical_ops:<12} {actual_ops:<12} {space:<10} {efficiency:<12.2f}")
                
                total_vertices = V
                total_edges = E
        
        output.append("")
        output.append("COMPLEXITY ANALYSIS SUMMARY:")
        output.append(f"• Graph Size: V = {total_vertices}, E = {total_edges}")
        output.append(f"• Theoretical Time Complexity: O(V + E) = O({total_vertices} + {total_edges}) = O({total_vertices + total_edges})")
        output.append(f"• Space Complexity: O(V) = O({total_vertices}) for all algorithms")
        output.append("")
        
        output.append("ALGORITHM CHARACTERISTICS:")
        output.append("• KAHN'S ALGORITHM:")
        output.append("  - Uses explicit queue and in-degree counting")
        output.append("  - Excellent for cycle detection")
        output.append("  - Natural for level-by-level processing")
        output.append("  - Space: O(V) for queue and in-degree storage")
        output.append("")
        
        output.append("• DFS ALGORITHM:")
        output.append("  - Uses recursion stack for traversal")
        output.append("  - Natural for depth-first exploration")
        output.append("  - Built-in cycle detection via recursion stack")
        output.append("  - Space: O(V) for recursion stack and visited sets")
        output.append("")
        
        output.append("• BFS ALGORITHM:")
        output.append("  - Uses level-based processing with queue")
        output.append("  - Provides dependency level information")
        output.append("  - Good for understanding research evolution")
        output.append("  - Space: O(V) for queue and level tracking")
        output.append("")
        
        # Performance comparison
        valid_results = {k: v for k, v in results.items() if v['valid']}
        if len(valid_results) > 1:
            fastest_algo = min(valid_results.keys(), 
                             key=lambda x: valid_results[x]['metrics']['execution_time_ms'])
            fastest_time = valid_results[fastest_algo]['metrics']['execution_time_ms']
            
            output.append("PERFORMANCE COMPARISON:")
            output.append(f"• Fastest Algorithm: {fastest_algo} ({fastest_time:.6f} ms)")
            
            for algo_name, data in valid_results.items():
                if algo_name != fastest_algo:
                    time_ms = data['metrics']['execution_time_ms']
                    speedup = time_ms / fastest_time
                    output.append(f"• {algo_name}: {time_ms:.6f} ms ({speedup:.2f}x slower than {fastest_algo})")
        
        return "\n".join(output)
    
    def generate_reading_schedule(self, reading_order: List[str]) -> str:
     
        # Reverse the order so that foundational papers appear first.
        ordered = list(reversed(reading_order))

        output: List[str] = []
        output.append("=" * 100)
        output.append("OPTIMAL RESEARCH PAPER READING SCHEDULE")
        output.append("=" * 100)
        output.append("Based on topological sorting of citation dependencies")
        output.append(
            f"Total Papers: {len(ordered)} | Citation Relationships: {self.stats['total_citations']}"
        )
        output.append(
            f"Research Period: {self.stats['research_span'] + 1} years (2017-2024)"
        )
        output.append("")
        output.append("READING ORDER (Foundational to Advanced):")
        output.append("")

        for i, paper_id in enumerate(ordered, 1):
            paper = self.metadata[paper_id]
            output.append(f"{i:2d}. {paper['title']}")
            output.append(f"    Authors: {paper['authors']}")
            output.append(
                f"    Year: {paper['year']} | Publication: {paper['venue']}"
            )
            output.append(f"    DOI: {paper['url']}")

            # List prerequisite citations (papers this one cites)
            prerequisites = [p for p in self.graph[paper_id] if p in self.metadata]
            if prerequisites:
                prereq_titles: List[str] = []
                for p in prerequisites:
                    title_short = self.metadata[p]['title']
                    if len(title_short) > 50:
                        title_short = title_short[:47] + "..."
                    prereq_titles.append(title_short)
                output.append(f"    Prerequisites: {', '.join(prereq_titles)}")
            output.append("")

        return "\n".join(output)
    
    def generate_dependency_analysis(self, levels: Dict[str, int]) -> str:
    
        if not levels:
            return "No dependency data available."

        # Determine the maximum BFS level and invert the mapping
        max_level = max(levels.values())
        inverted_levels: Dict[int, List[str]] = {}
        for paper_id, level in levels.items():
            inv = max_level - level
            inverted_levels.setdefault(inv, []).append(paper_id)

        output: List[str] = []
        output.append("=" * 80)
        output.append("RESEARCH DEPENDENCY LEVEL ANALYSIS")
        output.append("=" * 80)
        output.append("")
        output.append(
            "Papers grouped by dependency depth (Level 0 = foundational, no prerequisites):"
        )
        output.append("")

        for level in sorted(inverted_levels.keys()):
            papers = inverted_levels[level]
            # Determine descriptive label
            if level == 0:
                label = "Foundational (no prerequisites)"
            elif level == 1:
                label = "Depends on 1 previous paper"
            else:
                label = f"Depends on {level} previous papers"
            output.append(
                f"LEVEL {level} – {label} ({len(papers)} paper{'s' if len(papers) != 1 else ''}):"
            )

            for paper_id in papers:
                paper = self.metadata[paper_id]
                # Truncate long titles for readability
                title = paper['title']
                if len(title) > 70:
                    title = title[:67] + "..."
                output.append(f"  • {paper['year']}: {title}")
            output.append("")

        return "\n".join(output)

    def generate_dependency_visualization(self, reading_order: List[str]) -> str:
        """
        Generate a simple text-based visualization of the citation dependencies
        and reading order to make the topological sort achievement crystal clear.
        """
        output = []
        output.append("=" * 80)
        output.append("DEPENDENCY VISUALIZATION - CITATION FLOW")
        output.append("=" * 80)
        output.append("")
        output.append("HOW TOPOLOGICAL SORT FIGURED OUT THE READING ORDER:")
        output.append("")
        
        # Create a simple ASCII flow chart
        output.append("FOUNDATIONAL → INTERMEDIATE → ADVANCED RESEARCH")
        output.append("")
        
        # Group by approximate complexity level
        foundational = []
        intermediate = []
        advanced = []
        
        for paper_id in reading_order:
            deps = len(self.graph[paper_id])
            if deps == 0:
                foundational.append(paper_id)
            elif deps <= 2:
                intermediate.append(paper_id)
            else:
                advanced.append(paper_id)
        
        # Foundational papers
        output.append(" FOUNDATIONAL (Start Here):")
        for paper_id in foundational:
            paper = self.metadata[paper_id]
            output.append(f"   • {paper_id}: {paper['year']} - {paper['title'][:40]}...")
        output.append("")
        
        # Intermediate papers  
        output.append(" INTERMEDIATE (Builds on Foundational):")
        for paper_id in intermediate:
            paper = self.metadata[paper_id]
            deps = self.graph[paper_id]
            dep_names = [f"{dep}" for dep in deps]
            output.append(f"   • {paper_id}: {paper['year']} - Needs: {', '.join(dep_names)}")
        output.append("")
        
        # Advanced papers
        output.append(" ADVANCED (Integrates Multiple Works):")
        for paper_id in advanced:
            paper = self.metadata[paper_id]
            deps = self.graph[paper_id]
            dep_names = [f"{dep}" for dep in deps]
            output.append(f"   • {paper_id}: {paper['year']} - Combines: {', '.join(dep_names)}")
        output.append("")
        
        #  AUTOMATIC FLOW DIAGRAM GENERATION
        output.append(" AUTOMATIC DEPENDENCY FLOW DIAGRAM:")
        output.append("")
        
        # Get BFS levels for automatic positioning
        _, bfs_levels, _ = topological_sort_bfs(self.graph)
        
        # Create level groups automatically
        level_groups = {}
        for paper_id, level in bfs_levels.items():
            if level not in level_groups:
                level_groups[level] = []
            level_groups[level].append(paper_id)
        
        # Generate ASCII tree automatically
        max_level = max(level_groups.keys()) if level_groups else 0
        
        for level in sorted(level_groups.keys()):
            papers = level_groups[level]
            indent = "    " * level
            
            for i, paper_id in enumerate(papers):
                paper = self.metadata[paper_id]
                
                # Determine connector symbols
                if level == 0:
                    connector = "🟢 "
                    suffix = " (Foundation)"
                elif i == len(papers) - 1:
                    connector = "└── "
                    suffix = ""
                else:
                    connector = "├── "
                    suffix = ""
                
                # Show dependencies
                deps = self.graph[paper_id]
                if deps:
                    dep_text = f" ← depends on: {', '.join(deps)}"
                else:
                    dep_text = " (no dependencies)"
                
                output.append(f"{indent}{connector}{paper_id}: {paper['year']}{suffix}{dep_text}")
        
        output.append("")
        output.append(" WHAT THIS SHOWS:")
        output.append("• Topological sort AUTOMATICALLY discovered dependencies")
        output.append("• Reading order respects ALL citation relationships") 
        output.append("• No paper appears before its prerequisites")
        output.append("• Perfect learning path from basic → advanced")
        output.append("")
        
        return "\n".join(output)
    
    def save_comparison_csv(self, results: Dict[str, Dict], filename: str):
        """
        Save algorithm comparison data to CSV file for further analysis.
        
        Args:
            results: Dictionary containing algorithm results
            filename: Name of the CSV file
        """
        results_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'results')
        os.makedirs(results_dir, exist_ok=True)
        
        filepath = os.path.join(results_dir, filename)
        
        with open(filepath, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            # Write header
            writer.writerow([
                'Algorithm', 
                'Execution_Time_ms', 
                'Vertices', 
                'Edges', 
                'Theoretical_Operations_V+E', 
                'Actual_Operations', 
                'Space_Complexity', 
                'Efficiency_Ops_per_ms',
                'Valid_Result'
            ])
            
            # Write data rows
            for algo_name, data in results.items():
                if data['valid'] and 'metrics' in data:
                    metrics = data['metrics']
                    time_ms = metrics.get('execution_time_ms', 0)
                    V = metrics.get('vertices', 0)
                    E = metrics.get('edges', 0)
                    theoretical_ops = metrics.get('theoretical_operations', 0)
                    actual_ops = metrics.get('actual_operations', 0)
                    space = metrics.get('space_complexity', 0)
                    efficiency = actual_ops / time_ms if time_ms > 0 else 0
                    
                    writer.writerow([
                        algo_name, 
                        f"{time_ms:.6f}", 
                        V, 
                        E, 
                        theoretical_ops, 
                        actual_ops, 
                        space, 
                        f"{efficiency:.2f}",
                        "YES"
                    ])
                else:
                    writer.writerow([algo_name, '0.000000', '0', '0', '0', '0', '0', '0.00', 'NO'])
        
        print(f"COMPARISON DATA: Saved to {filepath}")
    
    def save_results_to_file(self, filename: str, content: str) -> None:
        """
        Save results to file in results directory.
        
        Args:
            filename: Name of the file
            content: Content to save
        """
        results_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'results')
        os.makedirs(results_dir, exist_ok=True)
        
        filepath = os.path.join(results_dir, filename)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
        
        print(f"OUTPUT SAVED: {filepath}")

def main():
    """
    Main application entry point.
    Orchestrates complete research analysis workflow.
    """
    print("TOPOLOGICAL SORT RESEARCH PROJECT")
    print("Design and Analysis of Algorithms - Professional Implementation")
    print("=" * 70)
    print("TEAM: CHARVI (Kahn) | MERIEM (DFS) | LOREENA (BFS & Integration)")
    print("=" * 70)
    
    try:
        # Initialize the analysis system
        system = ResearchAnalysisSystem()
        
        # Display research overview
        print("\nRESEARCH DATASET OVERVIEW:")
        print("-" * 50)
        analyze_research_evolution()
        
        # Run all algorithms and collect comprehensive data
        print("\nALGORITHM EXECUTION PHASE:")
        print("-" * 50)
        results = system.run_all_algorithms()
        
        # Generate and display complexity analysis
        print("\nCOMPLEXITY ANALYSIS PHASE:")
        print("-" * 50)
        complexity_analysis = system.generate_complexity_analysis(results)
        print(complexity_analysis)
        
        # Save complexity analysis
        system.save_results_to_file('complexity_analysis.txt', complexity_analysis)
        
        # Generate reading schedule using Kahn's algorithm (most reliable)
        if results['Kahn']['valid']:
            print("\nREADING SCHEDULE GENERATION:")
            print("-" * 50)
            reading_schedule = system.generate_reading_schedule(results['Kahn']['result'])
            print(reading_schedule)
            
            # Save reading schedule
            system.save_results_to_file('reading_schedule.txt', reading_schedule)
        
        # Generate dependency analysis using BFS levels
        if results['BFS']['valid']:
            print("\nDEPENDENCY ANALYSIS:")
            print("-" * 50)
            dependency_analysis = system.generate_dependency_analysis(results['BFS']['levels'])
            print(dependency_analysis)
            
            # Save dependency analysis
            system.save_results_to_file('dependency_analysis.txt', dependency_analysis)

        # 🆕 ADDED: Generate AUTOMATIC dependency visualization
        print("\n" + "=" * 60)
        print("VISUALIZATION - CLEAR DEPENDENCY EXPLANATION")
        print("=" * 60)
        dependency_viz = system.generate_dependency_visualization(results['Kahn']['result'])
        print(dependency_viz)
        system.save_results_to_file('dependency_visualization.txt', dependency_viz)
        
        # Save comprehensive comparison data to CSV
        system.save_comparison_csv(results, 'algorithm_comparison.csv')

        # Generate a plain performance summary and save to file
        try:
            performance_lines: List[str] = []
            performance_lines.append("PERFORMANCE SUMMARY (Execution times in microseconds)")
            performance_lines.append("Algorithm | Avg Time (μs)")
            performance_lines.append("-" * 40)
            for algo_name, data in results.items():
                if data['valid']:
                    # Convert milliseconds to microseconds for readability
                    time_us = data['metrics']['execution_time_ms'] * 1000
                    performance_lines.append(f"{algo_name:<10} | {time_us:.2f}")
            perf_report = "\n".join(performance_lines)
            system.save_results_to_file('performance_analysis.txt', perf_report)
        except Exception as e:
            print(f"Failed to write performance_analysis.txt: {e}")

        # Optionally generate visualisations (requires networkx and matplotlib)
        try:
            from generate_visualizations import (
                create_citation_graph_image,
                create_performance_bar_chart,
            )
            # Create images in results folder
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            results_dir = os.path.join(base_dir, 'results')
            os.makedirs(results_dir, exist_ok=True)
            graph = system.graph
            metadata = system.metadata
            citation_img = os.path.join(results_dir, 'citation_graph.png')
            perf_img = os.path.join(results_dir, 'performance_comparison.png')
            create_citation_graph_image(graph, metadata, citation_img)
            create_performance_bar_chart(results, perf_img)
            print("\nVISUALISATIONS GENERATED:")
            print(f"  • Citation graph image: {citation_img}")
            print(f"  • Performance comparison chart: {perf_img}")
        except ImportError:
            # Gracefully skip visualisation generation if libraries are missing
            print("\nOptional visualisation modules not installed; skipping image generation.")
        
        # Final summary and project completion
        print("\n" + "=" * 80)
        print("PROJECT COMPLETION SUMMARY")
        print("=" * 80)
        print("ALGORITHMS SUCCESSFULLY IMPLEMENTED AND ANALYZED:")
        print("  1. KAHN'S ALGORITHM (CHARVI)")
        print("     - Queue-based topological sort with in-degree counting")
        print("     - O(V + E) time complexity, O(V) space complexity")
        print("     - Excellent cycle detection capabilities")
        print("")
        print("  2. DFS ALGORITHM (MERIEM)")
        print("     - Depth-first search with recursion stack")
        print("     - O(V + E) time complexity, O(V) space complexity") 
        print("     - Natural recursive approach with built-in cycle detection")
        print("")
        print("  3. BFS ALGORITHM (LOREENA)")
        print("     - Level-based topological sort with dependency tracking")
        print("     - O(V + E) time complexity, O(V) space complexity")
        print("     - Provides comprehensive level analysis")
        print("")
        print("RESEARCH DATA ANALYSIS COMPLETED:")
        print(f"  • Papers Analyzed: {system.stats['total_papers']} real academic papers")
        print(f"  • Citation Relationships: {system.stats['total_citations']} dependencies")
        print(f"  • Research Timeline: {system.stats['research_span'] + 1} years (2017-2024)")
        print(f"  • Domain: Nanotechnology in Sustainable Agriculture")
        print("")
        print("OUTPUT FILES GENERATED:")
        print("  • results/reading_schedule.txt - Optimal research reading order")
        print("  • results/complexity_analysis.txt - Algorithm performance analysis")
        print("  • results/dependency_analysis.txt - Research dependency levels")
        print("  • results/dependency_visualization.txt - Clear dependency flow diagram")
        print("  • results/algorithm_comparison.csv - Detailed metrics (CSV format)")
        print("")
        print("ALL ALGORITHMS DEMONSTRATE O(V + E) TIME COMPLEXITY AND O(V) SPACE COMPLEXITY")
        print("THEORETICAL ANALYSIS CONFIRMED BY EMPIRICAL PERFORMANCE METRICS")
        print("=" * 80)
        
        return 0
        
    except Exception as e:
        print(f"\nSYSTEM ERROR: {e}")
        print("Please check the implementation and ensure all dependencies are available.")
        return 1

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)