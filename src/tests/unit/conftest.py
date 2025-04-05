# Description: pytest fixtures for testing
"""
@file conftest.py
@brief pytest fixtures for testing
@ingroup test_module
"""
import pytest
from sublimat.sequence_data_structure import SequenceData
from sublimat.substitution_matrix import SubMat

@pytest.fixture
def sample_sequence_data():
    """@fixture sample_sequence_data
    @brief Provides sample sequence data for testing
    @ingroup test_module
    """
    seq = SequenceData()
    seq.seq_a = "ACGT"
    seq.seq_b = "ACGT"
    return seq

@pytest.fixture
def sample_matrix_bench():
    """@fixture sample_matrix_bench
    @brief Provides sample substitution matrices for testing
    @ingroup test_module
    """
    matrix = SubMat()
    matrix.data = [
        {"NAME": "TEST1", "PENALIZING_COSTS": {"match": 1, "mismatch": -1, "gap": -2}},
        {"NAME": "TEST2", "PENALIZING_COSTS": {"match": 2, "mismatch": -1, "gap": -3}}
    ]
    return matrix