class apple_checkcoverage_error(Exception):
    def __init__(self, text: str="error"):
        self.text = text
