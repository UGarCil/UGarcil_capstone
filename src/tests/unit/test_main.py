from sublimat.sequence_data_structure import SequenceData
from sublimat.substitution_matrix import SubMat
from sublimat.main import main
import os
import pytest


def test_main_empty_submat():
    # Change the directory to the location of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    seq = SequenceData("./seq_test_1.txt")

    # Provide a proper 4x4 substitution matrix
    matrices = SubMat("./submat_test_1.txt")
    results = main(seq, matrices)
    assert len(results) == 1
    assert results[0]["score"] == 0
    
    

def test_main_one_bp_seq():
    # Change the directory to the location of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    seq = SequenceData("./seq_test_2.txt")
    # Provide a proper 4x4 substitution matrix
    matrices = SubMat("./submat_test_2.txt")
    results = main(seq, matrices)
    assert len(results) == 1
    assert results[0]["score"] == 1

def test_main_unitary_submat():
    # Change the directory to the location of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    seq = SequenceData("./seq_test_3.txt")
    # Provide a proper 4x4 substitution matrix
    matrices = SubMat("./submat_test_3.txt")
    results = main(seq, matrices)
    assert len(results) == 1
    assert results[0]["score"] == 3

def test_main_empty_seq():
    # Change the directory to the location of this script
    script_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(script_dir)
    
    # Test expected exception is raised
    with pytest.raises(ValueError) as excinfo:
        seq = SequenceData("./seq_test_4.txt")
        matrices = SubMat("./submat_test_4.txt")
        main(seq, matrices)
    
    # verif. exception message
    assert "Invalid FASTA File Error: Less than 2 sequences detected" in str(excinfo.value)