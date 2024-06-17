class ApiResultItem():
    def __init__(self, errors: [], data: dict):
        self.errors = errors
        self.data = data

    def to_dict(self) -> {}:
        return {
            "errors": self.errors,
            "data": self.data
        }