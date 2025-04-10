'''File Manager module for handling file I/O operations'''
## @file file_manager.py
# @ingroup control_module
# @brief File handling and I/O operations

import os
from os.path import join as jn

import pandas as pd

## @defgroup config_constants Configuration Paths
# @ingroup control_module
# @brief File system paths and locations

## @var root_path
# @brief Base data directory path
# @ingroup config_constants
ROOT_PATH = "../data/"

## @var input_sequences_path
# @brief FASTA file input path
# @ingroup config_constants
INPUT_SEQUENCES_PATH = jn(ROOT_PATH, "input_sequences.fasta")

## @var input_submat_path
# @brief Substitution matrix definitions path
# @ingroup config_constants
INPUT_SUBMAT_PATH = jn(ROOT_PATH, "substitution_matrices.txt")

## @var export_results_path
# @brief Benchmark results output path
# @ingroup config_constants
EXPORT_RESULTS_PATH = jn(ROOT_PATH, "benchmark_results.csv")

# Script directory initialization
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
os.chdir(SCRIPT_DIR)


## @fn export(data)
# @brief Exports alignment results to CSV
# @ingroup control_module
# @param data Benchmark results to export (list of RowResult dicts)
# @throw IOError If file cannot be written
# @see AlignmentModule::needleman_wunsch() SubstitutionMatrixModule::load_matrices()
# @details Implements
def export(data, file_path):
    '''Export the benchmark results to a CSV file'''
    result = pd.DataFrame(data)
    result_df = result.sort_values("score", ascending=False)
    final_path = jn(file_path, "benchmark_results.csv")
    result_df.to_csv(final_path, index=False)


## @fn read_sequence_file()
# @brief Reads and validates FASTA sequence file
# @ingroup control_module
# @return tuple (str, str) Validated nucleotide sequences
# @throw ValueError For invalid FASTA format
# @par Expected FASTA Format:
# @code
# >Sequence1
# TGGAT
# >Sequence2
# ATGGA
# @endcode
def read_sequence_file(file_path, max_length=5000):
    """@brief Gets the sequence data from the file path"""
    with open(file_path, encoding="utf-8") as file:
        data = file.readlines()

    if not data[0].startswith(">") or not data[2].startswith(">"):
        raise ValueError("Invalid FASTA File Error: Missing sequence name")
    if len(data) < 4:
        raise ValueError("Invalid FASTA File Error: Less than 2 sequences detected")

    total_headers = sum(1 for line in data if line.startswith(">"))
    if total_headers != 2:
        raise ValueError("Invalid FASTA File Error: More than 2 sequences detected")

    seq1 = data[1].strip()
    seq2 = data[3].strip()
    if len(seq1) < 1 or len(seq2) < 1:
        raise ValueError("Zero-length sequences Error")
    
    # Validate sequence length
    if len(seq1) > max_length or len(seq2) > max_length:
        raise ValueError(f"Sequence length exceeds maximum allowed size ({max_length}bp)")
    
    
    return (seq1, seq2)


## @fn read_submat_file()
# @brief Loads and validates substitution matrices
# @ingroup control_module
# @return list[dict] List of substitution matrix definitions
# @throw ValueError For invalid matrix format
# @par Expected Matrix Format:
# @code
# >MatrixName
# 1.0,-0.33,-0.33,-0.33
# -0.33,1.0,-0.33,-0.33
# -0.33,-0.33,1.0,-0.33
# -0.33,-0.33,-0.33,1.0
# @endcode
def read_submat_file(file_path):
    """@brief Gets the sequence data from the file path"""
    with open(file_path, encoding="utf-8") as file:
        data = [line.strip() for line in file if line.strip()]

    num_matrices = sum(1 for line in data if line.startswith(">"))
    if len(data) < num_matrices * 5:
        raise ValueError(
            "Invalid Substitution Matrix File Error: "
            "Non-square matrices or missing data"
        )

    for line in data:
        if not line.startswith(">") and not all(
            char in "0123456789.-," for char in line
        ):
            raise ValueError(
                f"Invalid Substitution Matrix in line {data.index(line)}.\n"
                "File Error: Non-numeric values in matrix"
            )

    benchmark = []

    # for each matrix, the first line is the name, the next 4 lines are the matrix
    for i in range(0, len(data), 5):
        _submat = {"PENALIZING_COSTS": None, "NAME": ""}
        _submat["NAME"] = data[i].strip().replace(">", "")
        _submat["PENALIZING_COSTS"] = [
            list(map(float, line.strip().split(","))) for line in data[i + 1 : i + 5]
        ]
        benchmark.append(_submat)
    return benchmark
