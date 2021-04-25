import simplebot
import translators as ts
from deltachat import Message
from simplebot.bot import DeltaBot, Replies

__version__ = "1.0.0"
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
    assert get_engine(bot) in engines, "Invalid engine, set one of: {!r}".format(
        engines
    )


@simplebot.command
def tr(bot: DeltaBot, payload: str, message: Message, replies: Replies) -> None:
    """Translate text.

    You need to pass origin and destination language.
    Example: `/tr en es hello world`
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
        engine = getattr(ts, get_engine(bot))
        replies.add(text=engine(text, from_language=l1, to_language=l2), quote=quote)
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
    def test_tr(self, mocker):
        quote = mocker.make_incoming_message("hello world")
        msg = mocker.get_one_reply("/tr_en_es", quote=quote)
        assert "hola mundo" in msg.text.lower()

        msg = mocker.get_one_reply("/tr_es_en hola mundo")
        assert "hello world" in msg.text.lower()

        msg = mocker.get_one_reply("/tr")
        assert "*" in msg.text
