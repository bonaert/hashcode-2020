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
    books: Set[int]