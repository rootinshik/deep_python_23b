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

    for key, values in json_doc.items():
        if key in required_fields:
            for value in values.split():
                if value in keywords:
                    keyword_callback(key, value)
