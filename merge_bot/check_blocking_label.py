import json
from typing import List


if __name__ == "__main__":

    import argparse

    parser: argparse.ArgumentParser = argparse.ArgumentParser(prog="Check for blocking label")
    parser.add_argument(
        "--blocking-label",
        dest="blocking_label",
        help="name of label that is blocking",
    )
    parser.add_argument(
        "--labels",
        type=str,
        help="list of labels for PR, as comma delimited string",
    )

    args = parser.parse_args()

    labels: List[str] = args.labels.split(",")

    if args.blocking_label in labels:
        exit(1)
