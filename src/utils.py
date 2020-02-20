from collections import namedtuple

Librairy = namedtuple("Librairy", ["id", "sign_up_time", "ship_per_day", "books"])


def read_input(filename):
    librairies = []
    with open(filename, "r") as f:
        lines = f.readlines()
        num_librairies = int(lines[0].split(" ")[1])
        book_scores = lines[1].strip().split(" ")

        start_lib_def = 2
        for i_lib in range(num_librairies):
            line_num = start_lib_def + (i_lib * 2)
            num_book, sign_up_time, ship_per_day = lines[line_num].split() 
            books_in_lib = lines[line_num + 1].split()
            librairies.append(Librairy(i_lib, sign_up_time, ship_per_day, books_in_lib))
            
    return librairies, book_scores



libs, bs = read_input("data/a_example.txt")
print(bs)
for l in libs:
    print(l)

# print(bs)