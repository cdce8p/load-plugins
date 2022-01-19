# Load-plugins

Dynamically load plugin packages based on `pyproject.toml` config.
Only recommend to use for applications that use a plugin
structure internally but don't officially support custom plugins.

## How does it work?

The library installs a `.pth` file into the `site-packages` directory.
This is executed for every Python program call.

The `.pth` file itself will load a Python module which reads the `pyproject.toml`
file to determine which packages to import. For each package, it will
import all individual modules separately. Thus, it's not necessary to
import them inside the package `__init__.py` file.

All that happens **before** the actual Python program is executed.

## Disclaimer

This library **will** slow down the startup of any Python program.
It is recommended to only use it in isolated environments!
E.g. together with `pre-commit`.

## Configuration and Usage

To configure the library, add a `pyproject.toml` file to the root of your project.

There are two different options, which can be used together.
1. Packages which should **always** be loaded
```toml
[tool.load_plugins]
packages = [
    "plugin_package",
    "folder.with_package",
]
```
2. And packages which should only be loaded for certain applications.
The name of the binary is used as filter.
E.g. for a Python application with entry point `app`, use this config.
```toml
[tool.load_plugins.app]
packages = [
    "plugin_package",
]
```

If used with `pre-commit`, remember to add `load-plugins` as `additional_dependencies`.

## License
This Project is licensed under the MIT license.
See [LICENSE][LICENSE_FILE] for the full license text.

[LICENSE_FILE]: https://github.com/cdce8p/load-plugins/blob/main/LICENSE
