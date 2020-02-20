from dataclasses import dataclass
from typing import List, Set


@dataclass
class LibraryScans:
    library_id: int
    time_at_which_it_was_signed_up: int
    scanned_books: List[int]


@dataclass
class Library:
    id: int
    sign_up_time: int
    ship_per_day: int
    sorted_books_by_score: List[int]


@dataclass
class ProblemInfo:
    libraries: List[Library]
    book_scores: List[int]
    num_days: int
    book_frequency: List[int]
