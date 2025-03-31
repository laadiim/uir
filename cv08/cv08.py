import sys
from collections import defaultdict
from typing import Dict, List, Tuple, override


class Point:
    def __init__(self, x: float, y: float, type: str) -> None:
        self.x: float = x
        self.y: float = y
        self.type: str = type

    @override
    def __str__(self) -> str:
        return f"({self.x}, {self.y}, {self.type})"


def load(filename: str) -> Tuple[List[Point], List[Tuple[float, float]]]:
    lines: List[str] = []
    with open(filename, "r") as file:
        lines = file.readlines()

    points: List[Point] = []
    tests: List[Tuple[float, float]] = []

    first: bool = True
    switched: bool = False
    for line in lines:
        line = line.split(";")
        if first:
            first = False
            continue
        if len(line) == 2:
            if not switched:
                switched = True
                continue

            tests.append((float(line[0]), float(line[1])))
        else:
            points.append(Point(float(line[0]), float(line[1]), line[2]))

    return (points, tests)


def calculate_centroid(points: List[Point]) -> Tuple[float, float]:
    x: float = 0
    y: float = 0

    for point in points:
        x += point.x
        y += point.y

    x /= len(points)
    y /= len(points)
    return (x, y)


def solve_centroids(
    classes: Dict[str, List[Point]], tests: List[Tuple[float, float]]
) -> List[Point]:

    centroids: Dict[str, Tuple[float, float]] = {}

    for cls in classes:
        centroids[cls] = calculate_centroid(classes[cls])

    results: List[Point] = []
    for px, py in tests:
        closest: str = ""
        dist_sq: float = float("inf")

        for cls in centroids:
            cx: float = centroids[cls][0]
            cy: float = centroids[cls][1]
            ds: float = (px - cx) ** 2 + (py - cy) ** 2
            if ds < dist_sq:
                closest = cls
                dist_sq = ds

        results.append(Point(px, py, closest))

    return results


def solve_neighbours(
    points: List[Point], tests: List[Tuple[float, float]]
) -> List[Point]:
    results: List[Point] = []
    distances: Dict[Tuple[float, float], Dict[Point, float]] = defaultdict(dict)

    for px, py in tests:
        for point in points:
            cx: float = point.x
            cy: float = point.y
            ds: float = (px - cx) ** 2 + (py - cy) ** 2
            distances[(px, py)][point] = ds

    k: int = 3
    for px, py in tests:
        most: Tuple[str, int] = ("", 0)
        counts: Dict[str, int] = {}
        lowest: List[Tuple[Point, float]] = []
        for point in distances[(px, py)]:
            d: float = distances[(px, py)][point]
            if len(lowest) < k:
                lowest.append((point, d))
            else:
                if d < lowest[-1][1]:
                    lowest[-1] = (point, d)
            lowest.sort(key=lambda p: p[1], reverse=True)
        for i in lowest:
            if i[0].type not in counts.keys():
                counts[i[0].type] = 1
            else:
                counts[i[0].type] += 1
        print(counts)
        for cls, count in counts.items():
            if count > most[1]:
                most = (cls, count)
        results.append(Point(px, py, most[0]))
    return results


def main():
    points, tests = load(sys.argv[1])
    classes: Dict[str, List[Point]] = {}

    for point in points:
        if point.type not in classes.keys():
            classes[point.type] = [point]
        else:
            classes[point.type].append(point)

    centroid_result = solve_centroids(classes, tests)
    for r in centroid_result:
        print(r)

    centroid_result = solve_neighbours(points, tests)
    for r in centroid_result:
        print(r)


if __name__ == "__main__":
    main()
