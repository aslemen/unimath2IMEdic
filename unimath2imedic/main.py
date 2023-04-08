import codecs
import re
import typing
from requests_cache.session import CachedSession

from . import roman2kana

_re_ITEM = re.compile(
    r'^\\UnicodeMathSymbol\{"(?P<point>.{5})\}\{\\(?P<name>\S+)\s*\}\{\\(?P<type>\S+)\}\{(?P<desc>.*?)\}'
)

def generate(out: typing.BinaryIO):
    session = CachedSession(
        "unicode-math-to-imedic",
        backend = "filesystem",
        use_cache_dir = True,
    )
    r = session.get(
        "http://mirrors.ctan.org/macros/unicodetex/latex/unicode-math/unicode-math-table.tex",
        stream = True
    )

    out.write(codecs.BOM_UTF16_LE)
    for line in map(lambda b: b.decode("utf-8"), r.iter_lines()):
        if match := _re_ITEM.match(line):
            char = chr(int(match.group("point"), base = 16))
            name = match.group("name")
            yomi = roman2kana.roman2kana_msime(
                name.lower()
            )
            
            # description length limit: 128 characters
            description = f"unicode-math symbol: \\{name} 【{match.group('type')}】 {match.group('desc')}"[:128]

            out.write(
                f"{yomi}\t{char}\t顔文字\t{description}\r\n".encode("utf-16-le")
            )