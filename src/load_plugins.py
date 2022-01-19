# ---------------------------------------------------------------------------
# Licensed under the MIT License. See LICENSE file for license information.
# ---------------------------------------------------------------------------
import importlib
import os
import pkgutil
import sys
from contextlib import contextmanager
from pathlib import Path

import tomli


@contextmanager
def patch_path(config_path):
    """Add main project folder to sys.path.
    Allows local modules being loaded without them being installed.
    """
    original_path = sys.path
    sys.path.append(str(config_path.parent.absolute()))
    yield
    sys.path = original_path


def activate():
    """Read pyproject.toml and load all modules from packages found in
    the tool.load_plugins.packages or tool.load_plugins.<arg_0>.packages section.
    """
    path = Path("pyproject.toml")
    if not path.is_file():
        return

    with open(path, "rb") as f:
        toml_dict = tomli.load(f)

    arg_0 = sys.argv[0].rpartition(os.path.sep)[2]

    config = toml_dict.get("tool", {}).get("load_plugins", {})
    conf_packages = [
        *config.get("packages", ()),
        *config.get(arg_0, {}).get("packages", ()),
    ]

    if conf_packages:
        with patch_path(path):
            for pkg_name in conf_packages:
                pkg = importlib.import_module(pkg_name)
                for mod_info in pkgutil.walk_packages(pkg.__path__, f"{pkg.__name__}."):
                    importlib.import_module(mod_info.name)


activate()
