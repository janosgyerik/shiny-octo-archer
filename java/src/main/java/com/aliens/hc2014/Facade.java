package com.aliens.hc2014;

import java.util.*;

public class Facade {
    static final char BLANK = '.';
    private static final char PAINTED = '#';

    static class Cell {
        final int row;
        final int col;

        Cell(int row, int col) {
            this.row = row;
            this.col = col;
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) {
                return true;
            }
            if (o == null || getClass() != o.getClass()) {
                return false;
            }

            Cell cell = (Cell) o;

            if (col != cell.col) {
                return false;
            }
            if (row != cell.row) {
                return false;
            }

            return true;
        }

        @Override
        public int hashCode() {
            int result = row;
            result = 31 * result + col;
            return result;
        }

        @Override
        public String toString() {
            return String.format("(%s,%s)", row, col);
        }

        public Cell afterMove(MoveOffset moveOffset) {
            return new Cell(row + moveOffset.rowOffset, col + moveOffset.colOffset);
        }
    }

    static class CellWithPaintedNeighborCount implements Comparable<CellWithPaintedNeighborCount> {
        final Cell cell;
        private final int count;

        public CellWithPaintedNeighborCount(Cell cell, int count) {
            this.cell = cell;
            this.count = count;
        }

        @Override
        public int compareTo(CellWithPaintedNeighborCount o) {
            int compare = Integer.compare(count, o.count);
            if (compare != 0) {
                return -compare;
            }
            compare = Integer.compare(cell.row, o.cell.row);
            if (compare != 0) {
                return compare;
            }
            return Integer.compare(cell.col, o.cell.col);
        }

        @Override
        public String toString() {
            return String.format("%s:%s", cell, count);
        }
    }

    final int height;
    final int width;
    final char[][] facade;

    Facade(int height, int width) {
        this.height = height;
        this.width = width;
        this.facade = new char[height][width];

        for (int i = 0; i < height; ++i) {
            for (int j = 0; j < width; ++j) {
                facade[i][j] = BLANK;
            }
        }
    }

    private void updateRow(int row, String s) {
        facade[row] = s.toCharArray();
    }

    public static Facade fromScanner(Scanner scanner) {
        int height = scanner.nextInt();
        int width = scanner.nextInt();
        scanner.nextLine();
        Facade facade = new Facade(height, width);
        for (int i = 0; i < height; ++i) {
            facade.updateRow(i, scanner.nextLine());
        }
        return facade;
    }

    public Set<Cell> getPaintedCells() {
        Set<Cell> painted = new HashSet<>();
        for (int row = 0; row < height; ++row) {
            for (int col = 0; col < width; ++col) {
                if (isPainted(row, col)) {
                    painted.add(new Cell(row, col));
                }
            }
        }
        return painted;
    }

    public SortedSet<CellWithPaintedNeighborCount> getCellsWithPaintedNeighborCount(Set<Cell> cells, int threshold) {
        SortedSet<CellWithPaintedNeighborCount> result = new TreeSet<>();
        for (Cell cell : cells) {
            for (Cell neighbor : getValidNeighbors(cell)) {
                int count = countPaintedNeighbors(neighbor);
                if (count < threshold) {
                    continue;
                }
                result.add(new CellWithPaintedNeighborCount(neighbor, count));
            }
        }
        return result;
    }

    enum MoveOffset {
        UPLEFT(-1, -1),
        UP(-1, 0),
        UPRIGHT(-1, 1),
        RIGHT(0, 1),
        DOWNRIGHT(1, 1),
        DOWN(1, 0),
        DOWNLEFT(1, -1),
        LEFT(0, -1)
        ;
        private final int rowOffset;
        private final int colOffset;

        MoveOffset(int rowOffset, int colOffset) {
            this.rowOffset = rowOffset;
            this.colOffset = colOffset;
        }
    }

    List<Cell> getValidNeighbors(Cell cell) {
        List<Cell> validNeighbors = new LinkedList<>();
        for (MoveOffset moveOffset : MoveOffset.values()) {
            Cell neighbor = cell.afterMove(moveOffset);
            if (0 <= neighbor.row && neighbor.row < height
                    && 0 <= neighbor.col && neighbor.col < width) {
                validNeighbors.add(neighbor);
            }
        }
        return validNeighbors;
    }

    private int countPaintedNeighbors(Cell cell) {
        int count = 0;
        for (Cell neighbor : getValidNeighbors(cell)) {
            if (isPainted(neighbor)) {
                ++count;
            }
        }
        return count;
    }

    private boolean isPainted(int row, int col) {
        return facade[row][col] == PAINTED;
    }

    private boolean isPainted(Cell cell) {
        return isPainted(cell.row, cell.col);
    }

    @Override
    public String toString() {
        StringBuilder builder = new StringBuilder((width + 1) * (height + 1));
        String newline = String.format("%n");
        builder.append(height).append(' ').append(width).append(newline);
        for (char[] row : facade) {
            builder.append(new String(row)).append(newline);
        }
        return builder.toString();
    }

    public void paintArea(int row, int col, int size) {
        int width = size * 2 + 1;
        int startrow = row - size;
        int startcol = col - size;
        for (int i = 0; i < width; ++i) {
            for (int j = 0; j < width; ++j) {
                facade[startrow + i][startcol + j] = PAINTED;
            }
        }
    }

    public void paintCell(int row, int col, char brush) {
        facade[row][col] = brush;
    }
}
