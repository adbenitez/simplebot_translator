"""Plugin's hooks and commands definition."""

import simplebot
import translators as ts
from deltachat import Message
from pkg_resources import DistributionNotFound, get_distribution
from simplebot.bot import DeltaBot, Replies

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    __version__ = "0.0.0.dev0-unknown"
langs = {
    "Afrikaans": "af",
    "Albanian": "sq",
    "Amharic": "am",
    "Arabic": "ar",
    "Armenian": "hy",
    "Azerbaijani": "az",
    "Basque": "eu",
    "Belarusian": "be",
    "Bengali": "bn",
    "Bosnian": "bs",
    "Bulgarian": "bg",
    "Catalan": "ca",
    "Cebuano": "ceb",
    "Chichewa": "ny",
    "Chinese (simplified)": "zh-CN",
    "Chinese (traditional)": "zh-TW",
    "Corsican": "co",
    "Croatian": "hr",
    "Czech": "cs",
    "Danish": "da",
    "Dutch": "nl",
    "English": "en",
    "Esperanto": "eo",
    "Estonian": "et",
    "Filipino": "tl",
    "Finnish": "fi",
    "French": "fr",
    "Frisian": "fy",
    "Galician": "gl",
    "Georgian": "ka",
    "German": "de",
    "Greek": "el",
    "Gujarati": "gu",
    "Haitian creole": "ht",
    "Hausa": "ha",
    "Hawaiian": "haw",
    "Hebrew": "iw",
    "Hindi": "hi",
    "Hmong": "hmn",
    "Hungarian": "hu",
    "Icelandic": "is",
    "Igbo": "ig",
    "Indonesian": "id",
    "Irish": "ga",
    "Italian": "it",
    "Japanese": "ja",
    "Javanese": "jw",
    "Kannada": "kn",
    "Kazakh": "kk",
    "Khmer": "km",
    "Korean": "ko",
    "Kurdish (kurmanji)": "ku",
    "Kyrgyz": "ky",
    "Lao": "lo",
    "Latin": "la",
    "Latvian": "lv",
    "Lithuanian": "lt",
    "Luxembourgish": "lb",
    "Macedonian": "mk",
    "Malagasy": "mg",
    "Malay": "ms",
    "Malayalam": "ml",
    "Maltese": "mt",
    "Maori": "mi",
    "Marathi": "mr",
    "Mongolian": "mn",
    "Myanmar (burmese)": "my",
    "Nepali": "ne",
    "Norwegian": "no",
    "Pashto": "ps",
    "Persian": "fa",
    "Polish": "pl",
    "Portuguese": "pt",
    "Punjabi": "pa",
    "Romanian": "ro",
    "Russian": "ru",
    "Samoan": "sm",
    "Scots gaelic": "gd",
    "Serbian": "sr",
    "Sesotho": "st",
    "Shona": "sn",
    "Sindhi": "sd",
    "Sinhala": "si",
    "Slovak": "sk",
    "Slovenian": "sl",
    "Somali": "so",
    "Spanish": "es",
    "Sundanese": "su",
    "Swahili": "sw",
    "Swedish": "sv",
    "Tajik": "tg",
    "Tamil": "ta",
    "Telugu": "te",
    "Thai": "th",
    "Turkish": "tr",
    "Ukrainian": "uk",
    "Urdu": "ur",
    "Uzbek": "uz",
    "Vietnamese": "vi",
    "Welsh": "cy",
    "Xhosa": "xh",
    "Yiddish": "yi",
    "Yoruba": "yo",
    "Zulu": "zu",
    "Auto-detect": "auto",
}
engines = ts.translators_pool


@simplebot.hookimpl
def deltabot_init(bot: DeltaBot) -> None:
    _get_engine(bot)  # initialize default engine
    filter_enabled = _get_setting(bot, "filter_enabled", "yes")
    if filter_enabled == "yes":
        lang = bot.get("language") or "en"
        bot.add_preference(
            "language",
            "Language to translate received text, default value is"
            f" {lang!r}, example values: en, es, de, ...",
        )
        bot.filters.register(translate_filter)


@simplebot.hookimpl
def deltabot_start(bot: DeltaBot) -> None:
    assert _get_engine(bot) in engines, f"Invalid engine, set one of: {engines!r}"


def translate_filter(bot: DeltaBot, message: Message, replies: Replies) -> None:
    """Send me in private any text message to translate it."""
    if not message.chat.is_multiuser() and message.text:
        lang = _get_language(bot, message.get_sender_contact().addr)
        if lang in langs.values():
            text = _translate("auto", lang, message.text, bot)
        else:
            text = (
                f"❌ Invalid language code: {lang!r}."
                " Send /tr to see the list of available codes."
            )
        replies.add(text=text, quote=message)


@simplebot.command
def tr(bot: DeltaBot, payload: str, message: Message, replies: Replies) -> None:
    """Translate text. You must pass origin and destination language.

    Examples:
    To translate from English to Spanish:
    /tr en es hello world
    To detect language automatically and translate it to Spanish:
    /tr auto es hello world
    To see the list of language codes:
    /tr
    You can also quote-reply a message with the command to translate it.
    """
    if payload:
        args = payload.split(maxsplit=2)
        if len(args) == 3:
            l1, l2, text = args
            quote = message
        elif len(args) == 2 and message.quote and message.quote.text:
            l1, l2 = args
            text = message.quote.text
            quote = message.quote
        else:
            replies.add(
                text="❌ Wrong usage. Valid requests look like:\n/tr_en_ja hello world",
                quote=message,
            )
            return
        if l1 not in langs.values() or l2 not in langs.values():
            replies.add(
                text="❌ Invalid language code. Send /tr to see the list of available codes.",
                quote=message,
            )
            return
        replies.add(text=_translate(l1, l2, text, bot), quote=quote)
    else:
        replies.add(text="\n".join(f"* {k}: {v}" for k, v in langs.items()))


def _translate(l1: str, l2: str, text: str, bot: DeltaBot) -> str:
    default_engine = _get_engine(bot)
    if engines[0] != default_engine:
        engines.remove(default_engine)
        engines.insert(0, default_engine)
    for name in engines:
        try:
            result = ts.translate_text(
                text, translator=name, from_language=l1, to_language=l2
            )
            break
        except Exception as ex:  # noqa
            bot.logger.exception(ex)
    else:
        result = "❌ Error! Failed to translate :("
    return result


def _get_engine(bot: DeltaBot) -> str:
    return _get_setting(bot, "engine", "google")


def _get_setting(bot: DeltaBot, key: str, value=None) -> str:
    scope = __name__.split(".", maxsplit=1)[0]
    val = bot.get(key, scope=scope)
    if val is None and value is not None:
        bot.set(key, value, scope=scope)
        val = value
    return val


def _get_language(bot, addr: str) -> str:
    return bot.get("language", scope=addr) or bot.get("language") or "en"


class TestPlugin:
    """Online tests"""

    def test_tr(self, mocker):
        quote = mocker.make_incoming_message("hello world")
        msg = mocker.get_one_reply("/tr_en_es", quote=quote)
        assert "hola mundo" in msg.text.lower()

        msg = mocker.get_one_reply("/tr_es_en hola mundo")
        assert "hello world" in msg.text.lower()

        msg = mocker.get_one_reply("/tr_es hello")
        assert "❌ Wrong usage" in msg.text

        msg = mocker.get_one_reply("/tr_foo_bar hello")
        assert "❌ Invalid language code" in msg.text

        msg = mocker.get_one_reply("/tr")
        assert "*" in msg.text

    def test_filter(self, mocker):
        msg = mocker.get_one_reply("hola mundo")
        assert "hello world" in msg.text.lower()

        # filter should work only in private/direct chat
        msgs = mocker.get_replies("hola mundo", group="group1")
        assert not msgs
