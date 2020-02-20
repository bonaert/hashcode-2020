from data_structures import LibraryScans
from write import write_solution


def read_input(filename):
    return None


def solve(data):
    solution = [
        LibraryScans(library_id=1, time_at_which_it_was_signed_up=0, scanned_books=[1, 2, 3]),
        LibraryScans(library_id=2, time_at_which_it_was_signed_up=5, scanned_books=[0, 1]),
        LibraryScans(library_id=3, time_at_which_it_was_signed_up=7, scanned_books=[4, 5, 1])
    ]
    return solution


for filename in ["a_example.txt", "b_read_on.txt", "c_incunabula.txt",
                 "d_tough_choices.txt", "e_so_many_books.txt", "f_libraries_of_the_world.txt"]:
    data = read_input("data/" + filename)
    solution = solve(data)
    write_solution(solution, "solutions/" + filename)
