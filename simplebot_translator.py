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
engines = [
    "google",
    "yandex",
    "bing",
    "sogou",
    "baidu",
    "tencent",
    "youdao",
    "alibaba",
    "deepl",
]


@simplebot.hookimpl
def deltabot_init(bot: DeltaBot) -> None:
    get_engine(bot)  # initialize default engine


@simplebot.hookimpl
def deltabot_start(bot: DeltaBot) -> None:
    assert get_engine(bot) in engines, "Invalid engine, set one of: {!r}".format(
        engines
    )


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
        l1, l2 = args.pop(0), args.pop(0)
        if args:
            text = args.pop()
            quote = message
        elif message.quote:
            text = message.quote.text
            quote = message.quote
        default_engine = get_engine(bot)
        if engines[0] != default_engine:
            engines.remove(default_engine)
            engines.insert(0, default_engine)
        for name in engines:
            try:
                result = getattr(ts, name)(text, from_language=l1, to_language=l2)
                break
            except Exception as ex:  # noqa
                bot.logger.exception(ex)
        else:
            result = "❌ Error! Failed to translate :("
        replies.add(text=result, quote=quote)
    else:
        replies.add(text="\n".join("* {}: {}".format(k, v) for k, v in langs.items()))


def get_engine(bot: DeltaBot) -> str:
    key = "engine"
    value = engines[0]
    val = bot.get(key, scope=__name__)
    if val is None and value is not None:
        bot.set(key, value, scope=__name__)
        val = value
    return val


class TestPlugin:
    """Offline tests"""

    def test_tr(self, mocker):
        quote = mocker.make_incoming_message("hello world")
        msg = mocker.get_one_reply("/tr_en_es", quote=quote)
        assert "hola mundo" in msg.text.lower()

        msg = mocker.get_one_reply("/tr_es_en hola mundo")
        assert "hello world" in msg.text.lower()

        msg = mocker.get_one_reply("/tr")
        assert "*" in msg.text
