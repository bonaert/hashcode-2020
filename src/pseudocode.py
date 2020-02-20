books_already_scanned = set()
current_time = 0
remaining_libraries = [0, 1, 2, 3]
solution = []


def get_score_and_books(library, books_already_scanned, remaining_days):
    # Compute how many books we can scan
    unscanned_books = library.books - books_already_scanned
    max_books_we_can_scan = min(
        len(unscanned_books),
        library.scanning_speed * remaining_days
    )

    # Pick which books we will scan. Balance between picking the highest value books and the books
    # that are unique to this library

    # V1: pick the highest value books (very basic, very dumb)
    # TODO: be smarter than this
    scores_and_ids = [(book.score, book.id) for book in unscanned_books]
    chosen_scores_and_ids = sorted(scores_and_ids)[:max_books_we_can_scan]

    best_books, total_score = [], 0
    for (book_score, book_id) in chosen_scores_and_ids:
        best_books.append(book_id)
        total_score += book_score

    return best_books, total_score



"""
Current approach:
While there's still time, pick the library we're opening and the books we'll scan there

Other approach:
Look at it one day at the time. Each day, pick which books we will scan and, if it's possible, which library we will open.
"""

def find_solutions(libraries: List[Library], book_scores: List[int]):
    while current_time < maxTime:

        # Choisir la bibliothèque qu'on va lire
        best_score, best_library, best_books_to_scan = -1, -1, []
        for library in remaining_libraries:
            score, books_to_scan = get_score_and_books(library, books_already_scanned, maxTime - current_time - signup_time)
            if score > best_score:
                best_library = library
                best_score = score
                best_books_to_scan = books_to_scan

        books_already_scanned.add(best_books_to_scan)

        solution.append(
            LibraryScan(
                best_library,
                current_time,
                best_books_to_scan
            )
        )

        current_time += library.sign_up_time
