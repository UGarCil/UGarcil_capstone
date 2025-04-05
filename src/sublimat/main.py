"""Main benchmarking controller for Substitution Matrix Benchmarking (SubliMat)."""

## @defgroup test_module Testing Module
# @brief Unit and integration tests for SubliMat
# @details Contains all test cases and testing utilities
#
# @section test_structure Test Structure
# - Unit tests: tests/unit/
# - Integration tests: tests/integration/
# - End-to-end tests: tests/e2e/

## @page naming_conventions PEP8 Naming Conventions
# @tableofcontents
#
# @section conventions_table Naming Rules
# @verbinclude pep8_table.txt
#

## @mainpage Substitution Matrix Benchmarking with pairwise sequence alignment (SubliMat)
# @tableofcontents
#
# @section overview Program Overview
# Benchmarking tool for substitution matrices using Needleman-Wunsch algorithm
#
# @section modules Core Modules
# @ref control_module | @ref alignment_module | @ref sequence_data_module | @ref matrix_module

## @file main.py
# @brief Main benchmarking controller
# @ingroup core_module
#
# Coordinates workflow between:
# - @ref control_module (File I/O)
# - @ref alignment_module (Needleman-Wunsch)
# - @ref sequence_data_module (Sequence handling)
# - @ref matrix_module (Substitution matrices)

from sublimat import file_manager
from sublimat.alignment import NeedlemanWunsch
from sublimat.sequence_data_structure import SequenceData
from sublimat.substitution_matrix import SubMat


## @fn main(seq_data: SequenceData, matrix_bench: SubMat) -> list
# @brief Execute full matrix_bench pipeline
# @ingroup core_module
# @param seq_data Validated sequence pair (from @ref seq_data_module)
# @param matrix_bench Matrix collection (from @ref matrix_module)
# @return List of result dictionaries
# @throws AlignmentError If sequences cannot be aligned
# @see NeedlemanWunsch SubMat SequenceData
def main(seq_data: str, matrix_bench: str) -> list:
    """@dotfile workflow.dot"""
    benchmark = SubMat(matrix_bench)
    sequence_data = SequenceData(seq_data)
    result = []
    alignment_manager = NeedlemanWunsch(sequence_data.seq_a,
                                        sequence_data.seq_b)
    for submat in benchmark.data:
        final_score = alignment_manager(submat["PENALIZING_COSTS"])
        result.append({
            "matrix": submat["NAME"],
            "score": round(final_score, 2)
        })
    return result


## @page execution_flow Program Workflow
# @dotfile workflow.dot
# @brief Data flow between modules

## @ifmainpage Main Execution
# @brief Command-line entry point
# @par Typical Usage:
# @code{.sh}
# python main.py --input sequences.fa --matrices matrices.txt
# @endcode
if __name__ == "__main__":
    benchmark = "../data/substitution_matrices.txt"
    sequence_data = "../data/input_sequences.fasta"
    file_manager.export(main(sequence_data, benchmark), "../data")
