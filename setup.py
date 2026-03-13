""" 
# +==== BEGIN polyguard =================+
# LOGO:
#       input
# 
#    @#$%!  hello
#      |     |
#      +--+--+
#         |
#         v
#   +------------+
#   | POLY GUARD |
#   +------------+
#     |        |
#     v        v
#  BLOCKED  PASSED
#    KO       OK
# /STOP
# PROJECT: polyguard
# FILE: setup.py
# CREATION DATE: 13-03-2026
# LAST Modified: 10:58:49 13-03-2026
# DESCRIPTION:
# A module that provides a set of swearwords to listen to when filtering while allowing to toggle on and off different languages.
# /STOP
# COPYRIGHT: (c) Henry Letellier
# PURPOSE: File containing the required information to successfully build a python package
# // AR
# +==== END polyguard =================+
"""


import setuptools

with open("README.md", "r", encoding="utf-8", newline="\n") as fh:
    long_description = fh.read()

setuptools.setup(
    name='polyguard',
    version='1.0.0',
    packages=setuptools.find_packages(),
    install_requires=[],
    author="Henry Letellier",
    author_email="henrysoftwarehouse@protonmail.com",
    description="A module that provides a set of swearwords to listen to when filtering while allowing to toggle on and off different languages.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Hanra-s-work/polyguard",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 5 - Production/Stable",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
