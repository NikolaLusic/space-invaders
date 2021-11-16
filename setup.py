import os
from functools import reduce

from setuptools import find_packages, setup
from setuptools.command.install import install


class PostInstall(install):
    def __init__(self, *args, **kwargs):
        super(PostInstall, self).__init__(*args, **kwargs)
        _install_requirements()


def _install_requirements():
    os.system("pre-commit install")
    os.system("pip install -r requirements")


REQUIRED_PACKAGES = ["pydantic >= 1.8.2", "python-dotenv >= 0.19.1", "numpy == 1.21.4"]


TEST_PACKAGES = [
    "pytest == 6.2.5",
    "coverage == 5.3",
    "black == 21.7b0",
]


EXTRA_REQUIREMENTS = {"test": TEST_PACKAGES}

name = "space_invaders"
version = "0.1.0"
description = "API used for managing housing units."


setup(
    name=name,
    version=version,
    description=description,
    packages=find_packages(
        where="src",
        include=["space_invaders*"],
    ),
    package_dir={"": "src"},
    python_requires=">= 3.9",
    include_package_data=True,
    install_requires=REQUIRED_PACKAGES,
    extras_require={
        **EXTRA_REQUIREMENTS,
        "all": reduce(lambda agg, value: agg + value, EXTRA_REQUIREMENTS.values(), []),
    },
    cmdclass={"install": PostInstall},
)
