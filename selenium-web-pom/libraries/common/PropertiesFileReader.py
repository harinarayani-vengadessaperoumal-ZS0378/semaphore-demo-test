import configparser
import os
class PropertiesFileReader:

    @staticmethod
    def get_value_from_properties_file(property_key, filepath):
        """Method to read values from the properties file"""
        result = False
        try:
            config = configparser.ConfigParser()
            #print(f"Config File Path : {filepath}")
            if os.path.exists(filepath):
                config.read(filepath)
                for section in config.sections():
                    if property_key in config[section]:
                        result = True
                        return config[section][property_key]
                if result is not True:
                    print(f'{property_key} is not found in "{filepath}" file.')
                    return None 
            else:
                print(f"Error in Get_Value_From_Properties_File method : Filename '{filepath}' does not exists.")
                raise FileNotFoundError
        
        except Exception as err:
            print(f'Error in Get_Value_From_Properties_File method : {repr(err)}')
            raise err