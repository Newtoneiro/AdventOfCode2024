import os

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "input.txt")


def get_disc_map():
    content = []
    id = 0
    with open(filename) as f:
        is_content = True
        for n in f.read():
            if is_content:
                for _ in range(int(n)):
                    content.append(str(id))
                id += 1
            else:
                for _ in range(int(n)):
                    content.append('.')
            is_content = not is_content
    return content


def main_one():
    content = get_disc_map()

    back = len(content) - 1
    front = 0

    while front < back:
        if content[front] == ".":
            while content[back] == "." and front < back:
                back -= 1
            if front < back:
                content[front], content[back] = content[back], content[front]

        front += 1

    return sum(i * int(id) if id != '.' else 0 for i, id in enumerate(content))


def main_two():
    content = get_disc_map()

    back = len(content) - 1
    while back > 0:
        while content[back] == "." and back > 0:
            back -= 1
        back_begin = back
        while content[back_begin] == content[back] and back_begin > 0:
            back_begin -= 1
        back_begin += 1
        group_len = back - back_begin + 1

        front = 0
        while front < back_begin:
            if content[front] == ".":
                front_end = front
                while content[front_end] == ".":
                    front_end += 1
                front_end -= 1
                gap_len = front_end - front + 1
                if group_len <= gap_len:
                    break
                else:
                    front = front_end
            front += 1

        if back_begin <= front_end:
            break

        if front < back_begin:
            i = front
            for j in range(back_begin, back + 1):
                content[i] = content[j]
                content[j] = "."
                i += 1
        back = back_begin - 1

    return sum(i * int(id) if id != '.' else 0 for i, id in enumerate(content))


if __name__ == "__main__":
    print(main_one())
    print(main_two())
