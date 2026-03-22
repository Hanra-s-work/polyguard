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
-- LAST Modified: 3:48:28 22-03-2026
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

To initialize PolyGuard, you need to create a language configuration and pass it to the constructor:

```py
from polyguard.src.polyguard import PolyGuard
from polyguard.src.constants import LangConfig

# Create a language configuration (enable desired languages)
lang_config = LangConfig()
# By default, all supported languages are enabled

# Initialize PolyGuard with optional parameters
polyguard_instance = PolyGuard(
    langs=lang_config,
    db_path=None,  # Uses default package database if None
    success=0,     # Exit code for success
    error=1,       # Exit code for error
    log=True,      # Enable logging
    debug=False    # Enable debug-level logging
)
```

### Usage Examples

Once initialized, you can use the following methods:

```py
# Check if a word is profanity (returns bool)
if polyguard_instance.is_a_swearword("hello world"):
    print("Contains profanity")
else:
    print("Clean text")

# Extract the first matching swearword (returns Optional[str])
offending_word = polyguard_instance.extract_swearword_if_present("some bad word here")
if offending_word:
    print(f"Found profanity: {offending_word}")

# Get all swearwords for enabled languages (returns Dict[str, Set])
all_words = polyguard_instance.get_list_of_swearwords()
for language, words in all_words.items():
    print(f"{language}: {len(words)} words")
```

**Note:** The database initialization happens automatically on the first call to any lookup function, so you don't need to call `main()` manually.

### Per-Call Language Configuration

All lookup functions accept an optional `languages_to_check` parameter, allowing you to override the default language configuration on a case-by-case basis:

```py
from polyguard import LangConfig

# Create a custom language config for this specific check
custom_langs = LangConfig()
custom_langs.en = True   # Only check English
custom_langs.fr = False  # Don't check French
custom_langs.de = False  # Don't check German
# ... set other languages as needed

# Use the custom config for this lookup only
if polyguard_instance.is_a_swearword("hello world", languages_to_check=custom_langs):
    print("Contains profanity in enabled languages")

# Extract swearword with custom language set
word = polyguard_instance.extract_swearword_if_present(
    "bonjour monde", 
    languages_to_check=custom_langs
)

# Get swearwords for custom language subset
words = polyguard_instance.get_list_of_swearwords(languages=custom_langs)
```

This is useful when you need to:

- Check text against only specific languages
- Perform different validations for different contexts
- Optimize performance by limiting language checks to what's needed

If `languages_to_check`/`languages` is not provided, the instance's default configuration (set during initialization) is used.

## Documentation

Comprehensive Doxygen-generated documentation is available online at [https://hanra-s-work.github.io/polyguard/](https://hanra-s-work.github.io/polyguard/). This includes detailed API references, class documentation, and usage examples.

To generate the documentation locally, navigate to the `doxygen_generation` directory and run the provided scripts.

## Author

This module was written by (c) Henry Letellier
Attributions are appreciated.
