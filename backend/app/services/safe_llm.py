class SafeLLM:

    @staticmethod
    def ensure_list(value):
        if value is None:
            return []
        if isinstance(value, str):
            return [value]
        if isinstance(value, list):
            return value
        return [str(value)]

    @staticmethod
    def ensure_string_list(value):
        return [str(v) for v in SafeLLM.ensure_list(value)]
