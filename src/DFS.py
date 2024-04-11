from typing import Dict, Tuple
from src.pyamaze import maze, agent, COLOR, textLabel

def DFS(m: maze) -> Dict[Tuple[int, int], Tuple[int, int]]:
    """
    Perform Depth-First Search (DFS) on a maze.
    
    Args:
        m (maze): The maze object.
    
    Returns:
        Dict[Tuple[int, int], Tuple[int, int]]: The path found by DFS.
            Each key-value pair represents a cell and its parent cell in the path.
    """
    
    # Initialize start cell, explored set, frontier, and path dictionary
    start = (m.rows, m.cols)
    explored = [start]  # List to keep track of explored cells
    frontier = [start]  # Stack to keep track of cells to be explored
    dfsPath = {}  # Dictionary to store the parent-child relationship in the path

    # Main loop of DFS algorithm
    while len(frontier) > 0:
        currCell = frontier.pop()  # Get the next cell from the frontier (last-in, first-out)
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
                elif d == 'S':
                    childCell = (currCell[0] + 1, currCell[1])
                elif d == 'N':
                    childCell = (currCell[0] - 1, currCell[1])
                if childCell in explored:  # Skip if already explored
                    continue
                # Add the child cell to the explored set and frontier
                explored.append(childCell)
                frontier.append(childCell)
                dfsPath[childCell] = currCell  # Record the parent-child relationship

    # Reconstruct the path from the destination to the start cell
    fwdPath = {}
    cell = (1, 1)
    while cell != start:
        fwdPath[dfsPath[cell]] = cell
        cell = dfsPath[cell]
    
    return fwdPath


if __name__ == '__main__':
    m = maze(15)
    m.CreateMaze(loopPercent=25)
    path = DFS(m)
    
    a = agent(m, footprints=True)
    m.tracePath({a: path})
    l = textLabel(m, 'Length of Shortest Path', len(path) + 1)
    
    # Run the maze
    m.run()
