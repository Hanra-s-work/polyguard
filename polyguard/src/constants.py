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
# LAST Modified: 18:39:49 21-03-2026
# DESCRIPTION:
# A module that provides a set of swearwords to listen to when filtering while allowing to toggle on and off different languages.
# /STOP
# COPYRIGHT: (c) Henry Letellier
# PURPOSE: This is the file containing the constants of the class.
# // AR
# +==== END polyguard =================+
"""

from enum import Enum
from pathlib import Path
from dataclasses import dataclass


# Module paths
# `MODULE_ROOT` points to the package root (the folder containing `src` and `data`).
MODULE_ROOT = Path(__file__).resolve().parent.parent

# Default location for the SQLite database inside the package `data` folder.
# Callers may override this value when constructing `PolyGuard`.
DEFAULT_DB_PATH = MODULE_ROOT / "data" / "polyguard.db"

DEFAULT_SOURCE_WORDS = MODULE_ROOT.parent / "wordlists"

# Default maximum number of language caches to keep in memory per `PolyGuard`.
# Tuneable: keeps memory bounded while allowing frequent languages to be cached.
DEFAULT_CACHE_MAX_LANGS = 8


@dataclass
class LangConfig:
    """This is the class in charge of allowing the user to configure the languages they which to check for.
    """
    # English variants
    en: bool = True
    en_uk: bool = False
    en_us: bool = False
    en_au: bool = False

    # Western European
    fr: bool = True
    fr_ca: bool = False
    es: bool = True
    es_es: bool = False
    es_mx: bool = False
    es_ar: bool = False
    de: bool = True
    de_at: bool = False
    de_ch: bool = False
    de_de: bool = False
    it: bool = True
    it_ch: bool = False
    it_it: bool = False
    pt: bool = True  # generic Portuguese (Europeans usually mean pt-PT)
    pt_pt: bool = False
    pt_br: bool = False
    pt_ao: bool = False
    nl: bool = True
    nl_nl: bool = False
    nl_be: bool = False
    nl_sr: bool = False

    # Central & Eastern Europe
    pl: bool = False
    pl_pl: bool = False
    pl_ua: bool = False
    pl_lt: bool = False
    ro: bool = False
    ro_ro: bool = False
    ro_md: bool = False
    ro_rs: bool = False
    hu: bool = False
    hu_hu: bool = False
    hu_at: bool = False
    hu_sk: bool = False
    hu_rs: bool = False

    # Nordic & other European languages
    sv: bool = False
    sv_se: bool = False
    sv_fi: bool = False
    sv_no: bool = False
    sv_dk: bool = False
    da: bool = False
    da_dk: bool = False
    da_se: bool = False
    da_no: bool = False
    da_gl: bool = False
    no: bool = False
    no_no: bool = False
    no_se: bool = False
    no_dk: bool = False
    no_sa: bool = False
    fi: bool = False
    fi_fi: bool = False
    fi_se: bool = False
    fi_ru: bool = False
    fi_ee: bool = False
    el: bool = False  # Greek
    el_gr: bool = False
    el_cy: bool = False
    el_tr: bool = False
    el_it: bool = False
    el_al: bool = False

    # Other common regional languages
    tr: bool = False  # Turkish (commonly encountered in parts of Europe)
    tr_tr: bool = False
    tr_cy: bool = False
    tr_bg: bool = False
    tr_gr: bool = False
    tr_mk: bool = False
    ru: bool = False  # Russian (widely understood in some regions)
    ru_ru: bool = False
    ru_by: bool = False
    ru_kz: bool = False
    ru_ua: bool = False
    ru_md: bool = False

    # Misc / special flags
    brainrot: bool = False
    brainrot_twitch: bool = False
    brainrot_tiktok: bool = False
    brainrot_gaming: bool = False
    brainrot_alpha: bool = False
    brainrot_discord: bool = False
    other: bool = False


class Langs(Enum):
    # English variants
    EN = "en"
    EN_UK = "en_uk"
    EN_US = "en_us"
    EN_AU = "en_au"

    # Romance languages
    FR = "fr"
    FR_CA = "fr_ca"
    ES = "es"
    ES_ES = "es_es"
    ES_MX = "es_mx"
    ES_AR = "es_ar"
    IT = "it"
    IT_IT = "it_it"
    IT_CH = "it_ch"
    PT = "pt"
    PT_PT = "pt_pt"
    PT_BR = "pt_br"
    PT_AO = "pt_ao"

    # Germanic languages
    DE = "de"
    DE_DE = "de_de"
    DE_AT = "de_at"
    DE_CH = "de_ch"
    NL = "nl"
    NL_NL = "nl_nl"
    NL_BE = "nl_be"
    NL_SR = "nl_sr"

    # Central & Eastern European languages
    PL = "pl"
    PL_PL = "pl_pl"
    PL_UA = "pl_ua"
    PL_LT = "pl_lt"
    RO = "ro"
    RO_RO = "ro_ro"
    RO_MD = "ro_md"
    RO_RS = "ro_rs"
    HU = "hu"
    HU_HU = "hu_hu"
    HU_AT = "hu_at"
    HU_SK = "hu_sk"
    HU_RS = "hu_rs"

    # Nordic languages
    SV = "sv"
    SV_SE = "sv_se"
    SV_FI = "sv_fi"
    SV_NO = "sv_no"
    SV_DK = "sv_dk"
    DA = "da"
    DA_DK = "da_dk"
    DA_SE = "da_se"
    DA_NO = "da_no"
    DA_GL = "da_gl"
    NO = "no"
    NO_NO = "no_no"
    NO_SE = "no_se"
    NO_DK = "no_dk"
    NO_SA = "no_sa"
    FI = "fi"
    FI_FI = "fi_fi"
    FI_SE = "fi_se"
    FI_RU = "fi_ru"
    FI_EE = "fi_ee"

    # Southern European languages
    EL = "el"
    EL_GR = "el_gr"
    EL_CY = "el_cy"
    EL_TR = "el_tr"
    EL_IT = "el_it"
    EL_AL = "el_al"

    # Other commonly encountered languages
    TR = "tr"
    TR_TR = "tr_tr"
    TR_CY = "tr_cy"
    TR_BG = "tr_bg"
    TR_GR = "tr_gr"
    TR_MK = "tr_mk"
    RU = "ru"
    RU_RU = "ru_ru"
    RU_BY = "ru_by"
    RU_KZ = "ru_kz"
    RU_UA = "ru_ua"
    RU_MD = "ru_md"

    # Brainrot (Gen Alpha internet slang)
    BRAINROT = "brainrot"
    BRAINROT_TWITCH = "brainrot_twitch"
    BRAINROT_TIKTOK = "brainrot_tiktok"
    BRAINROT_GAMING = "brainrot_gaming"
    BRAINROT_ALPHA = "brainrot_alpha"
    BRAINROT_DISCORD = "brainrot_discord"

    OTHER = "other"


COMMAND_TOKEN: str = ":"
COMMAND_TOKEN_LENGTH: int = len(COMMAND_TOKEN)

# REPL / CLI textual constants
POLY_BOOT_MSG = (
    "polyguard — interactive mode\n"
    f"Type '{COMMAND_TOKEN}help' for a short list of commands, '{COMMAND_TOKEN}man' for more details.\n"
    f"Enter a word to test it; '{COMMAND_TOKEN}exit' or '{COMMAND_TOKEN}quit' to leave."
)

POLY_HELP_TEXT = (
    f"Commands (prefix with '{COMMAND_TOKEN}' e.g. '{COMMAND_TOKEN}help'):\n"
    f"  {COMMAND_TOKEN}help        Short help text (this message)\n"
    f"  {COMMAND_TOKEN}man         Longer manual describing usage and options\n"
    f"  {COMMAND_TOKEN}exit, {COMMAND_TOKEN}quit Leave the REPL\n"
    f"  {COMMAND_TOKEN}db          Show configured DB path\n"
    "  <word>       Type a word to check it (no prefix required)\n"
    f"  {COMMAND_TOKEN}log <on/off>        Toggle logging output\n"
    f"  {COMMAND_TOKEN}langopt <lang> <on/off>  Enable/disable a language in your config\n"
    f"  {COMMAND_TOKEN}langs        List languages available in the DB (with counts)\n"
    f"  {COMMAND_TOKEN}langstatus   Show which languages are enabled in your config\n"
    f"  {COMMAND_TOKEN}word <w> [<lang>]  Check a word optionally for a specific language\n"
)

POLY_MAN_TEXT = (
    "polyguard manual\n\n"
    "This REPL accepts single-word queries and returns whether the word\n"
    "is considered a swearword according to the configured language lists.\n\n"
    "If started with --db-path, that DB will be used; otherwise the package\n"
    "default DB is used. You can also pipe words via stdin for batch checks.\n\n"
    "Command prefixing:\n"
    "  To avoid conflicts with words that match command names, commands must be\n"
    f"  prefixed with '{COMMAND_TOKEN}' (for example '{COMMAND_TOKEN}langs' or '{COMMAND_TOKEN}langopt en_uk off'). Any input\n"
    f"  that does not start with '{COMMAND_TOKEN}' is treated as a word to check.\n\n"
    "Additional commands:\n"
    f"  {COMMAND_TOKEN}log <on/off>             Turn logging on or off for the running session.\n"
    f"  {COMMAND_TOKEN}langopt <lang> <on/off>  Temporarily enable or disable a language in your session.\n"
    f"  {COMMAND_TOKEN}langs                    Show languages present in the DB and word counts.\n"
    f"  {COMMAND_TOKEN}langstatus               Show which languages are currently enabled in your config.\n"
    f"  {COMMAND_TOKEN}word <w> [<lang>]        Check <w> in either your current config or a specific language.\n"
)

POLY_PROMPT = "polyguard> "
STATUS_BLOCKED = "BLOCKED"
STATUS_OK = "OK"
DB_PATH_FMT = "DB path: {path}"
