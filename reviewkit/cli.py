from __future__ import annotations

import argparse
import subprocess
import sys

from reviewkit import __version__, comment_lint, pr_size


def cmd_size(args: argparse.Namespace) -> int:
    try:
        stats = pr_size.diff_stats(args.base, args.head)
    except subprocess.CalledProcessError as exc:
        print(f"git diff failed: {exc.stderr.strip()}", file=sys.stderr)
        return 2
    size = pr_size.classify(stats)
    print(pr_size.render_markdown(stats, size), end="")
    if args.fail_over and pr_size.SIZES.index(size) >= pr_size.SIZES.index(args.fail_over):
        return 1
    return 0


def cmd_lint_comments(args: argparse.Namespace) -> int:
    report = comment_lint.lint(comment_lint.load_comments(args.comments))
    print(comment_lint.render_report(report), end="")
    if args.strict and report.unlabeled:
        return 1
    return 0


def cmd_summary(args: argparse.Namespace) -> int:
    report = comment_lint.lint(comment_lint.load_comments(args.comments))
    reviews = comment_lint.load_reviews(args.reviews)
    print(comment_lint.render_markdown(report, reviews, args.pr), end="")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="reviewkit",
        description="Code review helpers: PR size, comment labels, and the next step.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    subparsers = parser.add_subparsers(dest="command", required=True)

    size = subparsers.add_parser("size", help="Classify the size of a branch's diff.")
    size.add_argument("--base", required=True, help="Base ref to compare against, e.g. main.")
    size.add_argument("--head", default="HEAD", help="Head ref (default: HEAD).")
    size.add_argument(
        "--fail-over",
        choices=[pr_size.LARGE, pr_size.EXTRA_LARGE],
        help="Exit 1 if the size is this or bigger.",
    )
    size.set_defaults(func=cmd_size)

    lint = subparsers.add_parser("lint-comments", help="Find review comments without a label.")
    lint.add_argument("--comments", required=True, help="JSON from .../pulls/N/comments.")
    lint.add_argument("--strict", action="store_true", help="Exit 1 if any comment is unlabeled.")
    lint.set_defaults(func=cmd_lint_comments)

    summary = subparsers.add_parser("summary", help="Render the review summary comment for a PR.")
    summary.add_argument("--comments", required=True, help="JSON from .../pulls/N/comments.")
    summary.add_argument("--reviews", required=True, help="JSON from .../pulls/N/reviews.")
    summary.add_argument("--pr", required=True, type=int, help="Pull request number.")
    summary.set_defaults(func=cmd_summary)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    return args.func(args)
