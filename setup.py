"""Setup module installation."""

import os
import re

from setuptools import setup


def load_requirements(path: str) -> list:
    """Load requirements from the given relative path."""
    with open(path, encoding="utf-8") as file:
        requirements = []
        for line in file.read().split("\n"):
            if line.startswith("-r"):
                dirname = os.path.dirname(path)
                filename = line.split(maxsplit=1)[1]
                requirements.extend(load_requirements(os.path.join(dirname, filename)))
            elif line and not line.startswith("#"):
                requirements.append(line.replace("==", ">="))
        return requirements


if __name__ == "__main__":
    MODULE_NAME = "simplebot_translator"
    DESC = "🌎 Translator plugin for SimpleBot"

    with open(MODULE_NAME + ".py") as fh:
        version = re.search(r"__version__ = \"(.*?)\"", fh.read(), re.M).group(1)

    with open("README.rst") as fh:
        long_description = fh.read()
    with open("CHANGELOG.rst") as fh:
        long_description += "\n" + fh.read()

    setup(
        name=MODULE_NAME,
        version=version,
        description=DESC,
        long_description=long_description,
        long_description_content_type="text/x-rst",
        author="The SimpleBot Contributors",
        author_email="adbenitez@nauta.cu",
        url="https://github.com/simplebot-org/simplebot_translator",
        keywords="simplebot plugin deltachat",
        license="MPL",
        classifiers=[
            "Development Status :: 4 - Beta",
            "Environment :: Plugins",
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: Mozilla Public License 2.0 (MPL 2.0)",
            "Operating System :: OS Independent",
            "Topic :: Utilities",
        ],
        zip_safe=False,
        include_package_data=True,
        py_modules=[MODULE_NAME],
        install_requires=load_requirements("requirements/requirements.txt"),
        extras_require={
            "test": load_requirements("requirements/requirements-test.txt"),
            "dev": load_requirements("requirements/requirements-dev.txt"),
        },
        entry_points={
            "simplebot.plugins": "{0} = {0}".format(MODULE_NAME),
        },
    )
