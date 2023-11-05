import json
import sys
from collections import Counter
from string import ascii_lowercase

import aiohttp
from bs4 import BeautifulSoup


async def parse_response(
        response: aiohttp.ClientResponse,
        top_k: int = 5
) -> str:
    data = await response.text()
    data = BeautifulSoup(data, "html.parser").get_text().lower().split()
    words = filter(
        lambda word: all(sym in ascii_lowercase for sym in word),
        data
    )
    word_count = dict(Counter(words).most_common(top_k))
    return json.dumps(word_count, ensure_ascii=False)


async def return_status_code(response: aiohttp.ClientResponse) -> int:
    return response.status


def parse_args() -> tuple[int, str]:
    if 3 <= len(sys.argv) <= 4:
        return int(sys.argv[-2]), sys.argv[-1]
    raise ValueError
