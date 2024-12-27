class TextFieldNotAvailableException(Exception):
    """Exception to Throw when unable to locate Text Element"""
    def __init__(self, element_description):
        self.message = f"{element_description} text field is not available."
        super().__init__(self.message)