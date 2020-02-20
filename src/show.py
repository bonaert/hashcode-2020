import matplotlib.pyplot as plt
from read import read_input

for filename in ["a_example.txt", "b_read_on.txt", "c_incunabula.txt",
                 "d_tough_choices.txt", "e_so_many_books.txt", "f_libraries_of_the_world.txt"]:
    problem_info = read_input("data/" + filename)

    signup_times = [library.sign_up_time for library in problem_info.libraries]
    scan_speed_times = [library.ship_per_day for library in problem_info.libraries]
    num_books = [len(library.sorted_books_by_score) for library in problem_info.libraries]

    book_distribution = [0] * len(problem_info.book_scores)
    for library in problem_info.libraries:
        for book in library.sorted_books_by_score:
            book_distribution[book] += 1

    plt.figure()
    plt.hist(signup_times, bins=len(set(signup_times)))
    plt.savefig(f"images/{filename}-signuptimes.png")

    plt.figure()
    plt.hist(scan_speed_times, bins=len(set(scan_speed_times)))
    plt.savefig(f"images/{filename}-scanspeed.png")

    plt.figure()
    plt.hist(num_books, bins=len(set(num_books)))
    plt.savefig(f"images/{filename}-numbooks.png")

    plt.figure()
    plt.hist(book_distribution, bins=len(set(book_distribution)))
    plt.savefig(f"images/{filename}-book_distribution.png")

    plt.figure()
    plt.hist(problem_info.book_scores, bins=len(set(problem_info.book_scores)))
    plt.savefig(f"images/{filename}-book_scores.png")
