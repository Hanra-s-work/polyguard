<!-- 
-- +==== BEGIN polyguard =================+
-- LOGO:
--       input
-- 
--    @#$%!  hello
--      |     |
--      +--+--+
--         |
--         v
--   +------------+
--   | POLY GUARD |
--   +------------+
--     |        |
--     v        v
--  BLOCKED  PASSED
--    KO       OK
-- /STOP
-- PROJECT: polyguard
-- FILE: README.md
-- CREATION DATE: 13-03-2026
-- LAST Modified: 23:53:25 13-03-2026
-- DESCRIPTION:
-- A module that provides a set of swearwords to listen to when filtering while allowing to toggle on and off different languages.
-- /STOP
-- COPYRIGHT: (c) Henry Letellier
-- PURPOSE: The readme file in charge of explaining how to use the module.
-- // AR
-- +==== END polyguard =================+
-->
# polyguard

![PyPI - Python Version](https://img.shields.io/pypi/pyversions/polyguard)
![PyPI - Implementation](https://img.shields.io/pypi/implementation/polyguard)
![PyPI - Wheel](https://img.shields.io/pypi/wheel/polyguard)
![PyPI - Version](https://img.shields.io/pypi/v/polyguard?label=pypi%20package:%20polyguard)
![PyPI - Downloads](https://img.shields.io/pypi/dm/polyguard)
![PyPI - License](https://img.shields.io/pypi/l/polyguard)
![Execution status](https://github.com/Hanra-s-work/polyguard/actions/workflows/python-package.yml/badge.svg)
![GitHub Workflow Status (with event)](https://img.shields.io/github/actions/workflow/status/Hanra-s-work/polyguard/python-package.yml)
![GitHub repo size](https://img.shields.io/github/repo-size/Hanra-s-work/polyguard)
![GitHub Repo stars](https://img.shields.io/github/stars/Hanra-s-work/polyguard)
![GitHub commit activity (branch)](https://img.shields.io/github/commit-activity/m/Hanra-s-work/polyguard)
![GitHub last commit (branch)](https://img.shields.io/github/last-commit/Hanra-s-work/polyguard/main)

[![Static Badge](https://img.shields.io/badge/Buy_me_a_tea-Hanra-%235F7FFF?style=flat-square&logo=buymeacoffee&label=Buy%20me%20a%20coffee&labelColor=%235F7FFF&color=%23FFDD00&link=https%3A%2F%2Fwww.buymeacoffee.com%2Fhanra)](https://www.buymeacoffee.com/hanra)

## Take a look

This project now has automated documentation that gets generated, this manually written one will remain for legacy reasons, but you can now take a look at the automatic documentation here: [https://hanra-s-work.github.io/polyguard/](https://hanra-s-work.github.io/polyguard/)

## Description

## Table of Content

1. [polyguard](#polyguard)
2. [Description](#description)
3. [Table of Content](#table-of-content)
4. [Installation](#installation)
    1. [Using pip](#using-pip)
    2. [Using python](#using-python)
5. [Usage](#usage)
    1. [Running as a script](#running-as-a-script)
    2. [Importing](#importing)
    3. [Initialising](#initialising)
6. [Documentation](#documentation)
7. [Author](#author)

## Installation

### Using pip

```sh
pip install -U polyguard
```

### Using python

Under Windows:

```bat
py -m pip install -U polyguard
```

Under Linux/Mac OS:

```sh
python3 -m pip install -U polyguard
```

## Usage

### Running as a script

You can run polyguard directly as a script to start an interactive terminal session:

```sh
python -m polyguard
```

This will launch the interactive PolyGuard interface where you can execute commands.

### Importing

```py
from polyguard import PolyGuard
```

### Initialising

The generic class is: `PolyGuard(success: int = 0, error: int = 1, log: bool = True, debug: bool = False)`

For your convenience, you can initialize the class with default parameters:

```py
from polyguard import PolyGuard
ERROR = 1
SUCCESS = 0
LOG=True
DEBUG=False

polyguard_instance = PolyGuard(
    SUCCESS,
    ERROR,
    COLOUR_LIB,
    LOG,
    DEBUG
)
polyguard_instance()
```

## Documentation

Comprehensive Doxygen-generated documentation is available online at [https://hanra-s-work.github.io/polyguard/](https://hanra-s-work.github.io/polyguard/). This includes detailed API references, class documentation, and usage examples.

To generate the documentation locally, navigate to the `doxygen_generation` directory and run the provided scripts.

## Author

This module was written by (c) Henry Letellier
Attributions are appreciated.
