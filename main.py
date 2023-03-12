import curses
from curses import wrapper
import queue
import time
from typing import List, Tuple
from functools import reduce


class Maze:
    def __init__(self, maze: List[List[str]]) -> None:
        self.maze = maze

    def print(self, stdscr, path=[]) -> None:
        BLUE = curses.color_pair(1)
        RED = curses.color_pair(2)

        for i, row in enumerate(self.maze):
            for j, value in enumerate(row):
                if (i, j) in path:
                    stdscr.addstr(i, j * 2, "X", RED)
                else:
                    stdscr.addstr(i, j * 2, value, BLUE)

    def find_start(self, start: str) -> Tuple[int, int]:
        for i, row in enumerate(self.maze):
            for j, value in enumerate(row):
                if value == start:
                    return i, j

        return None

    def find_path(self, stdscr) -> List[Tuple[int, int]]:
        start = "O"
        end = "X"
        start_pos = self.find_start(start)

        q = queue.Queue()
        q.put((start_pos, [start_pos]))

        visited = set()

        while not q.empty():
            current_pos, path = q.get()
            row, col = current_pos

            stdscr.clear()
            self.print(stdscr, path)
            time.sleep(0.2)
            stdscr.refresh()

            if self.maze[row][col] == end:
                return path

            neighbors = self.find_neighbors(row, col)
            for neighbor in neighbors:
                if neighbor in visited:
                    continue

                r, c = neighbor
                if self.maze[r][c] == "#":
                    continue

                new_path = path + [neighbor]
                q.put((neighbor, new_path))
                visited.add(neighbor)

    def find_neighbors(self, row: int, col: int) -> List[Tuple[int, int]]:
        neighbors = []

        if row > 0:  # UP
            neighbors.append((row - 1, col))
        if row + 1 < len(self.maze):  # DOWN
            neighbors.append((row + 1, col))
        if col > 0:  # LEFT
            neighbors.append((row, col - 1))
        if col + 1 < len(self.maze[0]):  # RIGHT
            neighbors.append((row, col + 1))

        return neighbors


def main(stdscr):
    curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
    curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)

    maze = Maze(
        [
            ["#", "O", "#", "#", "#", "#", "#", "#", "#"],
            ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
            ["#", " ", "#", "#", " ", "#", "#", " ", "#"],
            ["#", " ", "#", " ", " ", " ", "#", " ", "#"],
            ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
            ["#", " ", "#", " ", "#", " ", "#", " ", "#"],
            ["#", " ", "#", " ", "#", " ", "#", "#", "#"],
            ["#", " ", " ", " ", " ", " ", " ", " ", "#"],
            ["#", "#", "#", "#", "#", "#", "#", "X", "#"],
        ]
    )

    maze.find_path(stdscr)

    stdscr.getch()
    curses.endwin()


if __name__ == "__main__":
    wrapper(main)
