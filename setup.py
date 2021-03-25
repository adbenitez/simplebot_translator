"""Setup module installation."""

import re

from setuptools import setup

if __name__ == "__main__":
    MODULE_NAME = "simplebot_translator"
    DESC = "🌎 Translator plugin for SimpleBot"

    with open(MODULE_NAME + ".py") as fh:
        version = re.search(r"__version__ = \"(.*?)\"", fh.read(), re.M).group(1)

    with open("README.rst") as fh:
        long_description = fh.read()
    with open("CHANGELOG.rst") as fh:
        long_description += "\n" + fh.read()

    with open("requirements.txt", encoding="utf-8") as req:
        install_requires = [
            line.replace("==", ">=")
            for line in req.read().split("\n")
            if line and not line.startswith(("#", "-"))
        ]
    with open("requirements-test.txt", encoding="utf-8") as req:
        test_deps = [
            line.replace("==", ">=")
            for line in req.read().split("\n")
            if line and not line.startswith(("#", "-"))
        ]

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
        install_requires=install_requires,
        extras_require={"test": test_deps},
        entry_points={
            "simplebot.plugins": "{0} = {0}".format(MODULE_NAME),
        },
    )
