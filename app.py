
import streamlit as st
import pandas as pd
from typing import List

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Sudoku Validator",
    page_icon="🔢",
    layout="wide"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #101827, #17243a);
    color: white;
}

.block-container {
    padding-top: 2rem;
    max-width: 1100px;
}

h1, h2, h3, p, label {
    color: #f1f5f9 !important;
}

.subtitle {
    color: #94a3b8;
    font-size: 17px;
    margin-bottom: 25px;
}

div.stButton > button {
    background: #6366f1;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 12px 25px;
    font-weight: bold;
    transition: 0.3s;
}

div.stButton > button:hover {
    background: #818cf8;
    color: white;
    border: none;
}

.metric-card {
    background: #1e293b;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #334155;
    text-align: center;
}

.metric-number {
    font-size: 30px;
    font-weight: bold;
    color: #818cf8;
}

.metric-label {
    color: #94a3b8;
    font-size: 14px;
}

.result-valid {
    background: #064e3b;
    border: 1px solid #10b981;
    color: #a7f3d0;
    padding: 18px;
    border-radius: 12px;
    font-size: 19px;
    font-weight: bold;
}

.result-invalid {
    background: #7f1d1d;
    border: 1px solid #ef4444;
    color: #fecaca;
    padding: 18px;
    border-radius: 12px;
    font-size: 19px;
    font-weight: bold;
}

[data-testid="stDataFrame"] {
    border-radius: 12px;
}

</style>
""", unsafe_allow_html=True)


# ---------------- SUDOKU LOGIC ----------------

class Solution:
    def isValidSudoku(self, board: List[List[str]]) -> bool:

        rows = [set() for _ in range(9)]
        cols = [set() for _ in range(9)]
        boxes = [set() for _ in range(9)]

        for i in range(9):
            for j in range(9):

                if board[i][j] == ".":
                    continue

                num = board[i][j]
                box = (i // 3) * 3 + (j // 3)

                if (
                    num in rows[i]
                    or num in cols[j]
                    or num in boxes[box]
                ):
                    return False

                rows[i].add(num)
                cols[j].add(num)
                boxes[box].add(num)

        return True


# ---------------- SAMPLE BOARD ----------------

sample_board = [
    ["5", "3", ".", ".", "7", ".", ".", ".", "."],
    ["6", ".", ".", "1", "9", "5", ".", ".", "."],
    [".", "9", "8", ".", ".", ".", ".", "6", "."],
    ["8", ".", ".", ".", "6", ".", ".", ".", "3"],
    ["4", ".", ".", "8", ".", "3", ".", ".", "1"],
    ["7", ".", ".", ".", "2", ".", ".", ".", "6"],
    [".", "6", ".", ".", ".", ".", "2", "8", "."],
    [".", ".", ".", "4", "1", "9", ".", ".", "5"],
    [".", ".", ".", ".", "8", ".", ".", "7", "9"]
]


# ---------------- SESSION STATE ----------------

if "board_data" not in st.session_state:
    st.session_state.board_data = pd.DataFrame(
        sample_board,
        columns=[f"C{i+1}" for i in range(9)]
    )

if "editor_version" not in st.session_state:
    st.session_state.editor_version = 0


# ---------------- HEADER ----------------

st.markdown(
    "<h1 style='text-align:center;'>🔢 Sudoku Validator</h1>",
    unsafe_allow_html=True
)

st.markdown(
    "<p class='subtitle' style='text-align:center;'>"
    "A smart Sudoku validation tool powered by Python"
    "</p>",
    unsafe_allow_html=True
)

st.divider()


# ---------------- TOP METRICS ----------------

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-number">9×9</div>
        <div class="metric-label">Sudoku Grid</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-number">3</div>
        <div class="metric-label">Validation Rules</div>
    </div>
    """, unsafe_allow_html=True)

with col3:
    st.markdown("""
    <div class="metric-card">
        <div class="metric-number">81</div>
        <div class="metric-label">Total Cells</div>
    </div>
    """, unsafe_allow_html=True)


st.write("")
st.subheader("🧩 Enter Your Sudoku")
st.caption(
    "Enter numbers from 1–9. Leave empty cells blank. "
    "You can edit the grid directly."
)


# ---------------- SUDOKU GRID ----------------

edited_board = st.data_editor(
    st.session_state.board_data,
    key=f"sudoku_editor_{st.session_state.editor_version}",
    hide_index=True,
    use_container_width=True,
    num_rows="fixed",
    column_config={
        f"C{i+1}": st.column_config.TextColumn(
            label=f"{i+1}",
            max_chars=1,
            width="small"
        )
        for i in range(9)
    }
)

st.session_state.board_data = edited_board.copy()


# ---------------- BUTTONS ----------------

st.write("")

col1, col2, col3 = st.columns(3)

with col1:
    validate = st.button(
        "🔍 Validate Sudoku",
        use_container_width=True
    )

with col2:
    load_sample = st.button(
        "📋 Load Sample",
        use_container_width=True
    )

with col3:
    clear = st.button(
        "🗑️ Clear Board",
        use_container_width=True
    )


# ---------------- BUTTON FUNCTIONALITY ----------------

if load_sample:
    st.session_state.board_data = pd.DataFrame(
        sample_board,
        columns=[f"C{i+1}" for i in range(9)]
    )
    st.session_state.editor_version += 1
    st.rerun()


if clear:
    st.session_state.board_data = pd.DataFrame(
        [["" for _ in range(9)] for _ in range(9)],
        columns=[f"C{i+1}" for i in range(9)]
    )
    st.session_state.editor_version += 1
    st.rerun()


# ---------------- VALIDATION ----------------

if validate:

    board = []
    error = False

    for i in range(9):
        row = []

        for j in range(9):

            value = str(edited_board.iloc[i, j]).strip()

            if value == "" or value == ".":
                row.append(".")

            elif value in "123456789" and len(value) == 1:
                row.append(value)

            else:
                error = True
                break

        if error:
            break

        board.append(row)

    st.divider()
    st.subheader("📊 Validation Result")

    if error:

        st.markdown("""
        <div class="result-invalid">
            ❌ Invalid Input! Please enter only digits from 1 to 9.
        </div>
        """, unsafe_allow_html=True)

    else:

        solution = Solution()

        if solution.isValidSudoku(board):

            st.markdown("""
            <div class="result-valid">
                ✅ Valid Sudoku! No duplicate numbers found.
            </div>
            """, unsafe_allow_html=True)

            st.balloons()

        else:

            st.markdown("""
            <div class="result-invalid">
                ❌ Invalid Sudoku! Duplicate number detected
                in a row, column, or 3×3 box.
            </div>
            """, unsafe_allow_html=True)


# ---------------- VALIDATION RULES ----------------

st.divider()

st.subheader("📖 How Sudoku Validation Works")

rule1, rule2, rule3 = st.columns(3)

with rule1:
    st.markdown("""
    **1. Row Validation**

    Each row must contain no repeated digits from 1 to 9.
    """)

with rule2:
    st.markdown("""
    **2. Column Validation**

    Each column must contain no repeated digits from 1 to 9.
    """)

with rule3:
    st.markdown("""
    **3. 3×3 Box Validation**

    Every 3×3 box must contain no repeated digits.
    """)

st.divider()

st.markdown(
    "<p style='text-align:center;color:#94a3b8;'>"
    "Built with Python & Streamlit | Sudoku Validator"
    "</p>",
    unsafe_allow_html=True
)
