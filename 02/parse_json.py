import json


def example_callback(key: str, value: str) -> None:
    print(f"{key=}, {value=}")


def parse_json(
    json_str: str,
    required_fields: list[str] = None,
    keywords: list[str] = None,
    keyword_callback: callable = None,
) -> None:
    json_doc = json.loads(json_str)
    required_doc = {
        required_fields[i]:
            keywords.copy() for i in range(len(required_fields))
    }

    for key, values in json_doc.items():
        if key in required_doc.keys():
            for value in values.split():
                if value in required_doc[key]:
                    keyword_callback(key, value)
