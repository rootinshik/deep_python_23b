import json


def example_callback(key: str, value: str) -> None:
    print(f"{key=}, {value=}")


def parse_json(
    json_str: str = None,
    required_fields: list[str] = None,
    keywords: list[str] = None,
    keyword_callback: callable = None,
) -> None:

    if required_fields is None:
        raise AttributeError("required_fields is None")
    if keywords is None:
        raise AttributeError("keywords is None")
    if keyword_callback is None:
        raise AttributeError("keyword_callback is None")

    json_doc = json.loads(json_str)

    for key, values in json_doc.items():
        if key in required_fields:
            for value in values.split():
                if value.lower() in map(lambda x: x.lower(), keywords):
                    keyword_callback(key, value)
