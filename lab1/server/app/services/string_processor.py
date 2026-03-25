class StringProcessor:
    @staticmethod
    def change_brackets(value: str | None) -> str | None:
        if not value:
            return None

        res = value.replace('(', '[')
        res = res.replace(')', ']')

        return res