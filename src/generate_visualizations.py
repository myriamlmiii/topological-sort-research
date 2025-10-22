"""
# Meriem 
"""

import os
from typing import Dict, List

import matplotlib

# Use a non‑interactive backend to allow image generation without a display
matplotlib.use("Agg")  # type: ignore
import matplotlib.pyplot as plt  # type: ignore

from algorithms.kahn import topological_sort_kahn
from algorithms.dfs import topological_sort_dfs
from algorithms.bfs import topological_sort_bfs
from data.research_data import get_citation_graph, get_paper_metadata
from main import ResearchAnalysisSystem


def create_citation_graph_image(graph: Dict[str, List[str]], metadata: Dict[str, Dict], output_path: str) -> None:
    """
    Create a citation graph visualisation without using NetworkX.  This
    function computes a layered layout based on inverted BFS levels so
    that foundational papers (no prerequisites) appear on the top row
    (level 0) and more recent papers appear on subsequent rows.  Each
    node is represented by a coloured circle labelled with its ID and
    year.  Arrows point from a citing paper to the work it references.

    Args:
        graph: An adjacency list of the citation graph (keys are paper IDs,
            values are lists of papers they cite).
        metadata: Dictionary containing metadata for each paper.
        output_path: Destination file path for the PNG image.
    """
    # Determine year range for colour mapping
    years = [data["year"] for data in metadata.values()]
    min_year, max_year = min(years), max(years)
    year_range = max(max_year - min_year, 1)

    # Use BFS to get original levels, then invert to group by foundational depth
    _, bfs_levels, _ = topological_sort_bfs(graph)
    max_level = max(bfs_levels.values()) if bfs_levels else 0
    inverted_levels: Dict[int, List[str]] = {}
    for node, lvl in bfs_levels.items():
        inv = max_level - lvl
        inverted_levels.setdefault(inv, []).append(node)

    # Sort papers within each level for consistent ordering
    for level in inverted_levels:
        inverted_levels[level].sort()

    # Assign positions: x coordinate increments within each level,
    # y coordinate equals the level number (foundation at 0).
    pos: Dict[str, tuple] = {}
    y_spacing = 1.0
    x_spacing = 1.0
    for level in sorted(inverted_levels.keys()):
        nodes = inverted_levels[level]
        # Centre nodes horizontally
        offset = -(len(nodes) - 1) / 2.0
        for i, node in enumerate(nodes):
            x = (i + offset) * x_spacing
            y = -level * y_spacing  # negative so foundational at top
            pos[node] = (x, y)

    # Begin plotting
    plt.figure(figsize=(10, 6))
    ax = plt.gca()
    ax.set_title(
        "Citation Graph – Nanotechnology in Sustainable Agriculture",
        fontsize=12,
    )
    ax.axis("off")

    # Draw edges as arrows
    for paper_id, deps in graph.items():
        x1, y1 = pos[paper_id]
        for dep in deps:
            x2, y2 = pos[dep]
            # Draw arrow from paper -> cited paper
            ax.annotate(
                "",
                xy=(x2, y2),
                xytext=(x1, y1),
                arrowprops=dict(arrowstyle="->", lw=1.0, color="gray"),
            )

    # Draw nodes
    for paper_id, (x, y) in pos.items():
        year = metadata[paper_id]["year"]
        color_val = (year - min_year) / year_range
        node_color = plt.cm.viridis(color_val)
        circle = plt.Circle((x, y), 0.1, color=node_color, ec="black", zorder=3)
        ax.add_patch(circle)
        # Add label: show paper ID and year
        label = f"{paper_id}\n{year}"
        ax.text(x, y - 0.14, label, ha="center", va="top", fontsize=7)

    # Adjust limits to ensure all nodes and arrows fit
    all_x = [p[0] for p in pos.values()]
    all_y = [p[1] for p in pos.values()]
    if all_x:
        ax.set_xlim(min(all_x) - 1.5, max(all_x) + 1.5)
    if all_y:
        ax.set_ylim(min(all_y) - 1.0, max(all_y) + 0.5)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def create_performance_bar_chart(results: Dict[str, Dict], output_path: str) -> None:
    """
    Generate a bar chart comparing the execution times of each
    topological sort algorithm.  The y‑axis displays execution time in
    milliseconds.

    Args:
        results: Dictionary returned by ResearchAnalysisSystem.run_all_algorithms().
        output_path: Path to save the bar chart PNG.
    """
    algorithms = []
    times_ms = []
    for name, data in results.items():
        if data.get("valid"):
            algorithms.append(name)
            times_ms.append(data["metrics"]["execution_time_ms"])

    plt.figure(figsize=(8, 5))
    plt.bar(algorithms, times_ms)
    plt.xlabel("Algorithm")
    plt.ylabel("Execution Time (ms)")
    plt.title("Performance Comparison of Topological Sort Algorithms")
    # Display values on top of bars
    for i, val in enumerate(times_ms):
        plt.text(i, val, f"{val:.3f}", ha="center", va="bottom", fontsize=8)
    plt.tight_layout()
    plt.savefig(output_path, dpi=300)
    plt.close()


def main() -> None:
    """Run the visualization generation process."""
    print("Generating visualizations...")
    system = ResearchAnalysisSystem()
    # Run algorithms once to gather metrics
    results = system.run_all_algorithms()
    # Ensure results directory exists
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    results_dir = os.path.join(base_dir, "results")
    os.makedirs(results_dir, exist_ok=True)

    # Generate citation graph
    graph = get_citation_graph()
    metadata = get_paper_metadata()
    citation_path = os.path.join(results_dir, "citation_graph.png")
    create_citation_graph_image(graph, metadata, citation_path)
    print(f"Citation graph saved to {citation_path}")

    # Generate performance comparison
    perf_path = os.path.join(results_dir, "performance_comparison.png")
    create_performance_bar_chart(results, perf_path)
    print(f"Performance comparison saved to {perf_path}")


if __name__ == "__main__":
    main()