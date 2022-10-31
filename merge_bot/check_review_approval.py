import os
from typing import Any, Dict, List

import requests


REVIEW_APPROVED: str = "APPROVED"
GITHUB_TOKEN: str = os.getenv("GITHUB_TOKEN")


def get_reviewer_approvals(repository: str, pull_request_number: str) -> List[bool]:
    """Gets list of reviewer approvals for PR.

    :param repository: repository to get PR from
    :param pull_request_number: PR to get approvals from
    :return: list of reviewer approval statuses for PR
    """
    gh_api_response: requests.Response = requests.get(
        f"https://api.github.com/repos/{repository}/pulls/{pull_request_number}/reviews",
        headers={
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github+json",
        }
    )

    assert gh_api_response.status_code == 200, "Bad response from GitHub reviews API."
    
    response_list: List[Dict] = gh_api_response.json()

    # get latest review status from each reviewer
    # note: reviews are returned in chronological order
    reviews_by_reviewer: Dict[str, str] = {}
    for review in response_list:
        reviews_by_reviewer[review.get("user").get("login")] = review.get("state")

    # return if each reviewer has approved the PR
    review_statuses: List[bool] = []
    for reviewer, status in reviews_by_reviewer.items():
        approved: bool = status == REVIEW_APPROVED
        if not approved:
            print(f"No approval by reviewer: {reviewer}")

        review_statuses.append(approved)

    return review_statuses

if __name__ == "__main__":

    import argparse

    parser: argparse.ArgumentParser = argparse.ArgumentParser(prog="Check reviewer approvals")
    parser.add_argument(
        "--repository",
        help="repository to find reviewer approvals for",
    )
    parser.add_argument(
        "--pull-request-number",
        dest="pull_request_number",
        help="number of pull request to get reviewers for",
    )

    args = parser.parse_args()

    # get reviewer approvals
    reviewer_approvals: List[bool] = get_reviewer_approvals(
        args.repository,
        args.pull_request_number,
    )

    # exit w/ non-zero code if not all reviewers approve
    if not all(reviewer_approvals):
        exit(1)
