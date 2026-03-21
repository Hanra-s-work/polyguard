"""Unit tests for the constants module."""

import pytest
from pathlib import Path

from polyguard.src import constants as POLY_CONST


class TestModulePaths:
    """Test module path constants."""

    def test_module_root_exists(self):
        """Test that MODULE_ROOT points to an existing directory."""
        assert POLY_CONST.MODULE_ROOT.exists()
        assert POLY_CONST.MODULE_ROOT.is_dir()

    def test_module_root_contains_src(self):
        """Test that MODULE_ROOT contains the src directory."""
        src_dir = POLY_CONST.MODULE_ROOT / "src"
        assert src_dir.exists()

    def test_module_root_contains_data(self):
        """Test that MODULE_ROOT contains the data directory."""
        data_dir = POLY_CONST.MODULE_ROOT / "data"
        assert data_dir.exists()

    def test_default_db_path_structure(self):
        """Test that DEFAULT_DB_PATH is under data directory."""
        assert "data" in str(POLY_CONST.DEFAULT_DB_PATH)
        assert str(POLY_CONST.DEFAULT_DB_PATH).endswith(".sqlite")

    def test_default_db_path_parent_exists(self):
        """Test that DEFAULT_DB_PATH parent directory exists."""
        assert POLY_CONST.DEFAULT_DB_PATH.parent.exists()

    def test_default_source_words_exists(self):
        """Test that DEFAULT_SOURCE_WORDS points to existing wordlists directory."""
        assert POLY_CONST.DEFAULT_SOURCE_WORDS.exists()
        assert POLY_CONST.DEFAULT_SOURCE_WORDS.is_dir()


class TestCacheConstants:
    """Test cache-related constants."""

    def test_default_cache_max_langs_positive(self):
        """Test that DEFAULT_CACHE_MAX_LANGS is positive."""
        assert POLY_CONST.DEFAULT_CACHE_MAX_LANGS > 0

    def test_default_cache_max_langs_reasonable(self):
        """Test that DEFAULT_CACHE_MAX_LANGS has a reasonable value."""
        assert 1 <= POLY_CONST.DEFAULT_CACHE_MAX_LANGS <= 100


class TestLangConfig:
    """Test LangConfig dataclass."""

    def test_lang_config_instantiation_default(self):
        """Test LangConfig instantiation with defaults."""
        config = POLY_CONST.LangConfig()
        assert config is not None
        assert isinstance(config, POLY_CONST.LangConfig)

    def test_lang_config_has_english_variants(self):
        """Test that LangConfig has all English variants."""
        config = POLY_CONST.LangConfig()
        assert hasattr(config, 'en')
        assert hasattr(config, 'en_uk')
        assert hasattr(config, 'en_us')
        assert hasattr(config, 'en_au')

    def test_lang_config_has_western_european(self):
        """Test that LangConfig has Western European languages."""
        config = POLY_CONST.LangConfig()
        assert hasattr(config, 'fr')
        assert hasattr(config, 'de')
        assert hasattr(config, 'it')
        assert hasattr(config, 'pt')
        assert hasattr(config, 'nl')
        assert hasattr(config, 'es')

    def test_lang_config_has_central_eastern_european(self):
        """Test that LangConfig has Central/Eastern European languages."""
        config = POLY_CONST.LangConfig()
        assert hasattr(config, 'pl')
        assert hasattr(config, 'ro')
        assert hasattr(config, 'hu')

    def test_lang_config_has_nordic_languages(self):
        """Test that LangConfig has Nordic languages."""
        config = POLY_CONST.LangConfig()
        assert hasattr(config, 'sv')
        assert hasattr(config, 'da')
        assert hasattr(config, 'no')
        assert hasattr(config, 'fi')

    def test_lang_config_has_other_languages(self):
        """Test that LangConfig has other commonly encountered languages."""
        config = POLY_CONST.LangConfig()
        assert hasattr(config, 'el')  # Greek
        assert hasattr(config, 'tr')  # Turkish
        assert hasattr(config, 'ru')  # Russian

    def test_lang_config_has_brainrot(self):
        """Test that LangConfig has brainrot variants."""
        config = POLY_CONST.LangConfig()
        assert hasattr(config, 'brainrot')
        assert hasattr(config, 'brainrot_twitch')
        assert hasattr(config, 'brainrot_tiktok')
        assert hasattr(config, 'brainrot_gaming')
        assert hasattr(config, 'brainrot_alpha')
        assert hasattr(config, 'brainrot_discord')

    def test_lang_config_has_other(self):
        """Test that LangConfig has 'other' field."""
        config = POLY_CONST.LangConfig()
        assert hasattr(config, 'other')

    def test_lang_config_default_enabled_languages(self):
        """Test that default enabled languages are correct."""
        config = POLY_CONST.LangConfig()
        # English should be enabled by default
        assert config.en is True
        # Most regional variants should be disabled by default
        assert config.en_uk is False
        assert config.en_us is False

    def test_lang_config_modify(self):
        """Test that LangConfig fields can be modified."""
        config = POLY_CONST.LangConfig()
        config.en_us = True
        config.fr = False

        assert config.en_us is True
        assert config.fr is False

    def test_lang_config_disabled_by_default(self):
        """Test that most regional variants are disabled by default."""
        config = POLY_CONST.LangConfig()

        # Check that regional variants are False by default
        regional_variants = [
            'en_uk', 'en_us', 'en_au',
            'fr_ca', 'es_es', 'es_mx', 'es_ar',
            'de_de', 'de_at', 'de_ch',
            'it_it', 'it_ch',
            'pt_pt', 'pt_br', 'pt_ao',
            'nl_nl', 'nl_be', 'nl_sr',
        ]

        for variant in regional_variants:
            assert getattr(
                config, variant) is False, f"{variant} should be False by default"


class TestLangsEnum:
    """Test Langs enum."""

    def test_langs_enum_exists(self):
        """Test that Langs enum is defined."""
        assert hasattr(POLY_CONST, 'Langs')
        assert isinstance(POLY_CONST.Langs, type)

    def test_langs_enum_has_english_variants(self):
        """Test that Langs enum has English variants."""
        assert hasattr(POLY_CONST.Langs, 'EN')
        assert hasattr(POLY_CONST.Langs, 'EN_UK')
        assert hasattr(POLY_CONST.Langs, 'EN_US')
        assert hasattr(POLY_CONST.Langs, 'EN_AU')

    def test_langs_enum_has_romance_languages(self):
        """Test that Langs enum has Romance language variants."""
        assert hasattr(POLY_CONST.Langs, 'FR')
        assert hasattr(POLY_CONST.Langs, 'FR_CA')
        assert hasattr(POLY_CONST.Langs, 'ES')
        assert hasattr(POLY_CONST.Langs, 'ES_ES')
        assert hasattr(POLY_CONST.Langs, 'IT')
        assert hasattr(POLY_CONST.Langs, 'IT_IT')
        assert hasattr(POLY_CONST.Langs, 'PT')
        assert hasattr(POLY_CONST.Langs, 'PT_PT')
        assert hasattr(POLY_CONST.Langs, 'PT_BR')

    def test_langs_enum_has_germanic_languages(self):
        """Test that Langs enum has Germanic language variants."""
        assert hasattr(POLY_CONST.Langs, 'DE')
        assert hasattr(POLY_CONST.Langs, 'DE_DE')
        assert hasattr(POLY_CONST.Langs, 'NL')
        assert hasattr(POLY_CONST.Langs, 'NL_NL')

    def test_langs_enum_has_central_eastern_europe(self):
        """Test that Langs enum has Central/Eastern European languages."""
        assert hasattr(POLY_CONST.Langs, 'PL')
        assert hasattr(POLY_CONST.Langs, 'PL_PL')
        assert hasattr(POLY_CONST.Langs, 'RO')
        assert hasattr(POLY_CONST.Langs, 'RO_RO')
        assert hasattr(POLY_CONST.Langs, 'HU')
        assert hasattr(POLY_CONST.Langs, 'HU_HU')

    def test_langs_enum_has_nordic_languages(self):
        """Test that Langs enum has Nordic languages."""
        assert hasattr(POLY_CONST.Langs, 'SV')
        assert hasattr(POLY_CONST.Langs, 'SV_SE')
        assert hasattr(POLY_CONST.Langs, 'DA')
        assert hasattr(POLY_CONST.Langs, 'DA_DK')
        assert hasattr(POLY_CONST.Langs, 'NO')
        assert hasattr(POLY_CONST.Langs, 'NO_NO')
        assert hasattr(POLY_CONST.Langs, 'FI')
        assert hasattr(POLY_CONST.Langs, 'FI_FI')

    def test_langs_enum_has_southern_european(self):
        """Test that Langs enum has Southern European languages."""
        assert hasattr(POLY_CONST.Langs, 'EL')
        assert hasattr(POLY_CONST.Langs, 'EL_GR')
        assert hasattr(POLY_CONST.Langs, 'EL_CY')

    def test_langs_enum_has_other_commonly_encountered(self):
        """Test that Langs enum has other commonly encountered languages."""
        assert hasattr(POLY_CONST.Langs, 'TR')
        assert hasattr(POLY_CONST.Langs, 'TR_TR')
        assert hasattr(POLY_CONST.Langs, 'RU')
        assert hasattr(POLY_CONST.Langs, 'RU_RU')

    def test_langs_enum_has_brainrot(self):
        """Test that Langs enum has brainrot variants."""
        assert hasattr(POLY_CONST.Langs, 'BRAINROT')
        assert hasattr(POLY_CONST.Langs, 'BRAINROT_TWITCH')
        assert hasattr(POLY_CONST.Langs, 'BRAINROT_TIKTOK')
        assert hasattr(POLY_CONST.Langs, 'BRAINROT_GAMING')
        assert hasattr(POLY_CONST.Langs, 'BRAINROT_ALPHA')
        assert hasattr(POLY_CONST.Langs, 'BRAINROT_DISCORD')

    def test_langs_enum_has_other(self):
        """Test that Langs enum has 'other' value."""
        assert hasattr(POLY_CONST.Langs, 'OTHER')

    def test_langs_enum_values_are_strings(self):
        """Test that all Langs enum values are strings."""
        for member in POLY_CONST.Langs:
            assert isinstance(member.value, str)

    def test_langs_enum_values_are_lowercase(self):
        """Test that all Langs enum values are lowercase."""
        for member in POLY_CONST.Langs:
            assert member.value == member.value.lower()

    def test_langs_enum_values_match_naming(self):
        """Test that Langs enum values match their naming convention."""
        assert POLY_CONST.Langs.EN.value == "en"
        assert POLY_CONST.Langs.EN_UK.value == "en_uk"
        assert POLY_CONST.Langs.FR.value == "fr"
        assert POLY_CONST.Langs.FR_CA.value == "fr_ca"

    def test_langs_enum_total_count(self):
        """Test that Langs enum has expected number of entries."""
        # Should have at least 56 entries (all languages + variants)
        count = len(POLY_CONST.Langs)
        assert count >= 56, f"Expected at least 56 Langs entries, got {count}"

    def test_all_lang_config_attributes_have_enum_entry(self):
        """Test that all LangConfig attributes have corresponding Langs enum entries."""
        config = POLY_CONST.LangConfig()
        config_attrs = vars(config)

        lang_enum_values = {member.value for member in POLY_CONST.Langs}

        for attr_name in config_attrs:
            # The attribute name is the key, which should match a language code
            assert attr_name in lang_enum_values, \
                f"LangConfig attribute '{attr_name}' has no corresponding Langs enum entry"


class TestCommandConstants:
    """Test command and textual constants."""

    def test_command_token_defined(self):
        """Test that COMMAND_TOKEN is defined."""
        assert hasattr(POLY_CONST, 'COMMAND_TOKEN')
        assert isinstance(POLY_CONST.COMMAND_TOKEN, str)

    def test_command_token_non_empty(self):
        """Test that COMMAND_TOKEN is non-empty."""
        assert len(POLY_CONST.COMMAND_TOKEN) > 0

    def test_command_token_length_correct(self):
        """Test that COMMAND_TOKEN_LENGTH matches COMMAND_TOKEN length."""
        assert POLY_CONST.COMMAND_TOKEN_LENGTH == len(POLY_CONST.COMMAND_TOKEN)

    def test_command_token_length_matches_token(self):
        """Test that COMMAND_TOKEN_LENGTH is consistent with COMMAND_TOKEN."""
        expected_length = len(POLY_CONST.COMMAND_TOKEN)
        assert POLY_CONST.COMMAND_TOKEN_LENGTH == expected_length

    def test_poly_boot_msg_defined(self):
        """Test that POLY_BOOT_MSG is defined."""
        assert hasattr(POLY_CONST, 'POLY_BOOT_MSG')
        assert isinstance(POLY_CONST.POLY_BOOT_MSG, str)

    def test_poly_boot_msg_non_empty(self):
        """Test that POLY_BOOT_MSG is non-empty."""
        assert len(POLY_CONST.POLY_BOOT_MSG) > 0

    def test_poly_help_text_defined(self):
        """Test that POLY_HELP_TEXT is defined."""
        assert hasattr(POLY_CONST, 'POLY_HELP_TEXT')
        assert isinstance(POLY_CONST.POLY_HELP_TEXT, str)

    def test_poly_help_text_non_empty(self):
        """Test that POLY_HELP_TEXT is non-empty."""
        assert len(POLY_CONST.POLY_HELP_TEXT) > 0

    def test_poly_man_text_defined(self):
        """Test that POLY_MAN_TEXT is defined."""
        assert hasattr(POLY_CONST, 'POLY_MAN_TEXT')
        assert isinstance(POLY_CONST.POLY_MAN_TEXT, str)

    def test_poly_man_text_non_empty(self):
        """Test that POLY_MAN_TEXT is non-empty."""
        assert len(POLY_CONST.POLY_MAN_TEXT) > 0

    def test_poly_prompt_defined(self):
        """Test that POLY_PROMPT is defined."""
        assert hasattr(POLY_CONST, 'POLY_PROMPT')
        assert isinstance(POLY_CONST.POLY_PROMPT, str)

    def test_status_constants_defined(self):
        """Test that status constants are defined."""
        assert hasattr(POLY_CONST, 'STATUS_BLOCKED')
        assert hasattr(POLY_CONST, 'STATUS_OK')
        assert isinstance(POLY_CONST.STATUS_BLOCKED, str)
        assert isinstance(POLY_CONST.STATUS_OK, str)

    def test_db_path_fmt_defined(self):
        """Test that DB_PATH_FMT is defined and is a format string."""
        assert hasattr(POLY_CONST, 'DB_PATH_FMT')
        assert isinstance(POLY_CONST.DB_PATH_FMT, str)
        assert '{path}' in POLY_CONST.DB_PATH_FMT

    def test_db_path_fmt_formattable(self):
        """Test that DB_PATH_FMT can be formatted."""
        result = POLY_CONST.DB_PATH_FMT.format(path="/test/path/db.sqlite")
        assert "/test/path/db.sqlite" in result

    def test_status_constants_different(self):
        """Test that status constants have different values."""
        assert POLY_CONST.STATUS_BLOCKED != POLY_CONST.STATUS_OK

    def test_help_text_contains_command_token(self):
        """Test that help text contains references to command tokens."""
        assert POLY_CONST.COMMAND_TOKEN in POLY_CONST.POLY_HELP_TEXT
