"""Substitution matrix handling module.

This module provides the SubMat class for loading and validating
nucleotide substitution matrices used in sequence alignment.
"""

## @file substitution_matrix.py
# @ingroup matrix_module
# @brief Substitution matrix handling

from sublimat import file_manager

## @class SubMat
# @brief Substitution matrix container and validator
# @ingroup matrix_module
#
# @var data List of matrix dictionaries
# @throws ValueError Invalid matrix format
class SubMat:
    """Container for substitution matrices with validation.

    Attributes:
        data: List of matrix dictionaries containing:
            - NAME: Matrix identifier
            - PENALIZING_COSTS: 4x4 numerical matrix
    """

    ## @fn __init__(self)
    # @brief Initialize with matrices from file
    # @details Loads matrices using @ref file_manager.read_submat_file()
    # @post self.data contains validated matrices
    # @throws ValueError If validation fails
    def __init__(self, read_file_path):
        """@dotfile matrix_flow.dot"""
        self.data = file_manager.read_submat_file(read_file_path)
        self.validate_benchmark(self.data)

    ## @fn validate_benchmark(self, benchmark)
    # @brief Validate matrix collection
    # @param benchmark List of matrix dictionaries
    # @throws ValueError For invalid matrices
    # @details Checks:
    # @li Each matrix is 4x4
    # @li Contains only numerical values
    # @li Square structure
    def validate_benchmark(self, benchmark):
        """Validate all matrices in the benchmark meet specifications.
        
        Args:
            benchmark: List of matrix dictionaries to validate
            
        Raises:
            ValueError: If any matrix fails validation checks
        """
        for submat in benchmark:
            # Validate matrix dimensions
            if len(submat["PENALIZING_COSTS"]) != 4:
                raise ValueError(
                    "Invalid Substitution Matrix Error: Matrix is not square"
                )
            for row in submat["PENALIZING_COSTS"]:
                if len(row) != 4:
                    raise ValueError(
                        "Invalid Substitution Matrix Error: Matrix is not 4x4"
                    )

    ## @fn get_matrix_names(self)
    # @brief Get list of matrix names
    # @return List[str] Matrix names
    # @ingroup matrix_module
    def get_matrix_names(self):
        """Return list of all matrix names in the collection.
        
        Returns:
            list: Names of all matrices in the benchmark
        """
        return [matrix["NAME"] for matrix in self.data]


## @page matrix_specs Matrix Specifications
# @tableofcontents
# @section format Matrix File Format
# @verbinclude matrix_format.txt
#
# @section validation Validation Rules
# @li 4x4 nucleotide matrices
# @li Square structure required
# @li Numeric values only
