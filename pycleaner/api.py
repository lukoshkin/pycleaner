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
            "Project core files. The files or/and directories with the core"
            " files should reside within the project directory ('--project')."
            " Multiple targets should separated by a comma."
        ),
    )
    parser.add_argument(
        "--deep",
        action="store_true",
        default=False,
        help="Search all imports, even indented",
    )
    parser.add_argument(
        "--abs-path",
        action="store_true",
        default=False,
        help="Instead of relative paths show absolute",
    )
    parser.add_argument(
        "--log",
        action="store_true",
        default=False,
        help=(
            "Log scripts to pycleaner-scripts.log and libs to"
            " pycleaner-libs.log. Log-files are created in the current folder."
        ),
    )
    parser.add_argument(
        "-z",
        "--zip-lib",
        dest="zip",
        default=None,
        help="Zip dependencies for further migration",
    )
    parser.add_argument(
        "--rm-scripts",
        action="store_true",
        dest="rm",
        default=False,
        help="Remove all scripts",
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
    if args.rm and args.zip is not None:
        raise ValueError(
            "It is not supposed --rm-scripts and --zip-lib"
            " options are used simultaneously"
        )
    parser = utils.python_parser()
    sorter = lib_script_split.PyProjectDeps(
        parser,
        project_dir=args.project,
        target_files=args.target.split(","),
        deep_walk=args.deep,
    )
    cli = cmd.Cmd()
    try:
        width = os.get_terminal_size().columns
    except OSError:
        width = 120
        ## Falling back to 120 in case
        ## a user redirects stdout to a file.

    libs, scripts = sorter.recursive_call()
    if not any([args.libs, args.scripts, args.not_found, args.may_found]):
        args.libs = args.scripts = args.not_found = args.may_found = True

    def block(files, header, show=False):
        if show:
            print(header.upper())
            cli.columnize(files, width)
            print()

    rel = None if args.abs_path else sorter.cwd
    block(utils.rel_paths(libs, rel), "libraries", args.libs)
    block(utils.rel_paths(scripts, rel), "scripts", args.scripts)
    block(
        utils.may_found_dict_to_list(sorter.may_found, rel),
        "might be found",
        args.may_found,
    )
    block(
        utils.not_found_dict_to_list(sorter.not_found, rel),
        "not found",
        args.not_found,
    )
    print(
        f"There are {len(libs)} files that can be considered as libraries,"
        f" and {len(scripts)} ─ as scripts"
    )
    if args.log:
        log_files = utils.rel_paths(libs, rel)
        utils.file_list_log(log_files, "pycleaner-libs.log")
        log_files = utils.rel_paths(scripts, rel)
        utils.file_list_log(log_files, "pycleaner-scripts.log")
    if args.zip is not None:
        utils.file_list_zip(libs, args.zip)
    if args.rm:
        if _user_permits(
            "Are you sure you want to proceed with removal of all the scripts?"
        ):
            utils.file_list_rm(scripts)


if __name__ == "__main__":
    api_call()
