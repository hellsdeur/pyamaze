from typing import Any, Tuple, Dict
from src.pyamaze import maze, agent, COLOR, textLabel

def dijkstra(m: maze, *h: Tuple[Any, int], start: Tuple[int, int] = None) -> Tuple[Dict[Tuple[int, int], Tuple[int, int]], int]:
    """
    Perform Dijkstra's algorithm on a maze.

    Args:
        m (maze): The maze object.
        *h (Tuple[Any, int]): Tuple containing hurdles with their positions and costs.
        start (Tuple[int, int], optional): The starting position. Defaults to None, using the bottom-right corner.

    Returns:
        Tuple[Dict[Tuple[int, int], Tuple[int, int]], int]: A tuple containing:
            - The path found by Dijkstra's algorithm. Each key-value pair represents a cell and its parent cell in the path.
            - The total cost of the path.
    """
    if start is None:
        start = (m.rows, m.cols)

    hurdles = [(i.position, i.cost) for i in h]

    unvisited = {n: float('inf') for n in m.grid}
    unvisited[start] = 0
    visited = {}
    revPath = {}

    # Main loop of Dijkstra's algorithm
    while unvisited:
        currCell = min(unvisited, key=unvisited.get)  # Get the cell with the minimum distance
        visited[currCell] = unvisited[currCell]  # Move the cell from unvisited to visited
        if currCell == m._goal:  # Check if the destination is reached
            break
        # Iterate through possible directions
        for d in 'EWNS':
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
                if childCell in visited:  # Skip if already visited
                    continue
                tempDist = unvisited[currCell] + 1
                for hurdle in hurdles:  # Check for hurdles and add their costs
                    if hurdle[0] == currCell:
                        tempDist += hurdle[1]

                # Update the distance of the child cell if a shorter path is found
                if tempDist < unvisited[childCell]:
                    unvisited[childCell] = tempDist
                    revPath[childCell] = currCell
        unvisited.pop(currCell)  # Remove the current cell from the unvisited set

    # Reconstruct the path from the destination to the start cell
    fwdPath = {}
    cell = m._goal
    while cell != start:
        fwdPath[revPath[cell]] = cell
        cell = revPath[cell]

    return fwdPath, visited[m._goal]

if __name__ == '__main__':
    myMaze = maze(15)
    myMaze.CreateMaze(1, 4, loopPercent=25)

    # Create hurdles (agents)
    h1 = agent(myMaze, 4, 4, color=COLOR.red)
    h2 = agent(myMaze, 4, 6, color=COLOR.red)
    h3 = agent(myMaze, 4, 1, color=COLOR.red)
    h4 = agent(myMaze, 4, 2, color=COLOR.red)
    h5 = agent(myMaze, 4, 3, color=COLOR.red)

    # Set costs for hurdles
    h1.cost = 100
    h2.cost = 100
    h3.cost = 100
    h4.cost = 100
    h5.cost = 100

    path, c = dijkstra(myMaze, h1, h2, h3, h4, h5, start=(6, 1))
    textLabel(myMaze, 'Total Cost', c)
    a = agent(myMaze, 6, 1, color=COLOR.cyan, filled=True, footprints=True)
    myMaze.tracePath({a: path})
    
    myMaze.run()
