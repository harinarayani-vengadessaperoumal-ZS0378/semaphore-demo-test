import configparser
from pathlib import Path
from robot.api.deco import keyword

class   PropertiesFileReader():
    properties_filepath = Path(__file__).resolve().parents[2]/"config.properties"

    @keyword('Get Value From Properties File')
    def get_value_from_properties_file(self,property_key):
        result = False
        try:
            config = configparser.ConfigParser()
            print(f"Config File Path : {self.properties_filepath}")
            config.read(self.properties_filepath)
            for section in config.sections():
                if property_key in config[section]:
                    result = True
                    return config[section][property_key]
            if result is not True:
                print(f'{property_key} is not found in {self.properties_filepath} file.')
                return None       
            
        except Exception as err:
            print(f'Error in Get_Value_From_Properties_File method : {repr(err)}')
            return None