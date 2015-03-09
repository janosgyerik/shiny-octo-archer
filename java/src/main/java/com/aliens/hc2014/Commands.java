package com.aliens.hc2014;

public class Commands {
    public static Command fromString(String s) {
        String[] parts = s.split(" ");
        int[] args = parseArgs(parts);

        String name = parts[0];

        switch (name) {
            case PaintCommand.NAME:
                return new PaintCommand(args[0], args[1], args[2]);
            case EraseCommand.NAME:
                return new EraseCommand(args[0], args[1]);
        }
        throw new UnsupportedOperationException("No such command: " + name);
    }

    private static int[] parseArgs(String[] parts) {
        int[] args = new int[parts.length - 1];
        for (int i = 1; i < parts.length; ++i) {
            args[i - 1] = Integer.parseInt(parts[i]);
        }
        return args;
    }

    interface Command {
        void apply(Facade facade);
    }

    static class PaintCommand implements Command {
        public static final String NAME = "PAINTSQ";

        private final int row;
        private final int col;
        private final int size;

        public PaintCommand(int row, int col, int size) {
            this.row = row;
            this.col = col;
            this.size = size;
        }

        public PaintCommand(Facade.Cell cell) {
            this.row = cell.row;
            this.col = cell.col;
            this.size = 0;
        }

        @Override
        public void apply(Facade facade) {
            if (size == 0) {
                facade.paintCell(row, col, '#');
            } else {
                facade.paintArea(row, col, size);
            }
        }

        @Override
        public String toString() {
            return String.format("%s %d %d %d", NAME, row, col, size);
        }
    }

    static class EraseCommand implements Command {
        public static final String NAME = "ERASECELL";

        private final int row;
        private final int col;

        public EraseCommand(int row, int col) {
            this.row = row;
            this.col = col;
        }

        @Override
        public void apply(Facade facade) {
            facade.paintCell(row, col, Facade.BLANK);
        }

        @Override
        public String toString() {
            return String.format("%s %d %d", NAME, row, col);
        }

        @Override
        public boolean equals(Object o) {
            if (this == o) {
                return true;
            }
            if (o == null || getClass() != o.getClass()) {
                return false;
            }

            EraseCommand that = (EraseCommand) o;

            if (col != that.col) {
                return false;
            }
            if (row != that.row) {
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
    }
}
