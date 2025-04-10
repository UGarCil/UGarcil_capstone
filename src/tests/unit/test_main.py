from sublimat.sequence_data_structure import SequenceData
from sublimat.substitution_matrix import SubMat
from sublimat.main import main
import os
import pytest


# Helper function to get test file path
def get_test_file(filename):
    return os.path.join(os.path.dirname(__file__), "test_data", filename)

def test_main_empty_submat():
    # Change the directory to the location of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    seq = get_test_file("seq_test_1.fasta")

    # Provide a proper 4x4 substitution matrix
    matrices = get_test_file("submat_test_1.txt")
    results = main(seq, matrices)
    assert len(results) == 1
    assert results[0]["score"] == 0
    
    

def test_main_one_bp_seq():
    # Change the directory to the location of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    seq = get_test_file("seq_test_2.fasta")
    # Provide a proper 4x4 substitution matrix
    matrices = get_test_file("submat_test_2.txt")
    results = main(seq, matrices)
    assert len(results) == 1
    assert results[0]["score"] == 1

def test_main_unitary_submat():
    # Change the directory to the location of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    seq = get_test_file("seq_test_3.fasta")
    # Provide a proper 4x4 substitution matrix
    matrices = get_test_file("submat_test_3.txt")
    results = main(seq, matrices)
    assert len(results) == 1
    assert results[0]["score"] == 3

def test_main_empty_seq():
    # Change the directory to the location of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Test expected exception is raised
    with pytest.raises(ValueError) as excinfo:
        seq = get_test_file("seq_test_4.fasta")
        matrices = get_test_file("submat_test_4.txt")
        main(seq, matrices)
    
    # verif. exception message
    assert "Invalid FASTA File Error: Less than 2 sequences detected" in str(excinfo.value)
    
    
'''
Tests for valid/invalid sequence inputs — R1
'''

# TC-SubLiMat-1-1: Valid sequences
def test_valid_sequences():
    seq = get_test_file("valid_seqs.fasta")
    matrices = get_test_file("valid_submat.txt")
    results = main(seq, matrices)
    assert isinstance(results, list)
    assert all(isinstance(x["score"], float) for x in results)

# TC-SubLiMat-1-2: Empty sequence A
def test_empty_sequence_a():
    with pytest.raises(ValueError) as e:
        seq = get_test_file("empty_seq_a.fasta")
        matrices = get_test_file("valid_submat.txt")
        main(seq, matrices)
    assert "Zero-length sequences" in str(e.value)

# TC-SubLiMat-1-8: Invalid DNA characters
def test_invalid_dna_chars():
    with pytest.raises(ValueError) as e:
        seq = get_test_file("invalid_chars.fasta")
        matrices = get_test_file("valid_submat.txt")
        main(seq, matrices)
    assert "Invalid nucleotide" in str(e.value)
    
'''Matrix construction — R2'''

# TC-SubLiMat-2-4: Max allowed sequences (500x500)
def test_max_length_sequences():
    seq = get_test_file("max_length_seqs.fasta")  # 500bp x 500bp
    matrices = get_test_file("valid_submat.txt")
    results = main(seq, matrices)
    assert len(results) > 0

# TC-SubLiMat-2-6: Exceeds max length
def test_exceeds_max_length():
    with pytest.raises(ValueError) as e:
        seq = get_test_file("too_long_seqs.fasta")  # 5001bp x 5001bp
        matrices = get_test_file("valid_submat.txt")
        main(seq, matrices)
    assert "exceeds maximum" in str(e.value)
    
'''Matrix for Substitution matrix — R3'''

# TC-SubMat-3-1: Valid 4x4 matrix
def test_valid_submat():
    matrices = get_test_file("valid_submat.txt")
    submat = SubMat(matrices)
    assert len(submat.data[0]["PENALIZING_COSTS"]) == 4

# TC-SubMat-3-2: Non-square matrix
def test_nonsquare_matrix():
    with pytest.raises(ValueError) as e:
        matrices = get_test_file("nonsquare_submat.txt")
        SubMat(matrices)
    assert "not 4x4" in str(e.value)

# TC-SubMat-3-5: Asymmetric matrix
# def test_asymmetric_matrix():
#     with pytest.raises(ValueError) as e:
#         matrices = get_test_file("asymmetric_submat.txt")
#         SubMat(matrices)
#     assert "not symmetric" in str(e.value)
    
    
'''Output validation — R4/R5'''

# Known-value test
def test_known_alignment():
    seq = get_test_file("known_test_seqs.fasta")
    matrices = get_test_file("unitary_submat.txt")
    results = main(seq, matrices)
    assert results[0]["score"] == 10.0  # Expected score for test case

# Score consistency test
def test_score_consistency():
    seq = get_test_file("consistency_test.fasta")
    matrices = get_test_file("valid_submat.txt")
    results1 = main(seq, matrices)
    results2 = main(seq, matrices)
    assert results1 == results2