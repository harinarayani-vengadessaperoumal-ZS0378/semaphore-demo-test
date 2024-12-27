import json

class   CommonUtilities:
    
    def load_json(self, file_path):
        with open(file_path, 'r') as file:
            return json.load(file)

    def get_testdata(self, file_path, testcase_id, testdatakey):
        data = self.load_json(file_path)
        try:
            return data[testcase_id]["testData"][testdatakey]
        except KeyError:
            print(f"KeyError: Could not find '{testcase_id}' or '{testdatakey}' in test data.")

    def get_verificationdata(self, file_path, testcase_id, verificationkey):
        data = self.load_json(file_path)
        try:
            return data[testcase_id]["verificationData"][verificationkey]
        except KeyError:
            print(f"KeyError: Could not find '{testcase_id}' or '{verificationkey}' in verification data.")
            return None