from setuptools import setup
from os import path
import io
import platform

info = path.abspath(path.dirname(__file__))
with io.open(path.join(info, "requirements.txt"), encoding="utf-8") as file:
    core_require = file.read().split("\n")
    if platform.system == "windows":
        core_require.append("pywin32")

install_require = [x.strip() for x in core_require if "git+" not in x]

setup(
    name="Siskaperbapo",
    version="0.0.1",
    description="Scraping Data from siskaperbapo",
    packages=["Siskaperbapo"],
    install_requires=install_require,
    python_requires=">=3.10",
    license="MIT License",
    classifiers=[
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
)
