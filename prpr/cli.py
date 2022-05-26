import argparse
import datetime as dt

from prpr.download import DownloadMode
from prpr.filters import FilterMode

DOWNLOAD = "--download"
POST_PROCESS = "--post-process"
INTERACTIVE = "--interactive"


def configure_arg_parser():
    arg_parser = argparse.ArgumentParser(formatter_class=argparse.RawTextHelpFormatter)
    filters = arg_parser.add_argument_group(
        "filters",
        "these allow to specify the subset of homeworks to be displayed, can be composed",
    )
    configure_filter_arguments(filters)

    arg_parser.add_argument("-o", "--open", action="store_true", default=False, help="open homework pages in browser")

    download_options = arg_parser.add_argument_group(
        "download",
    )
    configure_download_arguments(download_options)

    arg_parser.add_argument(
        "-v",
        "--verbose",
        action="count",
        default=0,
    )
    process_options = arg_parser.add_argument_group("process")
    configure_process_arguments(process_options)
    return arg_parser


def configure_filter_arguments(filters):
    filters.add_argument(
        "-m",
        "--mode",
        type=FilterMode.from_string,
        choices=list(FilterMode),
        default=FilterMode.STANDARD,
        help="""filter mode
            standard: in review, open or on the side of user
            open: in review or open
            closed: resolved or closed
            closed-this-month: resolved or closed this "month" aka 💰.
            closed-previous-month: resolved or closed previous "month" aka 💰.
            all: all, duh""",
    )
    filters.add_argument(
        "-p",
        "--problems",
        type=int,
        nargs="+",
        help="the numbers of problems to be shown; multiple space-separated values are accepted",
    )
    filters.add_argument(
        "-n",
        "--no",
        type=int,
        help="the no of the homework to be shown, all other filters are ignored",
    )
    filters.add_argument(
        "-s",
        "--student",
        help="the substring to be found in the student column, mail works best",
    )
    filters.add_argument(
        "-c",
        "--cohorts",
        nargs="+",
        help="cohorts to be shown; multiple space-separated values are accepted",
    )
    filters.add_argument(
        "-f",
        "--from-date",
        help="the start date (YYYY-MM-DD)",
        type=dt.date.fromisoformat,
    )
    filters.add_argument(
        "-t",
        "--to-date",
        help="the end date (YYYY-MM-DD)",
        type=dt.date.fromisoformat,
    )
    filters.add_argument(
        "-u",
        "--user",
        default=None,
        type=str,
        help="Search USER's tickets instead of my (USER - name in tracker)",
    )
    filters.add_argument(
        "--free",
        action="store_true",
        help="show unassigned (free) tickets (overrides -u/--user)",
    )


def configure_download_arguments(download_options):
    download_options.add_argument(
        "-d",
        DOWNLOAD,  # TODO: Add help messages when we have all the options we want
        # action="store_true",
        nargs="?",
        type=DownloadMode.from_string,
        choices=list(DownloadMode),
        const=DownloadMode.ONE,
        help="""download mode
            one: first by deadline,
            all: all, duh
            interactive: choose one interactively,
            interactive-all: choose one interactively, repeat
            """,
    )
    download_options.add_argument(
        "--head",
        help="download with visible browser window (default is headless, i.e. the window is hidden)",
        action="store_true",
        default=False,
    )
    download_options.add_argument(
        "-i",
        INTERACTIVE,
        help="choose which homework to download interactively (deprecated)",
        action="store_true",
        default=False,
    )


def configure_process_arguments(process_options):
    process_options.add_argument(
        POST_PROCESS,
        action="store_true",
        default=False,
    )
