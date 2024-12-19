
# TuneParams

[![PyPI version](https://badge.fury.io/py/tuneparams.svg)](https://badge.fury.io/py/tuneparams)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## Overview

We've built TuneParams as a lightweight CLI tool to help you explore parameter spaces in your machine learning workflows. Using AST manipulation, we make it possible to modify parameters dynamically without touching your source code.

## Key Features

- **AST-Based Script Transformation**: Dynamic code parsing and modification through Python's AST module
- **Multi-Modal Parameter Input**: Supports direct CLI, file-based, and range-based parameter specifications
- **Automated Combinatorial Exploration**: Systematically generates and evaluates parameter combinations you specify
- **Structured Result Management**: Built-in CSV-based logging with querying capabilities
- **Non-Intrusive Integration**: Zero modifications required to your existing experimental scripts

## Installation

```bash
pip install tuneparams
```

## Usage Modes

### 1. Direct Parameter Specification
```bash
tuneparams model.py random_state=44, min_depth=10
```

### 2. Configuration File Mode
```bash
tuneparams model.py --param-file param_list.txt
```

Here's what your `param_list.txt` might look like:
```txt
learning_rate: 0.01, batch_size: 32, n_epochs: 100
random_state=50, max_depth=8
test_size=0.4, n_estimators=100
```

### 3. Range-Based Exploration
```bash
tuneparams model.py --range ranges.txt
```

Here's an example `ranges.txt`:
```txt
n_epoch=[50,200]
n_estimators=[100,110]
max_depth=[8,15]
```

### 4. Result Analysis
```bash
# Query experiments matching specific criteria 
tuneparams --query "accuracy >= 0.85 precision > 0.8"
```

## Pipeline

1. **Parsing**: Source code conversion to AST representation
2. **Analysis**: Parameter assignment node identification
3. **Transformation**: AST modification with new parameter values
4. **Regeneration**: Modified AST conversion back to executable code
5. **Execution**: Running transformed script with parameter combinations


![TuneParams Architecture Diagram](https://github.com/user-attachments/assets/b9a982fd-0163-4f2a-bd26-1ca3030ac7b6)

### Result Management
- **Storage**: We store experimental results in a local CSV database, with each row representing a unique experimental configuration and its corresponding performance metrics.
- **Schema**:
  - **ID**: A unique identifier for each experiment
  - **Input Parameters**: A list of parameter configurations used for the experiment
  - **Metrics**: We store all the metrics (eg: accuracy, precision, recall, and F1 score) values in seperate columns

## System Requirements

### Core Dependencies
- `Python` ≥ 3.7
- `astor` ≥ 0.8.0
- `pandas` ≥ 1.0.0

## Development Roadmap

### Current Version (0.2.3)
- [x] AST transformation
- [x] Multiple parameter input modes
- [x] Result logging and querying

### Upcoming Features (0.3.0)
- [ ] Parallel execution support
- [ ] Advanced metric extraction patterns
- [ ] Support for C++, Java and other languages

## Best Practices

```python
# TuneX-compatible format for printing metrics
def print_metrics(metrics: Dict[str, float]):
    """Print metrics in TuneParams-compatible format"""
    for name, value in metrics.items():
        print(f"{name}: {value}")

# Example usage
print_metrics({
    "accuracy": 0.857,
    "loss": 0.234,
    "f1_score": 0.843
})
```

**Disclaimer**: While we've made parameter exploration less time consuming, research still requires your expertise and insight.


