import os
import json

from libraries.common.Utils import Utils

class   Config(object):
    """Configuration for this test suite.

    This creates a variable named CONFIG (${CONFIG}) when included
    in a test as a variable file.
    """
    ROBOT_LIBRARY_SCOPE = 'GLOBAL'
    website = None
    timeout = None
    report_path = None

    @staticmethod
    def initialize(environment):
        """Read configuration values based on the environment."""
        # Load environment details from JSON
        environmentfile_path = os.path.join(Utils.get_project_root(), 'data', 'environment.json')

        # Load the JSON file
        with open(environmentfile_path, "r") as file:
            env_data = json.load(file)

        env_details = env_data.get(environment)
        if not env_details:
            raise ValueError(f"Environment '{environment}' not found in environment.json")
        
        # Set website and timeout from env_details
        Config.website = env_details.get("website")
        Config.timeout = env_details.get("timeout", 30)  # default to 30 if not specified

# This creates a variable that robot can see named ${CONFIG}
CONFIG = Config()