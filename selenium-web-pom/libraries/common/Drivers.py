from robot.libraries.BuiltIn import BuiltIn

class drivers:
    
    @staticmethod
    def get_selinuim_driver():
        built_in = BuiltIn()
        driver = built_in.get_library_instance(name="SeleniumLibrary")
        return driver