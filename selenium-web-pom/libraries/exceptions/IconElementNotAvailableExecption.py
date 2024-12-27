class   IconElementNotAvailableExecption(Exception):
    """Exception to Throw when unable to locate Icon Element"""
    def __init__(self, element_description):
        self.message = f"{element_description} icon element is not available."
        super().__init__(self.message)