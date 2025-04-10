## Installation
- Make sure to have a version of the interpreter installed in your computer, either as a standalone software, virtual environment with venv, or a virtual environment with Anaconda.
- Make sure to have pip package manager

## Prerequisites
- Python 3.8+
- pip package manager

## Interactive version
If you're interested in running the software virtually and avoid any local installations, please visit our <a style="font-size:1.5em" href="https://replit.com/join/lbjkwkjnii-garcilau"> Replit demo </a>

## Quick Start

```bash
git clone https://github.com/UGarCil/UGarcil_capstone.git
cd UGarcil_capstone/src
pip install .
```

To execute the code, use the following template:
```
from sublimat import file_manager
from sublimat.main import main

# To run the program:
# define the absolute path to:
# - substitution_matrices.txt
benchmark = "/home/runner/workspace/data/substitution_matrices.txt"
# - input_sequences.fasta
sequence_data = "/home/runner/workspace/data/input_sequences.fasta"
# - output directory
output_path = "/home/runner/workspace/data/"
# Execute the function composition export(main()) to export the results to the output directory
file_manager.export(main(sequence_data, benchmark), output_path)


```

The program will export a .csv file located at your output_path, and can be opened with Microsoft Excel or other spreadsheet software.