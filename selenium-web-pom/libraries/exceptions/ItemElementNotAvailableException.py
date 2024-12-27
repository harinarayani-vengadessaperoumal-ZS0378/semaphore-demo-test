class   ItemElementNotAvailableException(Exception):
    """Exception to Throw when unable to locate Item Element"""
    def __init__(self, element_description):
        self.message = f"{element_description} item element is not available."
        super().__init__(self.message)