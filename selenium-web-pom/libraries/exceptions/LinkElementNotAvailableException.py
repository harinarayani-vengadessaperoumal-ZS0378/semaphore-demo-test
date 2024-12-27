class   LinkElementNotAvailableException(Exception):
    """Exception to Throw when unable to locate Link Element"""
    def __init__(self, element_description):
        self.message = f"{element_description} link element is not available."
        super().__init__(self.message)