import re


def replace_placeholders(config_data: dict) -> dict:
    def replace_value(value, context):
        if isinstance(value, str):
            while True:
                matches = re.findall(r"\${(.*?)}", value)
                if not matches:
                    break
                for match in matches:
                    keys = match.split(".")
                    replacement = context
                    for key in keys:
                        replacement = replacement.get(key, "")
                    value = value.replace(f"${{{match}}}", replacement)
        return value

    def recursive_replace(data, context):
        if isinstance(data, dict):
            return {k: recursive_replace(v, context) for k, v in data.items()}
        elif isinstance(data, list):
            return [recursive_replace(item, context) for item in data]
        else:
            return replace_value(data, context)

    return recursive_replace(config_data, config_data)


def main():
    pass


if __name__ == "__main__":
    main()
