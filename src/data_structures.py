from dataclasses import dataclass
from typing import List


@dataclass
class LibraryScans:
    library_id: int
    time_at_which_it_was_signed_up: int
    scanned_books: List[int]