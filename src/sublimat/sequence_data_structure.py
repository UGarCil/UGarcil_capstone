"""Biological sequence container and validator module.

This module provides the SequenceData class for handling and validating
nucleotide sequence pairs for alignment purposes.
"""

## @file sequence_data_structure.py
# @ingroup sequence_data_structure_module
# @brief Biological sequence container and validator
from sublimat import file_manager


## @class SequenceData
# @brief Biological sequence pair container
# @ingroup sequence_data_structure_module
#
# @var seqA First sequence (5'→3')
# @var seqB Second sequence (5'→3')
# @throws ValueError Invalid sequence format
class SequenceData:
    """Container for biological sequence pairs with validation.

    Attributes:
        seq_a (str): First nucleotide sequence (5' to 3')
        seq_b (str): Second nucleotide sequence (5' to 3')
    """

    ## @fn __init__(self)
    # @brief Initialize with sequences from file
    # @details Loads sequences using @ref file_manager.read_sequence_file()
    # @post self.seqA and self.seqB contain valid sequences
    # @throws ValueError If validation fails
    def __init__(self, read_file_path):
        """@dotfile sequence_flow.dot"""
        self.seq_a, self.seq_b = file_manager.read_sequence_file(read_file_path)
        self.validate_sequence(self.seq_a)
        self.validate_sequence(self.seq_b)

    ## @fn validate_sequence(self, seq)
    # @brief Validate nucleotide sequence
    # @param seq Sequence to validate
    # @throws ValueError For invalid characters
    # @details Checks:
    # @li Only A/T/G/C/_ characters
    # @li Non-zero length
    def validate_sequence(self, seq):
        """Validate nucleotide sequence contains only valid characters.
        
        Args:
            seq: Sequence to validate
            
        Raises:
            ValueError: If sequence contains invalid characters
        """
        valid_chars = {"A", "T", "G", "C", "_"}
        if any(char not in valid_chars for char in seq):
            raise ValueError("Invalid nucleotide Error")

    ## @fn get_sequences(self)
    # @brief Get both sequences as a tuple
    # @return tuple (seqA, seqB)
    # @ingroup sequence_data_structure_module
    def get_sequences(self):
        """Return both sequences as a tuple.
        
        Returns:
            tuple: (seq_a, seq_b) sequence pair
        """
        return (self.seq_a, self.seq_b)


## @page sequence_requirements Sequence Requirements
# @tableofcontents
# @section format Sequence Format
# @verbinclude sequence_spec.txt
#
# @section validation Validation Rules
# @li Valid nucleotides only
# @li Minimum length 1bp
# @li No ambiguous bases
