"""Sequence Alignment (Needleman-Wunsch) Module"""

## @file alignment.py
# @ingroup alignment_module
# @brief Needleman-Wunsch global sequence alignment implementation
# @dotfile alignment_workflow.dot

from typing import List


## @class NeedlemanWunsch
# @brief Global sequence alignment processor
# @ingroup alignment_module
#
# @param seq_a First sequence (5'->3')
# @param seq_b Second sequence (5'->3')
# @param gap_penalty Gap penalty score (default: -2)
#
# @var seq_a_aligned Final aligned version of seq_a
# @var seq_b_aligned Final aligned version of seq_b
# @var submat Active substitution matrix
class NeedlemanWunsch:
    """Implementation of Needleman-Wunsch global sequence alignment algorithm.
    
    Attributes:
        seq_a (str): First input sequence (5' to 3')
        seq_b (str): Second input sequence (5' to 3')
        gap_penalty (float): Penalty score for gaps
        submat: Active substitution matrix
        seq_a_aligned (str): Aligned version of seq_a
        seq_b_aligned (str): Aligned version of seq_b
    """

    ## @fn __init__(self, seq_a: str, seq_b: str, gap_penalty: float = -2)
    # @brief Initialize alignment processor
    # @param seq_a First sequence from @ref data_module
    # @param seq_b Second sequence from @ref data_module
    # @param gap_penalty Gap insertion penalty
    def __init__(self, seq_a: str, seq_b: str, gap_penalty: float = -2):
        self.seq_a = seq_a
        self.seq_b = seq_b
        self.gap_penalty = gap_penalty
        self.submat = None
        self.seq_a_aligned = ""
        self.seq_b_aligned = ""

    ## @fn __call__(self, submat)
    # @brief Execute alignment with given matrix
    # @param submat Substitution matrix from @ref matrix_module
    # @return Alignment score
    # @see SubMat::data
    def __call__(self, submat):
        """Execute alignment with given substitution matrix."""
        return self.align(submat)

    ## @fn evaluate_substitution(self, s1: str, s2: str) -> float
    # @brief Calculate nucleotide substitution score
    # @param s1 First nucleotide (A/T/G/C)
    # @param s2 Second nucleotide (A/T/G/C)
    # @return Score from substitution matrix
    # @throws ValueError Invalid nucleotide input
    def evaluate_substitution(self, s1: str, s2: str) -> float:
        """Calculate score for nucleotide substitution."""
        nucleotide_arr = ["A", "T", "G", "C"]
        try:
            s1_idx = nucleotide_arr.index(s1)
            s2_idx = nucleotide_arr.index(s2)
            
            # Handle both old and new matrix formats
            if isinstance(self.submat, dict):
                # New format: {"matrix": [[...]], "match": x, "mismatch": y, "gap": z}
                if "matrix" in self.submat:
                    return self.submat["matrix"][s1_idx][s2_idx]
                else:
                    # If no matrix, use match/mismatch values
                    return self.submat.get("match", 1) if s1 == s2 else self.submat.get("mismatch", -1)
            else:
                # Old format: direct matrix
                return self.submat[s1_idx][s2_idx]
                
        except (ValueError, IndexError, KeyError) as e:
            print(f"Alignment warning: {e}")
            return -1.0  # Default penalty for invalid cases

    ## @fn evaluate(self, x: int, y: int, direction: str, matrix: List[List[float]]) -> float
    # @brief Calculate DP matrix cell score
    # @param x Column index
    # @param y Row index
    # @param direction Movement direction (l=left, t=top, d=diagonal)
    # @param matrix Current DP matrix
    # @return Calculated cell score
    def evaluate(
            self, x: int, y: int, direction: str, matrix: List[List[float]]
    ) -> float:
        """Calculate score for dynamic programming matrix cell."""
        if direction == "l":
            return matrix[y][x - 1] + self.gap_penalty
        if direction == "t":
            return matrix[y - 1][x] + self.gap_penalty
        return matrix[y - 1][x - 1] + self.evaluate_substitution(
            self.seq_a[y], self.seq_b[x])

    ## @fn compute_alignment_matrix(self, matrix: List[List[float]]) -> List[List[float]]
    # @brief Build dynamic programming matrix
    # @param matrix Empty matrix (len(seq_a) x len(seq_b))
    # @return Filled DP matrix
    # @throws AlignmentError If sequences cannot be aligned
    def compute_alignment_matrix(
            self, matrix: List[List[float]]) -> List[List[float]]:
        """Construct dynamic programming matrix for alignment."""
        for y in range(len(self.seq_a)):
            for x in range(len(self.seq_b)):
                if y == 0 and x == 0:
                    matrix[y][x] = self.evaluate(x, y, "d", matrix)
                elif y == 0:
                    matrix[y][x] = self.evaluate(x, y, "l", matrix)
                elif x == 0:
                    matrix[y][x] = self.evaluate(x, y, "t", matrix)
                else:
                    matrix[y][x] = max(
                        self.evaluate(x, y, "l", matrix),
                        self.evaluate(x, y, "t", matrix),
                        self.evaluate(x, y, "d", matrix),
                    )
        return matrix

    ## @fn backtrack(self, matrix: List[List[float]]) -> float
    # @brief Trace optimal alignment path
    # @param matrix Filled DP matrix
    # @return Final alignment score
    # @post seq_a_aligned and seq_b_aligned contain aligned sequences
    def backtrack(self, matrix: List[List[float]]) -> float:
        """Traceback through DP matrix to find optimal alignment."""
        row_score = 0
        seq_a_aligned = ""
        seq_b_aligned = ""
        rev_seq_a = self.seq_a[::-1]
        rev_seq_b = self.seq_b[::-1]
        rev_matrix = [row[::-1] for row in matrix[::-1]]

        x, y = 0, 0
        while y < len(rev_matrix) and x < len(rev_matrix[0]):
            row_score += rev_matrix[y][x]
            if y == len(matrix) - 1 and x == len(matrix) - 1:
                seq_a_aligned += rev_seq_a[y]
                seq_b_aligned += rev_seq_b[x]
                x += 1
                y += 1
            elif y == len(rev_matrix) - 1:
                seq_a_aligned += "_"
                seq_b_aligned += rev_seq_b[x]
                x += 1
            elif x == len(rev_matrix[0]) - 1:
                seq_a_aligned += rev_seq_a[y]
                seq_b_aligned += "_"
                y += 1
            else:
                max_scores = [
                    rev_matrix[y][x + 1],
                    rev_matrix[y + 1][x],
                    rev_matrix[y + 1][x + 1]
                ]
                max_idx = max_scores.index(max(max_scores))

                if max_idx == 0:  # Right
                    seq_a_aligned += "_"
                    seq_b_aligned += rev_seq_b[x]
                    x += 1
                elif max_idx == 1:  # Down
                    seq_a_aligned += rev_seq_a[y]
                    seq_b_aligned += "_"
                    y += 1
                else:  # Diagonal
                    seq_a_aligned += rev_seq_a[y]
                    seq_b_aligned += rev_seq_b[x]
                    x += 1
                    y += 1

        self.seq_a_aligned = seq_a_aligned[::-1]
        self.seq_b_aligned = seq_b_aligned[::-1]
        return row_score

    ## @fn align(self, submat) -> float
    # @brief Complete alignment process
    # @param submat Valid substitution matrix from @ref matrix_module
    # @return Final alignment score
    # @throws AlignmentError If alignment fails
    def align(self, submat) -> float:
        """Perform complete alignment process with given substitution matrix."""
        self.submat = submat
        matrix = [[0 for _ in self.seq_b] for _ in self.seq_a]
        matrix = self.compute_alignment_matrix(matrix)
        return self.backtrack(matrix)
