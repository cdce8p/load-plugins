# ---------------------------------------------------------------------------
# Licensed under the MIT License. See LICENSE file for license information.
# ---------------------------------------------------------------------------
# Cmdclass structure to install the .pth file
# taken from pytest-cov licensed under the MIT license.
# https://github.com/pytest-dev/pytest-cov/blob/v3.0.0/setup.py
# https://github.com/pytest-dev/pytest-cov/blob/v3.0.0/LICENSE
# ---------------------------------------------------------------------------

from itertools import chain
from pathlib import Path

from setuptools import setup
from setuptools.command.build_py import build_py
from setuptools.command.develop import develop
from setuptools.command.install_lib import install_lib

PTH_FILE_PATH = "src/load_plugins.pth"


class BuildPyWithPth(build_py):
    def run(self, *args, **kwargs):
        super().run(*args, **kwargs)
        path = Path(__file__).parent.joinpath(PTH_FILE_PATH)
        dest = Path(self.build_lib, path.name)
        self.copy_file(path, dest)


class DevelopWithPth(develop):
    def run(self, *args, **kwargs):
        super().run(*args, **kwargs)
        path = Path(__file__).parent.joinpath(PTH_FILE_PATH)
        dest = Path(self.install_dir, path.name)
        self.copy_file(path, dest)


class InstallLibWithPth(install_lib):
    def run(self, *args, **kwargs):
        super().run(*args, **kwargs)
        path = Path(__file__).parent.joinpath(PTH_FILE_PATH)
        dest = Path(self.install_dir, path.name)
        self.copy_file(path, dest)
        self.outputs = [dest]

    def get_outputs(self):
        return chain(super().get_outputs(), self.outputs)


setup(
    cmdclass={
        "build_py": BuildPyWithPth,
        "develop": DevelopWithPth,
        "install_lib": InstallLibWithPth,
    }
)
