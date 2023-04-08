import codecs
from dataclasses import dataclass
import re
import typing
from requests_cache.session import CachedSession
from . import roman2kana

@dataclass(frozen=True, slots=True)
class CharInfo:
    char: str
    name: str
    type: str
    description: str

_re_ITEM = re.compile(
    r'^\\UnicodeMathSymbol\{"(?P<point>.{5})\}\{\\(?P<name>\S+)\s*\}\{\\(?P<type>\S+)\}\{(?P<desc>.*?)\}'
)

_re_PREFIX_TO_STRIP = re.compile(r"^(mup|mdlgwht|mdlgblk)(?P<name>.*)")

def gen_mappging() -> typing.Iterator[CharInfo]:
    session = CachedSession(
        "unicode-math-to-imedic",
        backend = "filesystem",
        use_cache_dir = True,
    )
    r = session.get(
        "http://mirrors.ctan.org/macros/unicodetex/latex/unicode-math/unicode-math-table.tex",
        stream = True
    )

    for line in map(lambda b: b.decode("utf-8"), r.iter_lines()):
        if match := _re_ITEM.match(line):
            info = CharInfo(
                char = chr(int(match.group("point"), base = 16)),
                name = match.group("name"),
                type = match.group('type'),
                description = match.group('desc'),
            )
            yield info

            if match := _re_PREFIX_TO_STRIP.match(info.name):
                yield CharInfo(
                    char = info.char,
                    name = match.group("name"),
                    type = info.type,
                    description = info.description,
                )

def generate(out: typing.BinaryIO):
    out.write(codecs.BOM_UTF16_LE)
    for info in gen_mappging():
        yomi = roman2kana.roman2kana_MSIME(
            info.name.lower()
        )
        
        # description length limit: 128 characters
        description = f"unicode-math symbol: \\{info.name} 【{info.type}】 {info.description}"[:128]

        out.write(
            f"{yomi}\t{info.char}\t顔文字\t{description}\r\n".encode("utf-16-le")
        )