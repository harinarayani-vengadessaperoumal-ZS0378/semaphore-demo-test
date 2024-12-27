import json
import re
from faker import Faker
import random
import jsonschema
import jsonschema.validators
import requests
import random

class   BookingApi:

    faker_ = Faker()

#   Reads data from JSON file and returns it
    def read_jsondata(self,key,json_file_path):
        try:
            print(f'TestData is read from \'{json_file_path}\' file')
            with open(json_file_path, 'r') as file:
                data = json.load(file)
            value = data.get(key)
            print(value)
            if value == None:
                raise ValueError(f'"{key}" Key is not found in the "{json_file_path}" file')
            else:
                return value

        except FileNotFoundError:
            print(f"Error: The file '{json_file_path}' was not found.")
            return None

        except json.JSONDecodeError:
            print(f"Error: The file '{json_file_path}' is not a valid JSON.")
            return None

        except OSError as e:
            print(f"Error: An I/O error occurred: {e}")
            return None

        except TypeError:
            print("Error: Invalid file path provided. It must be a string.")
            return None
        
        except Exception as err:
            print(f'Error occured in read_jsondata method: {repr(err)}')
            return None
        
#   Validates the create token response from Booking API
    def validate_createtoken_response(self,response):
        try:
            # Parse the response if it's a JSON string
            if isinstance(response, str):
                response = json.loads(response)
            
            # Check for the presence of the 'token' key
            if 'token' in response.json():
                token_value = response.json()['token']
                if re.match(r'^[a-zA-Z0-9]+$', token_value):
                    print('Token is found in the actual response.')
                    print(response.json())
                    return True
                else:
                    print(f"Token '{token_value}' is not alphanumeric.")
                    print("Actual response found : ",response.json())
                    return False
            else:
                print("'Token' key is not found in the response.")
                print("Actual response found : ",response.json())
                return False
                
        except json.JSONDecodeError:
            print("Invalid JSON format")
            return False
        
#   Generates new JSON request to create booking details using Faker Library
    def generate_createbookingdetails_request(self):
        try:
            request_body = {
            "firstname": str(self.faker_.first_name()),
            "lastname": str(self.faker_.last_name()),
            "totalprice": random.randint(100, 500),
            "depositpaid": random.choice([True, False]),
            "bookingdates": {
                "checkin": str(self.faker_.date_between(start_date='-1y', end_date='today').isoformat()),
                "checkout": str(self.faker_.date_between(start_date='today', end_date='+1y').isoformat())
            },
            "additionalneeds": str(self.faker_.sentence(nb_words=3))
            }
            return request_body
        except Exception as err:
            print(f'Error occured in generate_createbookingdetails_request method: {repr(err)}')

#   Validates the create booking details response from booking API
    def validate_createbookingdetails_response(self,expected_request_body, response):
        try:
            if 'bookingid' not in response.json():
                return False, "'bookingid' property is missing in the response"
            
            # Extract booking details from the response
            booking_details = response.json()['booking']
            
            result = self.validate_booking_details_response(expected_request_body,booking_details)
            return result
        except Exception as err:
            print(f'Error occured in validate_createbookingdetails_response method: {repr(err)}')
    
#   Validates the Update booking details response values from booking API 
    def validate_update_booking_details_response(self,expected_request_body, response ):
        try:
            booking_details = response.json()
            result = self.validate_booking_details_response(expected_request_body,booking_details)
            return result
        except Exception as err:
            print(f'Error occured in validate_update_booking_details_response method: {repr(err)}')
    

    def validate_booking_details_response(self, expected_request_body, booking_details):
        try:
            # Validate each property
            for key in expected_request_body:
                if key != 'bookingdates':  # Handle bookingdates separately
                    if key not in booking_details:
                        print(f"'{key}' property key is not found in the response.")
                        return False
                    if expected_request_body[key] != booking_details[key]:
                        print(f"Mismatch for {key}: expected {expected_request_body[key]}, got {booking_details[key]}")
                        return False
                    else:
                        print(f"Matched {key} property - Expected : '{expected_request_body[key]}' , Actual : '{booking_details[key]}'")
            
            # Validate bookingdates separately
            for key in expected_request_body['bookingdates']:
                if str(expected_request_body['bookingdates'][key]).replace("\"","") != str(booking_details['bookingdates'][key]).replace("\"",""):
                    print(f"Mismatch for bookingdates.{key}: expected {expected_request_body['bookingdates'][key]}, got {booking_details['bookingdates'][key]}")
                    return False
                else:
                    print(f"Matched {key} property - Expected : '{expected_request_body['bookingdates'][key]}' , Actual : '{booking_details['bookingdates'][key]}'")
            
            return True
        except Exception as err:
            print(f'Error occured in validate_booking_details_response method: {repr(err)}')

#   Returns the property value from the response
    def get_property_value_from_response(self, response, propertykey : str):
        try:
            if response.json() is not None:
                if propertykey in response.json():
                    propertyvalue = response.json()[propertykey]
                    if propertykey == 'token':
                        return "token="+propertyvalue
                    else:
                        return propertyvalue
                else:
                    raise Exception(f'propertyKey "{propertykey}" is not found in the response.')    
            else:
                raise ValueError('Response has no content.')          
        
        except ValueError as valError:
            print('Error in get_property_value_from_response method : '+repr(valError))
        except Exception as error:
            print('Error in get_property_value_from_response method : '+repr(error))

#   Generates the JSON request for Updating booking details using Faker Library
    def generate_updateallbookingdetails_request(self):
        try:
            request_body = {
            "firstname": f'{self.faker_.first_name()}',
            "lastname": f'{self.faker_.last_name()}',
            "totalprice": random.randint(500, 5000),
            "depositpaid": random.choice([True, False]),
            "bookingdates": {
                "checkin": f'"{self.faker_.date_between(start_date='-1y', end_date='today').isoformat()}"',
                "checkout": f'"{self.faker_.date_between(start_date='today', end_date='+1y').isoformat()}"'
            },
            "additionalneeds": f'{self.faker_.sentence(nb_words=5)}'
            }
            return request_body
        except Exception as err:
            print(f'Error occured in generate_updateallbookingdetails_request method: {repr(err)}')
    
#   Update the values of specific property in the given API's request
    def update_booking_details_of_specific_property(self,propertykey, requestbody):
        try:
            propertyvalue = None
            match propertykey:
                case 'firstname': 
                    propertyvalue = self.faker_.first_name(),
                case 'lastname': 
                    propertyvalue = self.faker_.last_name(),
                case 'totalprice':
                    propertyvalue= random.randint(500, 5000)
                case 'depositpaid':
                    propertyvalue= random.choice([True, False])
                case 'bookingdates.checkin':
                    propertyvalue= self.faker_.date_between(start_date='-1y', end_date='today').isoformat()
                case 'bookingdates.checkout':
                    propertyvalue = self.faker_.date_between(start_date='today', end_date='+1y').isoformat()
                case 'additionalneeds':
                    propertyvalue = self.faker_.sentence(nb_words=5)
                case default :
                    raise AssertionError(f'{propertykey} is not valid. Try again with valid propertykey.')
            
            requestbody[propertykey] = propertyvalue
            return requestbody
        
        except Exception as err:
            print(f'Error occured in update_booking_details_of_specific_property method: {repr(err)}')

    def update_json_data(self,propertyname_to_update,propertyvalue_to_update,jsonbody):
        try:
            if propertyname_to_update is None:
                raise AttributeError('The argument "propertyname_to_update" is required.')
            if propertyvalue_to_update is None:
                raise AttributeError('The argument "propertyvalue_to_update" is required.')
            
            if isinstance(jsonbody, str):
                jsonbody = json.loads(jsonbody)
        
            # Update the JSON object
            jsonbody[propertyname_to_update] = propertyvalue_to_update
            return jsonbody
            
        except AttributeError as attrErr:
            print(repr(attrErr))
        except (jsonschema.ValidationError, jsonschema.SchemaError) as jsonErr:
            print(repr(jsonErr))

    def validate_json_schema(self,input_json, reference_schema_path, schema_key):
        try:
            with open(reference_schema_path) as json_file:
                schemas = json.load(json_file)

            if schema_key not in schemas:
                raise ValueError(f"Schema with key '{schema_key}' not found in the 'API_Schema.json' reference file.")

            reference_schema = schemas[schema_key]
            jsonschema.validate(instance=input_json, schema=reference_schema)
            print(f'Schema Validation is successfull.\nExpected schema :\n{reference_schema}\nActual response :\n{input_json}')
            return True
        
        except jsonschema.ValidationError as valError:
            print(f'Error occured in validate_json_schema method: Schema validation is failed. {valError.message} but received the response as {input_json}')
        except Exception as err:
            print(f'Error occured in validate_json_schema method: {repr(err)}')
            return False
    
    def validate_get_all_booking_id_response(self, response):
        try:
            bookingids=[]
            bookingid_response = response.json()
            for bookingid in bookingid_response:
                bookingids.append(bookingid['bookingid'])
            
            if len(bookingids) >0:
                print(f'Found {len(bookingids)} records of booking.\nList of Booking IDs : \n{bookingids}') 
                return True           
            else:
                raise ValueError('No records of booking is found.')
        
        except ValueError as valerr:
            print(f'Error in validate_get_all_booking_id_response method : {repr(valerr)}')
        except Exception as err:
            print(f'Error in validate_get_all_booking_id_response method : {repr(err)}')

    def validate_delete_bookingdetails_response(self, response):
        try:
            delete_response : str = response.json()
            expected_response = "created"
            if delete_response.lower() == expected_response:
                print(f'Delete booking details response validation is Successfull.\n{response.json()}')
            else:
                raise Exception(f'Delete booking details response validation is unsuccessfull.\n{response.json()}')
        except Exception as err:
            print(f'Error occured in validate_delete_bookingdetails_response method: {repr(err)}')
        
    def delete_all_booking_details(self, get_allbookingdetails_response):
        try:
            bookingids=[]
            url = "https://restful-booker.herokuapp.com/booking/"
            bookingid_response = get_allbookingdetails_response.json()
            for bookingid in bookingid_response:
                bookingids.append(bookingid['bookingid'])

            # Delete bookings while bookingIds has more than 10 entries
            while len(bookingids) > 10:
                # Use a copy of the list to avoid modifying it while iterating
                for booking_id in bookingids[:]:
                    delete_url = url + str(booking_id)
                    response = requests.delete(delete_url)
                    if response.status_code == 201:  # Assuming 201 indicates successful deletion
                        print(f'Deleted booking ID: {booking_id}')
                        bookingids.remove(booking_id)
                    else:
                        print(f'Failed to delete booking ID: {booking_id}, Status Code: {response.status_code}')
                    
                    # Exit the loop once we have fewer than or equal to 10 bookings
                    if len(bookingids) <= 10:
                        break
        except Exception as err:
            print(f'Error occured in delete_all_booking_details method: {repr(err)}')