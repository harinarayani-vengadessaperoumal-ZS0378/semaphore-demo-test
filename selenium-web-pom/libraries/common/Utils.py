import re
import os
import time
from pathlib import Path
from contextlib import suppress
from datetime import datetime, timedelta
from robot.libraries.BuiltIn import BuiltIn
from libraries.common.Drivers import drivers
import json

class   Utils:
    """ Utils class to have all helper methods"""
    
    @staticmethod
    def wait_for_page_load(timeout=20):
        """
        Wait for the page to completely load by checking the document's readyState.
        """
        time.sleep(0.5)
        with suppress(Exception):
            seleniumlib = drivers.get_selinuim_driver()
            seleniumlib.wait_for_condition(
                'return document.readyState == "complete";', 
                timeout=timeout
            )

    @staticmethod
    def wait_for_elements(elem,timeout=20):
        """
        Wait for element(s) and returns element(s) if element(s) present in the DOM
        """
        seleniumlib = drivers.get_selinuim_driver()
        for attempt in range(timeout):
            elems = seleniumlib.find_elements(elem)
            time.sleep(0.5)
            if elems:
                return elems
        else:
            return None
        
    @staticmethod    
    def un_wrap(values):
        """
        Remove brackets if a single value is enclosed
        """
        if isinstance(values,tuple) or isinstance(values,list):
            un_wraped_list = [value[0] if (type(value) in (list,tuple) and len(value)==1) else value for value in values]
            return un_wraped_list
        return values
    
    @staticmethod    
    def log_output(*args,**kwargs):
        built_in = BuiltIn()
        built_in.log(*args,**kwargs)

    @staticmethod    
    def compare_using_soft_assert(list_of_value1,list_of_value2):

        failed_list = []

        for index in range(len(list_of_value1)):
            if list_of_value1[index]!=list_of_value2[index] :
                failed_list.append(f"{list_of_value1[index]}-{list_of_value2[index]}")

        if failed_list:
            assert False,f"Below Option(s) are not matching\n{failed_list}"
        else:
            Utils.log_output(f"All Option(s) are matching")
        
    @staticmethod
    def get_project_root():
        """Get Project Root directory"""
        # Go up to the root directory of the project
        return os.path.abspath(Path(__file__).parent.parent.parent)