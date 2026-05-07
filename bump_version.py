import os, sys, re, subprocess, argparse

VERSION_FILE = 'VERSION'

FRUITS = [
    "Apple", "Banana", "Cherry", "Date", "Elderberry", "Fig", "Grape", "Honeydew",
    "Kiwi", "Lemon", "Mango", "Nectarine", "Orange", "Papaya", "Quince", "Raspberry",
    "Strawberry", "Tangerine", "Ugli", "Vanilla", "Watermelon", "Xigua", "Yuzu", "Zucchini"
]

def get_fruit_codename(major, minor):
    index = (major * 10 + minor) % len(FRUITS)
    return FRUITS[index]

def read_version():
    if not os.path.exists(VERSION_FILE):
        return [1, 0, 0]
    with open(VERSION_FILE, 'r') as f:
        content = f.read().strip()
        match = re.search(r'v(\d+)\.(\d+)\.(\d+)', content)
        if match:
            return [int(match.group(1)), int(match.group(2)), int(match.group(3))]
    return [1, 0, 0]

def write_version(v_list):
    codename = get_fruit_codename(v_list[0], v_list[1])
    v_str = f"v{v_list[0]}.{v_list[1]}.{v_list[2]} '{codename}'"
    with open(VERSION_FILE, 'w') as f:
        f.write(v_str)
    return v_str

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--major', action='store_true')
    parser.add_argument('--minor', action='store_true')
    parser.add_argument('--patch-only', action='store_true')
    args = parser.parse_args()

    v = read_version()
    if args.major:
        v[0] += 1
        v[1] = 0
        v[2] = 0
    elif args.minor:
        v[1] += 1
        v[2] = 0
    else:
        v[2] += 1

    new_v = write_version(v)
    print(f"Bumped version to {new_v}")

if __name__ == '__main__':
    main()
