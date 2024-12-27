class   ButtonElementNotAvailableException(Exception):
    """Exception to Throw when unable to locate Button Element"""
    def __init__(self, element_description):
        self.message = f"{element_description} button element is not available."
        super().__init__(self.message)