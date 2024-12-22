import os

dirname = os.path.dirname(__file__)
filename = os.path.join(dirname, "input.txt")


def get_data():
    out = []
    with open(filename) as f:
        for line in f.readlines():
            out.append(int(line.strip()))
    return out


def mix(x, y):
    return x ^ y


def prune(x):
    return x % 16777216


def get_prices(x):
    ans = [x]
    for _ in range(2000):
        x = prune(mix(x, 64*x))
        x = prune(mix(x, x//32))
        x = prune(mix(x, x*2048))
        ans.append(x)
    return ans


def get_changes(prices):
    return [
        prices[i+1] - prices[i] for i in range(len(prices) - 1)
    ]
    

def get_scores(prices, changes):
    out = {}
    for i in range(len(changes) - 3):
        pattern = (changes[i], changes[i + 1], changes[i + 2], changes[i + 3])
        if pattern not in out:
            out[pattern] = prices[i + 4]
    return out


def main_one():
    total = 0
    data = get_data()
    for number in data:
        total += get_prices(number)[-1]
    return total
        

def main_two():
    SCORE = {}
    data = get_data()
    for number in data:
        prices = get_prices(number)
        prices = [x % 10 for x in prices]  # Last digit
        changes = get_changes(prices)
        scores = get_scores(prices, changes)
        for k, v in scores.items():
            if k not in SCORE:
                SCORE[k] = v
            else:
                SCORE[k] += v
    
    return max(SCORE.values())


if __name__ == "__main__":
    print(main_one())
    print(main_two())
