#!/usr/bin/env python3
"""
Simple CLI to check primes.
Usage:
  - Provide numbers as command-line arguments:
      python3 backend/is_prime_cli.py 17 18 19
  - Or pipe numbers (space/newline separated) via stdin:
      echo "17 18 19" | python3 backend/is_prime_cli.py

Prints each number and whether it's prime.
"""
import sys
import math


def is_prime(n: int) -> bool:
    if n <= 1:
        return False
    if n <= 3:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def parse_input(args):
    """Return a list of integers from args or stdin."""
    nums = []
    if len(args) > 1:
        # args[1:] are numbers
        for a in args[1:]:
            for part in a.replace(',', ' ').split():
                try:
                    nums.append(int(part))
                except ValueError:
                    pass
    else:
        # read from stdin
        data = sys.stdin.read().strip()
        for part in data.replace(',', ' ').split():
            try:
                nums.append(int(part))
            except ValueError:
                pass
    return nums


def main():
    nums = parse_input(sys.argv)
    if not nums:
        print("No integers provided. Give numbers as args or via stdin.")
        return
    for n in nums:
        print(f"{n}: {'prime' if is_prime(n) else 'not prime'}")


if __name__ == '__main__':
    main()
