# Topological Sort  Project

In this asisgnement we have implemented the topological sort
research assignment originally provided by the user.  It models
citation relationships between ten real academic papers on
nanotechnology in sustainable agriculture and implements three
topological sorting algorithms Kahn’s algorithm, a depth‑first search
based sort, and a breadth‑first search (BFS) variant with level
tracking.  In addition to the core functionality, this improved
edition includes a clear reading schedule (from foundational to
advanced papers), an inverted dependency analysis, comprehensive
performance metrics, optional visualisations of the citation network
and algorithm timings, and a concise README.

## Directory Structure

```
improved_project/
├── python/                  # (Unused stub for future Python scripts)
├── requirements.txt         # Python dependencies
├── results/
│   ├── algorithm_comparison.csv    # CSV summarising algorithm metrics
│   ├── complexity_analysis.txt     # Human‑readable complexity overview
│   ├── dependency_analysis.txt     # Grouped dependency levels (inverted)
│   ├── performance_analysis.txt    # Summary of execution times
│   ├── reading_schedule.txt        # Foundational→advanced reading order
│   ├── citation_graph.png          # Visual representation of the citation network
│   └── performance_comparison.png  # Bar chart comparing algorithm runtimes
├── src/
│   ├── algorithms/
│   │   ├── bfs.py           # BFS‑based topological sort with level tracking
│   │   ├── dfs.py           # DFS‑based topological sort
│   │   └── kahn.py          # Kahn’s algorithm implementation
│   ├── data/
│   │   └── research_data.py # Citation graph and paper metadata
│   ├── generate_visualizations.py  # Optional visualisation script
│   ├── main.py              # End‑to‑end analysis pipeline
│   ├── debug_levels.py      # Utility to inspect BFS level assignments
│   └── tests/
│       ├── test_bfs.py      # Unit tests for BFS algorithm
│       ├── test_dfs.py      # Unit tests for DFS algorithm
│       ├── test_integration.py # Integration tests and performance checks
│       └── test_kahn.py     # Unit tests for Kahn’s algorithm
└── README.md (this file)
```

## Getting Started

This project is designed to run on Python 3.7 or later.  Clone the
repository and install dependencies:

```bash
python -m pip install -r requirements.txt
```

> **Note**: The core algorithms use only the standard library.  The
> additional libraries—`networkx`, `matplotlib` and `numpy`—are
> required only for the optional visualisations.

### Running the Analysis Pipeline

To execute all algorithms, analyse their complexity, generate a
reading schedule, perform a dependency analysis and write the output
files to the `results/` directory:

```bash
python src/main.py
```

This command prints a summary to the console and creates the
following files:

- **reading_schedule.txt** – a numbered list of papers to read from
  foundational to advanced, including authors, publication venue and
  DOI.  The schedule is derived from Kahn’s algorithm but reversed to
  start with the earliest work.
- **complexity_analysis.txt** – a side‑by‑side comparison of time and
  space complexity for Kahn’s, DFS and BFS algorithms along with
  theoretical vs. actual operations and relative efficiency.
- **dependency_analysis.txt** – papers grouped by dependency depth.
  Level 0 contains the foundational papers with no citations; higher
  levels correspond to papers that cite an increasing number of works.
- **performance_analysis.txt** – a concise table of average execution
  times for each algorithm in microseconds.
- **algorithm_comparison.csv** – a machine‑readable CSV containing
  metrics for further analysis.
- **citation_graph.png** and **performance_comparison.png** – if you
  have installed the optional visualisation libraries, these images
  provide a graph of the citation network and a bar chart of algorithm
  runtimes, respectively.

### Running Tests

Each algorithm comes with an extensive suite of unit tests.  You can
run them individually or all together.  For example:

```bash
python src/tests/test_kahn.py
python src/tests/test_dfs.py
python src/tests/test_bfs.py
python src/tests/test_integration.py
```

The integration tests verify that all algorithms return valid
topological orders on the research graph, ensure error conditions are
properly handled, and benchmark algorithm performance.  The tests
assume the citation graph orientation used in this project: edges
point from each paper to the earlier works it cites.

### Generating Visualisations

If you wish to visualise the citation network and compare algorithm
performance graphically, run:

```bash
python src/generate_visualizations.py
```

This script will regenerate the citation graph and performance
comparison charts in the `results/` directory.  Node colours in the
network diagram correspond to publication years, and arrows point
from a citing paper to the work it references.  The bar chart shows
execution times in milliseconds for Kahn’s algorithm, DFS and BFS.

## What Was Improved

Compared with the original submission, this edition introduces the
following improvements:

- **Corrected reading order** – Because the citation graph points from
  newer papers to the older works they cite, the raw topological
  order starts with the most recent paper.  The reading schedule now
  reverses that order to guide readers from foundational research to
  advanced reviews.
- **Inverted dependency levels** – The BFS algorithm still reports
  level 0 for the most dependent papers (no incoming citations).  For
  clarity, the dependency analysis now inverts these levels so that
  level 0 lists the foundational papers without prerequisites and
  higher levels indicate an increasing number of dependencies.
- **Performance summary** – A new `performance_analysis.txt` file
  summarises execution times (converted to microseconds) for each
  algorithm, complementing the detailed `complexity_analysis.txt`.
- **Visualisations** – A dedicated script uses `networkx` and
  `matplotlib` to generate a citation graph image and a bar chart of
  algorithm runtimes.  These diagrams help readers understand the
  research landscape and performance differences at a glance.
- **Comprehensive README** – This document explains how to set up
  the environment, run the analysis pipeline, execute tests,
  generate visualisations, and understand the outputs.

## Citation Data Source

The citation network is derived from ten real academic papers on
nanotechnology in sustainable agriculture.  The foundational study on
Mo–nanoparticle seed treatments is cited by subsequent reviews and
experimental papers, culminating in a 2024 review on climate change
mitigation【643682034050769†L230-L236】.  The metadata and dependency structure are stored
in `src/data/research_data.py`.

## License

This project is provided for educational purposes and may be used and
modified freely.  All papers referenced are credited to their
original authors and publishers.
