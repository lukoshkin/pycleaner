"""
Utility functions.
"""
import zipfile
from pathlib import Path
from typing import Any

from tree_sitter import Language, Parser


def python_parser() -> Parser:
    """
    Build Python parser for the user with tree-sitter.
    """
    parser = Parser()
    cwd = Path(__file__).parent.resolve()
    # lang_so = cwd / "tree-sitter-python/build/lang.so"
    # Language.build_library(lang_so, [cwd / "tree-sitter-python"])
    ## For compatibility with old versions, use f-strings instead.
    lang_so = f"{cwd}/tree-sitter-python/build/lang.so"
    Language.build_library(lang_so, [f"{cwd}/tree-sitter-python"])
    py_lang = Language(lang_so, "python")
    parser.set_language(py_lang)
    return parser


def rel_paths(paths: str | list[str], rel: str | Path = None) -> list[str]:
    """
    Return paths that are relative to `rel`.
    Return unmodified paths if `rel` is None.
    Note that `rel` should be given as abs path.
    """
    if rel is None:
        return paths

    if isinstance(paths, str):
        paths = [paths]

    paths = [str(Path(f).relative_to(rel)) for f in paths]
    return paths


def file_list_log(file_list: list[str], logfile: str):
    """
    Save file names to `logfile`.
    """
    with open(logfile, "w") as fd:
        for file in file_list:
            fd.write(f"{file}\n")


def file_list_rm(file_list: list[str]):
    """
    Remove files given in the list.
    Here mainly due to unwillingness to import pathlib.Path in 'api.py'.
    """
    for file in file_list:
        Path(file).unlink()


def file_list_zip(file_list: list[str], zipname: str):
    """
    Zip files for further migration.
    """
    with zipfile.ZipFile(zipname, "w", zipfile.ZIP_DEFLATED) as zip_ref:
        for file in file_list:
            zip_ref.write(file)


def not_found_dict_to_list(
    files: dict[str, list[str]], rel: str | Path = None
) -> list[str]:
    """
    Convert `files` dict of "module - list of files" pairs into a flattened
    list of strings of the form "module from a file".

    To apply `rel_paths` function to the dict values, one must pass absolute
    path `rel` relative to which the files in lists should be considered.
    """
    new_files = []
    for key, files in files.items():
        files = rel_paths(files, rel)
        new_files.extend([f"{key} FROM {v}" for v in files])

    return new_files


def may_found_dict_to_list(
    files: dict[str, list[str]], rel: str | Path = None
) -> list[str]:
    """
    Convert `files` dict of "module - list of files" pairs into a flattened
    list of strings of the form "module from a file".

    To apply `rel_paths` function to the dict values, one must pass absolute
    path `rel` relative to which the files in lists should be considered.
    """
    new_files = []
    for key, files in files.items():
        key = f"{key[0]} FROM {rel_paths(key[1], rel)[0]}"
        files = ", ".join(rel_paths(files, rel))
        new_files.extend([f"{key} IS ONE OF {files}"])

    return new_files


def largest_common_prefix(strings: list[str]) -> str:
    """
    Find the largest common prefix in the `strings` list.
    """
    path_iter = iter(strings)
    res = next(path_iter)

    for path in path_iter:
        while not path.startswith(res):
            res = res[:-1]
            if len(res) == 0:
                return ""

    return res


def contains_prefix(strings: list[str]) -> bool:
    """
    Check if there is a string in the list that is the prefix
    of another string from the list.
    """
    lcp = largest_common_prefix(strings)
    strings = iter(sorted([x.removeprefix(lcp) for x in strings]))
    prev_val = next(strings)

    for val in strings:
        if val.startswith(prev_val):
            return True

        prev_val = val

    return False


def is_sublist(small: list[Any], big: list[Any]) -> bool:
    """
    Check whether `big` contains `small`
    """
    if len(small) > len(big):
        return False

    if len(small) == 0:
        return True

    start = 0
    for start, big_el in enumerate(big):
        if start > len(big) - len(small):
            return False

        if big_el == small[0]:
            break
    else:
        return False

    for i in range(1, len(small)):
        if small[i] != big[i + start]:
            return False

    return True
