# PyCleaner

**PyCleaner** is a simple Python library that helps you to keep the repository
clean by finding all redundant py-files there. It is especially helpful when
you incorporate someone else's repositories, your project is growing huge, and
at some point, you need to get rid of the Python scripts you don't use.

**PyCleaner** scans the project folder for dependencies of the core project
files (_target_). After exploring the project directory, it provides stats
about modules directly or indirectly imported in the target files. These
modules are referred to (in the context of this package) as _libraries_. The
rest files whose names were not found during recursive search of the import
statements of the core files are named _scripts_. While the removal of scripts
is possible by design, a user should prefer manual deletion after more thorough
inspection.


## Usage

Install with pip
```bash
pip install pycleaner
```

Get stats about the core file dependencies
```bash
pycleaner --project <proj_dir> --target <dir_w/_project_core_files>
```

Remove those files on which the core file do not depend
```bash
pycleaner --project <proj_dir> --target <dir_w/_project_core_files> --rm-scripts
```

Learn more about `pycleaner`'s options
```bash
pycleaner --help
```
