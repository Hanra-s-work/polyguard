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
# FILE: constants.py
# CREATION DATE: 20-03-2026
# LAST Modified: 15:19:51 21-03-2026
# DESCRIPTION:
# A module that provides a set of swearwords to listen to when filtering while allowing to toggle on and off different languages.
# /STOP
# COPYRIGHT: (c) Henry Letellier
# PURPOSE: This is the file containing the constants of the class.
# // AR
# +==== END polyguard =================+
"""

from dataclasses import dataclass
from enum import Enum
from pathlib import Path


# Module paths
# `MODULE_ROOT` points to the package root (the folder containing `src` and `data`).
MODULE_ROOT = Path(__file__).resolve().parent.parent

# Default location for the SQLite database inside the package `data` folder.
# Callers may override this value when constructing `PolyGuard`.
DEFAULT_DB_PATH = MODULE_ROOT / "data" / "polyguard.db"

# Default maximum number of language caches to keep in memory per `PolyGuard`.
# Tuneable: keeps memory bounded while allowing frequent languages to be cached.
DEFAULT_CACHE_MAX_LANGS = 8


@dataclass
class LangConfig:
    """This is the class in charge of allowing the user to configure the languages they which to check for.
    """
    # English variants
    en_uk: bool = True
    en_us: bool = True
    en_au: bool = False

    # Western European
    fr: bool = True
    es: bool = True
    de: bool = True
    it: bool = True
    pt: bool = True  # generic Portuguese (Europeans usually mean pt-PT)
    nl: bool = True

    # Central & Eastern Europe
    pl: bool = False
    ro: bool = False
    hu: bool = False

    # Nordic & other European languages
    sv: bool = False
    da: bool = False
    no: bool = False
    fi: bool = False
    el: bool = False  # Greek

    # Other common regional languages
    tr: bool = False  # Turkish (commonly encountered in parts of Europe)
    ru: bool = False  # Russian (widely understood in some regions)

    # Misc / special flags
    brainrot: bool = False
    other: bool = False


class Langs(Enum):
    EN_UK = "en_uk"
    EN_US = "en_us"
    EN_AU = "en_au"

    FR = "fr"
    ES = "es"
    DE = "de"
    IT = "it"
    PT = "pt"
    NL = "nl"

    PL = "pl"
    RO = "ro"
    HU = "hu"

    SV = "sv"
    DA = "da"
    NO = "no"
    FI = "fi"
    EL = "el"

    TR = "tr"
    RU = "ru"

    BRAINROT = "brainrot"
    OTHER = "other"


# REPL / CLI textual constants
POLY_BOOT_MSG = (
    "polyguard — interactive mode\n"
    "Type 'help' for a short list of commands, 'man' for more details.\n"
    "Enter a word to test it; 'exit' or 'quit' to leave."
)

POLY_HELP_TEXT = (
    "Commands:\n"
    "  help        Short help text (this message)\n"
    "  man         Longer manual describing usage and options\n"
    "  exit, quit  Leave the REPL\n"
    "  db          Show configured DB path\n"
    "  <word>      Check whether <word> is blocked (prints BLOCKED/OK)\n"
)

POLY_MAN_TEXT = (
    "polyguard manual\n\n"
    "This REPL accepts single-word queries and returns whether the word\n"
    "is considered a swearword according to the configured language lists.\n\n"
    "If started with --db-path, that DB will be used; otherwise the package\n"
    "default DB is used. You can also pipe words via stdin for batch checks.\n"
)

POLY_PROMPT = "polyguard> "
STATUS_BLOCKED = "BLOCKED"
STATUS_OK = "OK"
DB_PATH_FMT = f"DB path: {DEFAULT_DB_PATH}"
