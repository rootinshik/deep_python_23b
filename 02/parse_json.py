import json


def example_callback(key: str, value: str) -> None:
    print(f"{key=}, {value=}")


def parse_json(
    json_str: str = None,
    required_fields: list[str] = None,
    keywords: list[str] = None,
    keyword_callback: callable = None,
) -> None:
    json_doc = json.loads(json_str)
    required_doc = {
        required_fields[i]: keywords.copy() for i in range(len(required_fields))
    }

    for key, values in json_doc.items():
        if key in required_doc.keys():
            for value in values.split():
                if value in required_doc[key]:
                    keyword_callback(key, value)


if __name__ == "__main__":
    parse_json(
        json_str='{"key1": "Word1 word2", "key2": "word2 word3"}',
        required_fields=["key1"],
        keywords=["word2"],
        keyword_callback=example_callback,
    )
