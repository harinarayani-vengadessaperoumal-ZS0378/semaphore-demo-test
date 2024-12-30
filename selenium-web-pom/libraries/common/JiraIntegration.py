import xml.etree.ElementTree as ET
from jira import JIRA
import json
import os
from pathlib import Path
from collections import defaultdict
from Secure import Secure
from PropertiesFileReader import PropertiesFileReader

class   JiraIntegration:

    def __init__(self, config_file):
        """Initializes jira with configuration details"""
        try:
            # Load JIRA configuration
            decrypted_jira_api_token = Secure.decrypt_password(PropertiesFileReader.get_value_from_properties_file("jira_encrypted_api_token",config_file),PropertiesFileReader.get_value_from_properties_file("privatekey",config_file))

            self.jira = JIRA(
                server= PropertiesFileReader.get_value_from_properties_file("jira_url",config_file),
                basic_auth=(PropertiesFileReader.get_value_from_properties_file("jira_username",config_file), decrypted_jira_api_token)
            )
            self.project_key = PropertiesFileReader.get_value_from_properties_file("jira_projectkey",config_file)
            self.jira_url = PropertiesFileReader.get_value_from_properties_file("jira_url",config_file)
        except Exception as ex:
            raise ex

    def issue_exists(self, summary):
        """Verifies if summary of the issue exists in JIRA tool"""
        try:
            jql = f'summary ~ "{summary}" AND project = "{self.project_key}" AND issuetype = "Bug"'
            issues = self.jira.search_issues(jql)
            return len(issues) > 0
        except Exception as e:
            print(f"Error searching for issues: {e}")
            return False

    def create_issue(self, summary, description, issue_type="Bug"):
        """Creates a new issue if no duplicate issue is found"""
        try:
            if self.issue_exists(summary):
                print(f"Issue with summary '{summary}' already exists. Skipping creation.")
                return None
            # Create a new JIRA issue
            issue = self.jira.create_issue(
                project=self.project_key,
                summary=summary,
                description=description,
                issuetype={"name": issue_type},
            )
            return issue.key
        except Exception as e:
            print(f"Error in creating issue: {e}")
            raise e

    def add_attachment(self, issue_key, file_path):
        # Attach a file to the issue
        try : 
            if os.path.exists(file_path):
                self.jira.add_attachment(issue=issue_key, attachment=file_path)
            else:
                print(f"Error in attaching file in Jira : Filename '{file_path}' does not exists.")
                raise FileNotFoundError
        except Exception as err:
            print(f"Error in adding attachment to JIRA: {err}")
            raise err
    
    def fetch_issues(self, jql_query):
        """
        Fetch issues from JIRA based on JQL query.
        """
        issues = self.jira.search_issues(jql_query, maxResults=1000)  # Adjust maxResults if needed
        return issues

    def delete_issue(self, issue_key):
        """
        Delete an issue from JIRA by its key.
        """
        try:
            issue_url = self.jira_url+"rest/api/2/issue/"+issue_key
            response = self.jira._session.delete(issue_url)
            # Check for success
            if response.status_code == 204:  # HTTP 204 No Content indicates success
                print(f"Issue {issue_key} deleted successfully.")
            else:
                print(f"Failed to delete issue {issue_key}: {response.status_code} {response.text}")

        except Exception as e:
            print(f"Failed to delete issue {issue_key}: {e}")

    def remove_duplicate_bugs(self):
        """
        Identify and delete duplicate bugs in the project.
        """
        try:
            # Fetch all bug issues in the project
            jql_query = f'project = "{self.project_key}" AND issuetype = "Bug"'
            issues = self.fetch_issues(jql_query)

            # Dictionary to track unique issues by summary
            unique_issues = defaultdict(list)

            # Group issues by summary
            for issue in issues:
                unique_issues[issue.fields.summary].append(issue)

            # Identify and delete duplicates
            for summary, issue_list in unique_issues.items():
                if len(issue_list) > 1:
                    # Keep the first issue and delete the rest
                    print(f"Duplicate issues found for summary: {summary}")
                    for duplicate in issue_list[1:]:
                        self.delete_issue(duplicate.key)
        except Exception as ex:
            raise ex

    def get_test_steps(self, output_file, test_name):
        """Function to extract UI test steps from Robot Framework output.xml"""
        try:
            if os.path.exists(output_file):
                tree = ET.parse(output_file)
                root = tree.getroot()
                steps = []
                for test in root.iter("test"):
                    if test.get("name") == test_name:
                        for kw in test.iter("kw"):
                            library = kw.get("library")
                            if library and library.strip().lower() in {"setup", "basepage", "builtin", "collections", "jsonlibrary"}:
                                continue
                            step_name = kw.get("name")
                            if step_name:
                                if kw.get("name") == "GetJSONValue":
                                    # Find all <arg> tags under this <kw>
                                    args = kw.findall("arg")
                                    if args:
                                        steps.append(step_name+"\t"+args[0].text)
                                else: 
                                    steps.append(step_name)
                steps = "\n".join(f"- {step}" for step in steps)
                return steps
            else:
                print(f"Error in extracting UI test steps from output.xml file : Filename '{output_file}' does not exists.")
                raise FileNotFoundError
        except Exception as ex:
            raise ex
    
    def update_bug_description(self, issue_key, test_steps):
        """Updates the bug description using given test steps"""
        description = "Test Steps:\n\n" + test_steps
        try:
            issue = self.jira.issue(issue_key)
            issue.update(fields={"description": description})
            print(f"Updated description for issue {issue_key}.")
        except Exception as e:
            print(f"Failed to update description for issue {issue_key}: {e}")
    
    def extract_http_details(self,output_file):
        """Retrieves the request and response details from the API output.xml file 
        to log them in the bug description
        """
        try:
            if os.path.exists(output_file):
                tree = ET.parse(output_file)
                root = tree.getroot()
                http_details = {}
                methods = ['GET', 'POST', 'PUT', 'DELETE', 'PATCH']

                for method in methods:
                    for kw in root.iter("kw"):
                        if kw.get("name") == method:
                            request_endpoint = None
                            request_body = None
                            response_body = None
                            statuscode = None

                            for msg in kw.findall("msg"):
                                if f"{method} Request" in msg.text:
                                    request_details = msg.text.split("\n")
                                    #print(f"Request details : {request_details}")
                                    for detail in request_details:
                                        if "url=" in detail and "path_url=" not in detail:
                                            request_endpoint = detail.split("url=")[1].strip()
                                        if "body=" in detail:
                                            request_body = detail.split("body=")[1].strip()
                                if f"{method} Response" in msg.text:
                                    response_details = msg.text.split("\n")
                                    #print(f"Response details : {response_details}")
                                    for response in response_details:
                                        if "body=" in response:
                                            response_body = response.split("body=")[1].strip()
                                        if "status=" in response:
                                            statuscode = response.split("status=")[1].strip(",reason=")

                            if request_endpoint or response_details:
                                http_details[method] = {
                                    "endpoint": request_endpoint,
                                    "body": request_body,
                                    "response": response_body,
                                    "response_statuscode": statuscode
                                }
                return http_details
            else:
                print(f"Error in extracting API details from output.xml file: Filename '{output_file}' does not exists.")
                raise FileNotFoundError
        except Exception as ex:
            raise ex

    def format_http_details(self,http_details):
        """Formats the request and response details"""
        description = []
        try:
            for method, details in http_details.items():
                description.append(f"**HTTP Method: {method}**")
                description.append(f"**Request Endpoint:** {details['endpoint']}")
                description.append(f"**Request Body:** {details['body']}")
                description.append(f"**Response:** {details['response']}")
                description.append(f"**Response Statuscode:** {details['response_statuscode']}")
                description.append("")
            return "\n".join(description).encode("utf-8").decode("utf-8").strip()
        except Exception as ex:
            raise ex

def parse_robot_output(output_file):
    """ Parse Robot Framework's output.xml"""
    try:
        if os.path.exists(output_file):
            tree = ET.parse(output_file)
            root = tree.getroot()

            test_results = []
            for suite in root.findall(".//suite"):
                for test in suite.findall("test"):
                    test_name = test.get("name")
                    test_status = test.find("status").get("status")
                    test_results.append((test_name, test_status))
            return test_results
        else:
            print(f"Error in parsing output.xml file: Filename '{output_file}' does not exists.")
            raise FileNotFoundError
    except Exception as ex:
        raise ex

def create_bugs_if_exists(jira : object, robot_output_file : str):
    """Creates API and UI bugs in JIRA tool if any tests from output.xml file is failed"""
    try:
        if os.path.exists(robot_output_file):
            # Parse test results
            test_results = parse_robot_output(robot_output_file)

            count=0
            # Log failed test cases to JIRA
            for test_name, test_status in test_results:
                if test_status.lower() == "fail":
                    summary = f"{test_name}"
                    description = f"The test case '{test_name}' failed. Check attached logs for details."
                    issue_key = jira.create_issue(summary, description)
                    if robot_output_file.find("selenium-api")!= -1:
                        http_details = jira.extract_http_details(robot_output_file)
                        if http_details:
                            test_steps = jira.format_http_details(http_details)
                            print(f"Formatted API description steps : {test_steps}")
                        else:
                            test_steps = "No HTTP details found."
                    else:
                        test_steps = jira.get_test_steps(robot_output_file, test_name)
                    
                    if issue_key is None or issue_key == "":
                        count = 0
                    else:
                        print(f"JIRA issue created: {issue_key}")
                        jira.add_attachment(issue_key, robot_output_file)   # Optionally attach logs or output.xml to the issue
                        if test_steps:
                            jira.update_bug_description(issue_key, test_steps)
                        else:
                            print(f"No step definitions are found for test case: {test_name}")
                        count= count+1
            if count == 0:
                print(f'No new issues are created.')
        else:
            print(f"Error in creating bug in Jira : Filename '{robot_output_file}' does not exists.")
            raise FileNotFoundError
    except Exception as ex:
        raise ex

def main():
    # Configuration file for JIRA
    jira_config = os.path.join(os.path.abspath(Path(__file__).parent.parent.parent), 'data', 'common_config.properties')

    # Path to Robot Framework's UI output.xml
    ui_output_file = os.path.join(os.path.abspath(Path(__file__).parent.parent.parent),'test-results','output.xml')

    # Path to Robot Framework's API output.xml
    api_output_file = os.path.join(os.path.abspath(Path(__file__).parent.parent.parent.parent),'selenium-api','test-results','output.xml')

    # Initialize JIRA integration
    jira = JiraIntegration(jira_config)
    create_bugs_if_exists(jira,ui_output_file)
    create_bugs_if_exists(jira,api_output_file)
    jira.remove_duplicate_bugs()

if __name__ == "__main__":
    main()
