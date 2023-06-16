from pathlib import Path

from tree_sitter import Language, Parser


def python_parser():
    """
    Build Python parser for the user with tree-sitter.
    """
    parser = Parser()
    CWD = Path(__file__).parent.resolve()
    lang_so = CWD / "tree-sitter-python/build/lang.so"
    Language.build_library(lang_so, [CWD / "tree-sitter-python"])
    py_lang = Language(lang_so, "python")
    parser.set_language(py_lang)
    return parser


def rel_paths(paths, rel, modify=True):
    """
    Return paths that are relative to `rel`.
    Return unmodified paths if `modify` is `False`.
    """
    if not modify:
        return paths

    paths = [str(Path(f).relative_to(rel)) for f in paths]
    return paths


def file_list_rm(file_list: list[str]):
    """
    Remove files given in the list.
    Here mainly due to unwillingness to import pathlib.Path in 'api.py'.
    """
    for file in file_list:
        Path(file).unlink()
