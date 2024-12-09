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

    front = 0
    while front < len(content):
        while content[front] != "." and front < len(content):
            front += 1
        start = front
        while content[front] == "." and front < len(content):
            front += 1
        end = front - 1
        free_space_length = end - start + 1

        back = len(content) - 1
        while back > 0:
            if content[back] != ".":
                back_begin = back
                while content[back_begin] == content[back]:
                    back_begin -= 1
                back_begin += 1
                if back - back_begin + 1 <= free_space_length:
                    break
                else:
                    back = back_begin
            back -= 1

        if start >= back_begin:
            break

        i = start
        for j in range(back_begin, back + 1):
            content[i] = content[j]
            content[j] = "."
            i += 1
        front = i

    return sum(i * int(id) if id != '.' else 0 for i, id in enumerate(content))


if __name__ == "__main__":
    print(main_one())
    print(main_two())
