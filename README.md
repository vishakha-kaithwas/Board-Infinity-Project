# 36. Valid Sudoku

## Intuition

We only need to ensure every digit appears once in:
- each row
- each column
- each 3×3 box

HashSets make duplicate checking efficient.

## Approach

- Create 9 sets for rows.
- Create 9 sets for columns.
- Create 9 sets for boxes.
- Traverse the board.
- Ignore '.'.
- Compute the box index:
box = (row // 3) * 3 + (col // 3)

- If the digit already exists in any corresponding set, return False.
- Otherwise, insert it into all three sets.

## Complexity

- Time: O(81) = O(1)
- Space: O(81) = O(1)
