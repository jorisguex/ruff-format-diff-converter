"""Entry file to the ruff-format-diff-converter app."""

import argparse
import sys

import junit_xml
import whatthepatch


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

    test_cases = []
    for diff in whatthepatch.parse_patch(data):
        test_case = junit_xml.TestCase(name=diff.header.old_path)
        changes = "\n\n"
        for change in diff.changes:
            if change.old is None:
                changes += f"New Line {change.new}: '{change.line}'\n"
            if change.new is None:
                changes += f"Old Line {change.old}: '{change.line}'\n"

        changes += "\n"
        test_case.add_failure_info("file would be reformatted", changes, "formatting")
        test_cases.append(test_case)

    test_suite = junit_xml.TestSuite("Ruff Formatting", test_cases)
    junit_xml.TestSuite.to_file(args.output, [test_suite])

    return 0
