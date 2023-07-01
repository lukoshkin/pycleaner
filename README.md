# PyCleaner

**PyCleaner** is a simple Python library that helps you to keep the repository
clean by finding all redundant py-files there. It is especially helpful when
you incorporate someone else's repositories, your project is growing huge, and
at some point, you need to get rid of the Python scripts you don't use.

**PyCleaner** scans the project folder for dependencies of the core project
files (_targets_). After exploring the project directory, it provides stats
about modules directly or indirectly imported in the target files. These
modules are referred to (in the context of this package) as _libraries_. The
rest files whose names were not found during recursive search of the import
statements of the core files are named _scripts_. While the removal of scripts
is possible by design, a user should prefer manual deletion after more thorough
inspection.


## Usage

Install with pip
```bash
pip install cleaner-project
```

Get stats about the core file dependencies
```bash
pycleaner --project <proj_dir> --target <dir_w/_project_core_files>
```

A toy example:
```bash
pycleaner -t folder1,folder2,path/to/file.py
# To delete empty folders if any appeared, use:
find . -type d -empty -delete
```

The target files here are py-files anywhere within `folder1` and `folder2` and
`path/to/file.py`. Note that the project directory if not specified, and thus,
is the current one by default. A user should specify target files and folders
relative to the project directory since it is assumed that they reside in the
project folder.

Learn more about `pycleaner`'s options
```bash
pycleaner --help
```
