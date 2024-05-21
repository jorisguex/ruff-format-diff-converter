"""Entry file to the ruff-format-diff-converter app."""

import argparse
import sys


def main() -> int:
    """Entry function to the ruff-format-diff-converter app."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-i",
        "--input",
        type=argparse.FileType("r"),
        default=sys.stdin,
        help="input file path (defaults to stdin)",
    )
    parser.add_argument(
        "-o",
        "--output",
        type=argparse.FileType("w"),
        default=sys.stdout,
        help="output file path (defaults to stdout)",
    )
    args = parser.parse_args()
    if args.input.isatty():
        sys.stderr.write("Error: Input must not be a TTY.\n")
        sys.exit(1)

    data = args.input.read()
    args.output.write(data)

    return 0
