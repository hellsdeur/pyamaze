from typing import Dict, Tuple, List
from src.pyamaze import maze, agent, COLOR, textLabel

def BFS(m: maze) -> Dict[Tuple[int, int], Tuple[int, int]]:
    """
    Perform Breadth-First Search (BFS) on a maze.

    Args:
        m (Maze): The maze object.

    Returns:
        Dict[Tuple[int, int], Tuple[int, int]]: The path found by BFS.
            Each key-value pair represents a cell and its parent cell in the path.
    """

    # Initialize start cell, frontier, explored set, and path dictionary
    start = (m.rows, m.cols)
    frontier = [start]  # List to keep track of cells to be explored
    explored = [start]  # List to keep track of explored cells
    bfsPath = {}  # Dictionary to store the parent-child relationship in the path

    # Main loop of BFS algorithm
    while len(frontier) > 0:
        currCell = frontier.pop(0)  # Get the next cell from the frontier (first-in, first-out)
        if currCell == (1, 1):  # Check if the destination is reached
            break
        # Iterate through possible directions
        for d in 'ESNW':
            if m.maze_map[currCell][d]:
                # Calculate the child cell based on the current direction
                if d == 'E':
                    childCell = (currCell[0], currCell[1] + 1)
                elif d == 'W':
                    childCell = (currCell[0], currCell[1] - 1)
                elif d == 'N':
                    childCell = (currCell[0] - 1, currCell[1])
                elif d == 'S':
                    childCell = (currCell[0] + 1, currCell[1])
                if childCell in explored:  # Skip if already explored
                    continue
                # Add the child cell to the frontier and explored set
                frontier.append(childCell)
                explored.append(childCell)
                bfsPath[childCell] = currCell  # Record the parent-child relationship

    # Reconstruct the path from the destination to the start cell
    fwdPath = {}
    cell = (1, 1)
    while cell != start:
        fwdPath[bfsPath[cell]] = cell
        cell = bfsPath[cell]
    
    return fwdPath


if __name__ == '__main__':
    m = maze(15)
    m.CreateMaze(loopPercent=25)
    path = BFS(m)
    
    a = agent(m, footprints=True)
    m.tracePath({a: path})
    l = textLabel(m, 'Length of Shortest Path', len(path) + 1)
    
    m.run()
