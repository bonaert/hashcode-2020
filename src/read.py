from typing import Tuple, List

from data_structures import Library, ProblemInfo


def read_input(filename: str) -> Tuple[List[Library], List[int]]:
    libraries = []
    with open(filename, "r") as f:
        lines = f.readlines()
        num_days = lines[0].split()[-1]
        num_libraries = int(lines[0].split(" ")[1])
        book_scores = list(map(int, lines[1].strip().split(" ")))

        start_lib_def = 2
        for i_lib in range(num_libraries):
            line_num = start_lib_def + (i_lib * 2)
            num_book, sign_up_time, ship_per_day = list(map(int, lines[line_num].split()))
            books_in_lib = set(map(int, lines[line_num + 1].split()))
            libraries.append(
                Library(i_lib, sign_up_time, ship_per_day, books_in_lib)
            )

    return ProblemInfo(libraries, book_scores, num_days)

if __name__ == '__main__':
    problemInfo = read_input("data/a_example.txt")
    print(problemInfo)

    # print(bs)
