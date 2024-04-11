from typing import Dict, Tuple
from src.pyamaze import maze,agent,textLabel
from queue import PriorityQueue

def h(cell1: Tuple[int, int], cell2: Tuple[int, int]) -> int:
    """
    Heuristic function for A* algorithm.
    
    Args:
        cell1 (Tuple[int, int]): Coordinates of the first cell.
        cell2 (Tuple[int, int]): Coordinates of the second cell.
    
    Returns:
        int: Manhattan distance between the two cells.
    """
    x1, y1 = cell1
    x2, y2 = cell2
    return abs(x1 - x2) + abs(y1 - y2)

def aStar(m: maze) -> Dict[Tuple[int, int], Tuple[int, int]]:
    """
    Perform A* search on a maze.
    
    Args:
        m (maze): The maze object.
    
    Returns:
        Dict[Tuple[int, int], Tuple[int, int]]: The path found by A*.
            Each key-value pair represents a cell and its parent cell in the path.
    """

    # Initialize start cell, g_score, and f_score dictionaries
    start = (m.rows, m.cols)
    g_score = {cell: float('inf') for cell in m.grid}
    g_score[start] = 0
    f_score = {cell: float('inf') for cell in m.grid}
    f_score[start] = h(start, (1, 1))

    # Initialize priority queue for open set and dictionary to store the path
    open_set = PriorityQueue()
    open_set.put((h(start, (1, 1)), h(start, (1, 1)), start))
    aPath = {}

    # Main loop of A* algorithm
    while not open_set.empty():
        currCell = open_set.get()[2]
        if currCell == (1, 1):
            break

        # Iterate through possible directions
        for d in 'ESNW':
            if m.maze_map[currCell][d]:
                # Calculate the child cell based on the current direction
                if d == 'E':
                    childCell = (currCell[0], currCell[1] + 1)
                if d == 'W':
                    childCell = (currCell[0], currCell[1] - 1)
                if d == 'N':
                    childCell = (currCell[0] - 1, currCell[1])
                if d == 'S':
                    childCell = (currCell[0] + 1, currCell[1])

                # Calculate tentative g_score and f_score for the child cell
                temp_g_score = g_score[currCell] + 1
                temp_f_score = temp_g_score + h(childCell, (1, 1))

                # Update scores and add the child cell to the open set if it's better than before
                if temp_f_score < f_score[childCell]:
                    g_score[childCell] = temp_g_score
                    f_score[childCell] = temp_f_score
                    open_set.put((temp_f_score, h(childCell, (1, 1)), childCell))
                    aPath[childCell] = currCell

    # Reconstruct the path from the destination to the start cell
    fwdPath = {}
    cell = (1, 1)
    while cell != start:
        fwdPath[aPath[cell]] = cell
        cell = aPath[cell]
    
    return fwdPath



if __name__ == '__main__':
    m = maze(15)
    m.CreateMaze(loopPercent=25)
    path = aStar(m)
    
    a = agent(m, footprints=True)
    m.tracePath({a: path})
    l = textLabel(m, 'A Star Path Length', len(path) + 1)
    
    m.run()
