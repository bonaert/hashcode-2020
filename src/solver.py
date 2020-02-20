from typing import List, Set, Tuple

from data_structures import ProblemInfo, LibraryScans, Library


def get_score_and_books(
        problem_info: ProblemInfo,
        library: Library,
        books_already_scanned: Set[int],
        remaining_days: int) -> Tuple[float, List[int]]:
    # Pick which books we will scan. Balance between picking the highest value books and the books
    # that are unique to this library

    # V1: pick the highest value books (very basic, very dumb)
    # TODO: be smarter than this
    best_books, total_score = [], 0
    num_scanned_books = 0
    max_books_we_can_scan = library.ship_per_day * remaining_days

    if max_books_we_can_scan == 0:
        return 0, []

    books_to_delete = []
    for book in library.sorted_books_by_score:
        if book not in books_already_scanned:
            best_books.append(book)
            total_score += problem_info.book_scores[book]
            num_scanned_books += 1

            if num_scanned_books == max_books_we_can_scan:
                break
        else:
            books_to_delete.append(book)

    for book_to_delete in books_to_delete:
        library.sorted_books_by_score.remove(book_to_delete)

    return total_score / library.sign_up_time, best_books


"""
Current approach:
While there's still time, pick the library we're opening and the books we'll scan there

Other approach:
Look at it one day at the time. Each day, pick which books we will scan and, if it's possible, which library we will open.
"""


def find_solution(problem_info: ProblemInfo) -> List[LibraryScans]:
    books_already_scanned = set()
    current_time = 0
    remaining_libraries = problem_info.libraries
    solution = []

    step = 0

    print("Starting")
    while current_time < problem_info.num_days and remaining_libraries:
        # Choose the library we will sign up
        best_score, best_library, best_index, best_books_to_scan = -1, -1, 0, []
        for i, library in enumerate(remaining_libraries):
            # Not enough time to set up library
            if library.sign_up_time > problem_info.num_days - current_time:
                continue

            score, books_to_scan = get_score_and_books(problem_info, library, books_already_scanned,
                                                       problem_info.num_days - current_time - library.sign_up_time)
            if score > best_score:
                best_library = library
                best_score = score
                best_books_to_scan = books_to_scan
                best_index = i

        if best_score == -1 or len(best_books_to_scan) == 0:
            break

        solution.append(
            LibraryScans(
                library_id=best_library.id,
                time_at_which_it_was_signed_up=current_time,
                scanned_books=best_books_to_scan
            )
        )

        for book in best_books_to_scan:
            books_already_scanned.add(book)

        remaining_libraries.pop(best_index)
        current_time += best_library.sign_up_time

        if step % 10 == 0:
            print(f"Added {step}-th library - Day {current_time} out of {problem_info.num_days} days")
        step += 1

    print(f"Finished - Day {current_time} out of {problem_info.num_days} days")
    print()
    return solution
