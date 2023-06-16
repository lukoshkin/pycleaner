import subprocess
from pathlib import Path

from setuptools import setup
from setuptools.command.install import install

NAME = "pycleaner"
PIP_ALLOWED_NAME = "cleaner-project"
## Unfortunately, pip doesn't allow to upload under the name "pycleaner".


def long_description():
    readme = Path(__file__).parent / "README.md"
    with open(readme, encoding="utf-8") as fd:
        return "\n" + fd.read()


class CustomInstall(install):
    def run(self):
        ## git is required
        subprocess.call(
            [
                "git",
                "clone",
                "https://github.com/tree-sitter/tree-sitter-python",
            ]
        )
        src = Path(__file__).parent.resolve() / "tree-sitter-python"
        dst = f"{self.install_lib}/{NAME}/tree-sitter-python"
        ## maybe, there is `shutil`'s `copytree` under the hood
        self.copy_tree(str(src), str(dst))
        ## I could also have used `shutil` for `src` removal,
        ## but I don't want to import it just for this purpose.
        subprocess.call(["rm", "-rf", str(src)])
        ## -f is required since some of .git files are write-protected.
        super().run()


setup(
    name=PIP_ALLOWED_NAME,
    version="1.0.1",
    author="lukoshkin",
    author_email="lukoshkin.workspace@gmail.com",
    description=(
        "Partitions the project w.r.t. its core files to libraries and scripts"
        " (that is, those files that do not directly relate to the project"
        " core files). The latter can be removed with a dedicated API call and"
        " its options."
    ),
    license="MIT",
    long_description=long_description(),
    long_description_content_type="text/markdown",
    packages=[NAME],
    entry_points={
        "console_scripts": [
            ## pyclean is occupied on PyPI already.
            f"{NAME} = {NAME}.api:api_call",
        ],
    },
    install_requires=["tree-sitter"],
    cmdclass={"install": CustomInstall},
)
