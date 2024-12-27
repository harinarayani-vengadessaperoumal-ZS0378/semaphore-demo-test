class   CheckBoxElementNotAvailableException(Exception):
    """Exception to Throw when unable to locate Check Box Element"""
    def __init__(self, element_description):
        self.message = f"{element_description} check box element is not available."
        super().__init__(self.message)