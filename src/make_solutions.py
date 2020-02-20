from read import read_input
from solver import find_solution
from write import write_solution


for filename in [
    # "a_example.txt",
    # "b_read_on.txt",
    # "c_incunabula.txt",
    "d_tough_choices.txt",
    # "e_so_many_books.txt",
    # "f_libraries_of_the_world.txt"
]:
    problem_info = read_input("data/" + filename)
    solution = find_solution(problem_info)
    write_solution(solution, "solutions/" + filename)
