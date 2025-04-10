#!/bin/bash

# Create directories if needed
mkdir -p test_data

# 1. Create valid sequences FASTA file
cat > valid_seqs.fasta << 'EOF'
>Sequence_A
ATGCTAGCTAGCTAGCT
>Sequence_B
ATGCAGTCAGTCAGTCA
EOF

# 2. Create FASTA file with empty first sequence
cat > empty_seq_a.fasta << 'EOF'
>Sequence_A

>Sequence_B
ATGCAGTCAGTCAGTCA
EOF

# 3. Create FASTA file with invalid characters
cat > invalid_chars.fasta << 'EOF'
>Sequence_A
ATGC1AGCXAGCTAGCT
>Sequence_B
ATGCAGTCAGTCAGTCA
EOF

# 4. Create FASTA file with max length sequences
cat > max_length_seqs.fasta << 'EOF'
>Max_Length_A
ATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGC
>Max_Length_B
GCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCAT
EOF

# 5. Create FASTA file with extra long sequences (for performance testing)
cat > too_long_seqs.fasta << 'EOF'
>Too_Long_A
ATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGC
>Too_Long_B
GCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCATGCAT
EOF

# 6. Create valid substitution matrix file
cat > valid_submat.txt << 'EOF'
>IDENTITY_MATRIX
1.0,0.0,0.0,0.0
0.0,1.0,0.0,0.0
0.0,0.0,1.0,0.0
0.0,0.0,0.0,1.0
>BASIC_MATCH_MISMATCH
2.0,-1.0,-1.0,-1.0
-1.0,2.0,-1.0,-1.0
-1.0,-1.0,2.0,-1.0
-1.0,-1.0,-1.0,2.0
EOF

# 7. Create non-square substitution matrix file
cat > nonsquare_submat.txt << 'EOF'
>NON_SQUARE_MATRIX
1.0,0.0,0.0
0.0,1.0,0.0
0.0,0.0,1.0
0.0,0.0,0.0
EOF

# 8. Create asymmetric substitution matrix file
cat > asymmetric_submat.txt << 'EOF'
>ASYMMETRIC_MATRIX
1.0,0.5,0.0,0.0
0.0,1.0,0.5,0.0
0.0,0.0,1.0,0.5
0.5,0.0,0.0,1.0
EOF

# 9. Create unitary substitution matrix file
cat > unitary_submat.txt << 'EOF'
>UNITARY_MATRIX
1.0,1.0,1.0,1.0
1.0,1.0,1.0,1.0
1.0,1.0,1.0,1.0
1.0,1.0,1.0,1.0
EOF

# 10. Create known test sequences for verification
cat > known_test_seqs.fasta << 'EOF'
>Known_Test_A
ATGC
>Known_Test_B
GCTA
EOF

# 11. Create performance test sequences (long sequences)
cat > perf_test_seqs.fasta << 'EOF'
>Performance_Test_A
ATGCTAGCTAGCTAGCTATGCTAGCTAGCTAGCTATGCTAGCTAGCTAGCTATGCTAGCTAGCTAGCTATGCTAGCTAGCTAGCT
>Performance_Test_B
ATGCAGTCAGTCAGTCAATGCAGTCAGTCAGTCAATGCAGTCAGTCAGTCAATGCAGTCAGTCAGTCAATGCAGTCAGTCAGTCA
EOF

echo "All test files created successfully."
