from faker import Faker

class   FakerLibrary:
    faker = Faker()

    def get_firstname(self):
        return self.faker.first_name()
    
    def get_lastname(self):
        return self.faker.last_name()
    
    def get_exact_length_of_numbers(self,length : int):
        return self.faker.random_number(length,fix_len=True)
    
    def get_differed_length_of_numbers(self, length : int):
        return self.faker.random_number(length,fix_len=False)
    
    def get_address(self):
        return self.faker.street_address_with_county()
    
    def get_phonenumber(self):
        return self.faker.phone_number()
    
    def get_random_message(self):
        return  self.faker.paragraph(5)
    
    def get_random_emailaddress(self):
        return self.faker.email()
    
    def get_currency_name(self):
        return self.faker.currency_name()
    
    def get_currency_symbol(self):
        return self.faker.currency_symbol()
    
    def get_current_year(self):
        return self.faker.year()