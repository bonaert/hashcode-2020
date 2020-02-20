from typing import List

from data_structures import LibraryScans


def write_solution(ordered_solution: List[LibraryScans], filename: str):
    with open(filename, 'w') as f:
        f.write(f"{len(ordered_solution)}\n")

        for library_scan in ordered_solution:
            f.write(f"{library_scan.library_id} {len(library_scan.scanned_books)}\n")
            assert len(set(library_scan.scanned_books)) == len(library_scan.scanned_books), "Repeated books!"
            f.write(f"{' '.join(map(str, library_scan.scanned_books))}\n")


if __name__ == '__main__':
    solution = [
        LibraryScans(library_id=1, time_at_which_it_was_signed_up=0, scanned_books=[1, 2, 3]),
        LibraryScans(library_id=2, time_at_which_it_was_signed_up=5, scanned_books=[0, 1]),
        LibraryScans(library_id=3, time_at_which_it_was_signed_up=7, scanned_books=[4, 5, 1])
    ]
    write_solution(solution, "test.txt")
