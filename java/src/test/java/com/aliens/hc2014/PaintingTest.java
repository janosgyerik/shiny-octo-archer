package com.aliens.hc2014;


import org.junit.Test;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.util.*;

import static org.junit.Assert.assertEquals;

public class PaintingTest {

    private String commandsToString(List<Commands.Command> commands) {
        String newline = String.format("%n");

        StringBuilder builder = new StringBuilder();
        builder.append(commands.size()).append(newline);

        for (Commands.Command command : commands) {
            builder.append(command).append(newline);
        }
        return builder.toString();
    }

    private List<Commands.Command> generateNaiveSolution(Facade facade) {
        List<Commands.Command> commands = new LinkedList<>();
        Set<Facade.Cell> cells = facade.getPaintedCells();
        for (Facade.Cell cell : cells) {
            commands.add(new Commands.PaintCommand(cell));
        }
        return commands;
    }

    private List<Commands.Command> generateSolutionUsing3x3(Facade facade) {
        Set<Facade.Cell> originalPaintedCells = facade.getPaintedCells();
        Set<Facade.Cell> paintedCells = new HashSet<>(originalPaintedCells);
        SortedSet<Facade.CellWithPaintedNeighborCount> cellsWithPaintedNeighborCount = facade
                .getCellsWithPaintedNeighborCount(paintedCells, 6);

        List<Commands.Command> commands = new LinkedList<>();
        Set<Commands.Command> eraseCommands = new HashSet<>();
        for (Facade.CellWithPaintedNeighborCount cellWithPaintedNeighborCount : cellsWithPaintedNeighborCount) {
            Facade.Cell cell = cellWithPaintedNeighborCount.cell;
            commands.add(new Commands.PaintCommand(cell.row, cell.col, 1));
            if (!originalPaintedCells.contains(cell)) {
                eraseCommands.add(new Commands.EraseCommand(cell.row, cell.col));
            }

            paintedCells.remove(cell);
            for (Facade.Cell neighbor : facade.getValidNeighbors(cell)) {
                paintedCells.remove(neighbor);
                if (!originalPaintedCells.contains(neighbor)) {
                    eraseCommands.add(new Commands.EraseCommand(neighbor.row, neighbor.col));
                }
            }
        }

        for (Facade.Cell cell : paintedCells) {
            commands.add(new Commands.PaintCommand(cell));
        }
        commands.addAll(eraseCommands);
        return new LinkedList<>(commands);
    }

    private String execute(Facade facade, Scanner commands) {
        int commandsCount = commands.nextInt();
        commands.nextLine();
        for (int i = 0; i < commandsCount; ++i) {
            String commandString = commands.nextLine();
            Commands.Command command = Commands.fromString(commandString);
            command.apply(facade);
        }
        return facade.toString();
    }

    private String execute(Facade facade, List<Commands.Command> commands) {
        for (Commands.Command command : commands) {
            command.apply(facade);
        }
        return facade.toString();
    }

    private final String simpleFacadeString = "5 7\n" +
            "....#..\n" +
            "..###..\n" +
            "..#.#..\n" +
            "..###..\n" +
            "..#....\n";

    private final Facade simpleFacade = Facade.fromScanner(new Scanner(simpleFacadeString));

    @Test
    public void testExecuteSimpleExample() {
        assertEquals(simpleFacadeString, execute(simpleFacade, new Scanner("4\n" +
                        "PAINTSQ 2 3 1\n" +
                        "PAINTSQ 0 4 0\n" +
                        "PAINTSQ 4 2 0\n" +
                        "ERASECELL 2 3\n")));
    }

    @Test
    public void testNaiveSolution() {
        assertEquals(simpleFacadeString,
                execute(simpleFacade, new Scanner(commandsToString(generateNaiveSolution(simpleFacade)))));
    }

    @Test
    public void testSolutionUsing3x3() {
        assertEquals(simpleFacadeString,
                execute(simpleFacade, new Scanner(commandsToString(generateSolutionUsing3x3(simpleFacade)))));
    }

    private static final Facade longFacade;
    private static final String longFacadeString;

    static {
        Facade facade = null;
        try {
            facade = Facade.fromScanner(new Scanner(new File("src/test/resources/hc2014/doodle.txt")));
        } catch (FileNotFoundException e) {
            facade = new Facade(0, 0);
        }
        longFacade = facade;
        longFacadeString = facade.toString();
    }

    @Test
    public void testLongSolutionUsingNaive() {
        List<Commands.Command> commands = generateNaiveSolution(longFacade);
        assertEquals(185309, commands.size());
        assertEquals(longFacadeString, execute(longFacade, commands));
    }

    @Test
    public void testLongSolutionUsing3x3() throws IOException {
        List<Commands.Command> commands = generateSolutionUsing3x3(longFacade);
        assertEquals(185148, commands.size());
        assertEquals(longFacadeString, execute(longFacade, commands));
        //        try (FileWriter writer = new FileWriter("/tmp/facade.out")) {
        //            writer.write(commandsToString(commands));
        //        }
    }

}
