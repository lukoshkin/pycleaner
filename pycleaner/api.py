"""
This script is an easier interface to 'lib_script_split.py' functionality.
"""
import argparse
import cmd
import os

from . import lib_script_split, utils


def _parsed_args():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--project",
        default=".",
        help="The directory of a project to check",
    )
    parser.add_argument(
        "-t",
        "--target",
        default="core",
        help=(
            "Project core files. The file or directory with the core files"
            " should reside within the project directory ('--project')"
        ),
    )
    parser.add_argument(
        "--rm-scripts",
        action="store_true",
        dest="rm",
        default=False,
        help="Remove all scripts",
    )
    parser.add_argument(
        "--abs-path",
        action="store_true",
        default=False,
        help="Instead of relative paths show absolute",
    )
    parser.add_argument(
        "-1",
        "--libs",
        action="store_true",
        default=False,
        help="Show stats about found libraries",
    )
    parser.add_argument(
        "-2",
        "--scripts",
        action="store_true",
        default=False,
        help="Show stats about found scripts",
    )
    parser.add_argument(
        "-3",
        "--not-found",
        action="store_true",
        default=False,
        help="Show stats about not found modules",
    )
    parser.add_argument(
        "-4",
        "--may-found",
        action="store_true",
        default=False,
        help="Show stats about modules that might be found manually",
    )
    args = parser.parse_args()
    return args


def _user_permits(question: str):
    user_input = input(f"{question} [yN] ").lower()
    if user_input == "y":
        return True
    return False


def api_call():
    """
    Command Line Interface for scanning a Python project and finding out what
    py-files are libraries w.r.t. the core files of the project and what are
    just scripts (either ancillary files in the project or redundant).
    """
    args = _parsed_args()
    rel = not args.abs_path
    parser = utils.python_parser()
    sorter = lib_script_split.PyProjectDeps(
        parser,
        project_dir=args.project,
        target_files=args.target,
    )
    cli = cmd.Cmd()
    width = os.get_terminal_size().columns
    libs, scripts = sorter.recursive_call()

    if not any([args.libs, args.scripts, args.not_found, args.may_found]):
        args.libs = args.scripts = args.not_found = args.may_found = True

    def block(file_list, header, show=False):
        if show:
            print(header.upper())
            cli.columnize(file_list, width)
            print()

    block(utils.rel_paths(libs, sorter.cwd, rel), "libraries", args.libs)
    block(utils.rel_paths(scripts, sorter.cwd, rel), "scripts", args.scripts)
    block(sorter.may_found, "might be found", args.may_found)
    block(sorter.not_found, "not found", args.not_found)
    print(
        f"There are {len(libs)} files that can be considered as libraries,"
        f" and {len(scripts)} ─ as scripts"
    )
    if args.rm:
        if _user_permits(
            "Are you sure you want to proceed with removal of all the scripts?"
        ):
            utils.file_list_rm(scripts)


if __name__ == "__main__":
    api_call()
