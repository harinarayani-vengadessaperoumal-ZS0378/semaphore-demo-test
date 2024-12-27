class   TabElementNotAvailableException(Exception):
    """Exception to Throw when unable to locate Tab Element"""
    def __init__(self, element_description):
        self.message = f"{element_description} tab element is not available."
        super().__init__(self.message)