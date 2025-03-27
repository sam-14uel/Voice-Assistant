from hubspot import HubSpot
from hubspot.crm.contacts import SimplePublicObjectInputForCreate, PublicObjectSearchRequest
from hubspot.crm.contacts.exceptions import ApiException
from hubspot.crm.objects import ApiException as ObjectsApiException
from hubspot.cms.audit_logs import ApiException as AuditApiException
from dateutil import parser

class HubSpotClient:
    def __init__(self, api_key="eu1-6c8b-8ca6-4144-988b-7302e4a208e6"):
        """Initialize HubSpot client with access token"""
        self.api_client = HubSpot(api_key=api_key)


# ==========================================================================================
# Contacts
# ==========================================================================================

    def create_contact(self, email):
        """
        Create a new contact in HubSpot CRM
        
        Args:
            email (str): Contact's email address
            properties (dict, optional): Additional contact properties
        
        Returns:
            API response object or None if failed
        """
        properties = {
            "name": "Emeka",
        }
        try:
            if properties is None:
                properties = {}
            properties["email"] = email
            
            contact_input = SimplePublicObjectInputForCreate(properties=properties)
            response = self.api_client.crm.contacts.basic_api.create(
                simple_public_object_input_for_create=contact_input
            )
            return response
        except ApiException as e:
            print(f"Exception when creating contact: {e}")
            return None
        
#==================================================================================================
        
    def update_contact(self, contact_id, properties):
        try:
            contact_input = SimplePublicObjectInputForCreate(properties=properties)
            response = self.api_client.crm.contacts.basic_api.update(
                contact_id, contact_input
            )
            return response
        except ApiException as e:
            print(f"Exception when updating contact: {e}")
            return None

#==================================================================================================
        
    def get_contact_by_id(self, contact_id):
        """
        Retrieve a contact by ID
        
        Args:
            contact_id (str): ID of the contact to fetch
        
        Returns:
            Contact object or None if failed
        """
        try:
            contact = self.api_client.crm.contacts.basic_api.get_by_id(contact_id)
            return contact
        except ApiException as e:
            print(f"Exception when requesting contact by id: {e}")
            return None

#==================================================================================================
   
    def get_contact_by_email(self):
        pass
    
#==================================================================================================

    def get_all_contacts(self):
        """
        Get all contacts from HubSpot CRM
       
        Returns:
            List of all contacts or None if failed
        """
        try:
            all_contacts = self.api_client.crm.contacts.get_all()
            return all_contacts
        except ApiException as e:
            print(f"Exception when getting all contacts: {e}")
            return None
        
#==================================================================================================

    def delete_contact(self, contact_id):
        try:
            response = self.api_client.crm.contacts.basic_api.archive(contact_id)
            return response
        except ApiException as e:
            print(f"Exception when deleting contact: {e}")
            return None
        


# ==========================================================================================
# Companies
# ==========================================================================================

    def create_company(self, company_name, domain):
        try:
            properties = {
                "name": company_name,
                "domain": domain
            }
            contact_input = SimplePublicObjectInputForCreate(properties=properties)
            company = self.api_client.crm.companies.basic_api.create(contact_input)
            return company
        except ApiException as e:
            print(f"Exception when creating company: {e}")
            return None

#==================================================================================================

    def update_company(self, company_id, company_name, domain):
        try:
            properties = {
                "name": company_name,
                "domain": domain
            }
            company_data_input = SimplePublicObjectInputForCreate(properties=properties)
            return self.api_client.crm.companies.basic_api.update(company_id, company_data_input)
        except ApiException as e:
            print(f"Exception when updating company: {e}")
            return None

#==================================================================================================

    def get_company_by_id(self, company_id):
        try:
            contact = self.api_client.crm.companies.basic_api.get_by_id(company_id)
            return contact
        except ApiException as e:
            print(f"Exception when requesting contact by id: {e}")
            return None

#==================================================================================================

    def get_all_companies(self):
        try:
            all_companies = self.api_client.crm.companies.get_all()
            return all_companies
        except ApiException as e:
            print(f"Exception when getting all companies: {e}")
            return None
        
#==================================================================================================

    def delete_company(self, company_id):
        try:
            response = self.api_client.crm.companies.basic_api.archive(company_id)
            return response
        except ApiException as e:
            print(f"Exception when deleting company: {e}")
            return None

# ==========================================================================================
# Deals
# ==========================================================================================

    def create_deal(self, deal_name, pipeline_id, deal_stage):
        try:
            properties = {
                "dealname": deal_name,
                "pipeline": pipeline_id,
                "dealstage": deal_stage
            }
            deal_input = SimplePublicObjectInputForCreate(properties=properties)
            return self.api_client.crm.deals.basic_api.create(deal_input)
        except ApiException as e:
            print(f"Exception when creating deal: {e}")
            return None

#==================================================================================================

    def update_deal(self, deal_id):
        try:
            updated_properties = {
                
            }
            deal_input = SimplePublicObjectInputForCreate(properties=updated_properties)
            response = self.api_client.crm.deals.basic_api.update(
                deal_id, simple_public_object_input=deal_input
            )
            return response
        except ApiException as e:
            print(f"Exception when updating deal: {e}")
            return None

#==================================================================================================

    def get_deal_by_id(self, deal_id):
        try:
            deal = self.api_client.crm.deals.basic_api.get_by_id(deal_id)
            return deal
        except ApiException as e:
            print(f"Exception when requesting deal by id: {e}")
            return None

#==================================================================================================

    def get_all_deals(self):
        try:
            response = self.api_client.crm.deals.basic_api.get_page()
            return response
        except ApiException as e:
            print(f"Exception when getting all deals: {e}")
            return None

#==================================================================================================

    def delete_deal(self, deal_id):
        try:
            response = self.api_client.crm.deals.basic_api.archive(deal_id)
            return response
        except ApiException as e:
            print(f"Exception when deleting deal: {e}")
            return None



# ==========================================================================================
# Tickets
# ==========================================================================================

    def create_ticket(self):
        try:
            properties = {

            }
            contact_input = SimplePublicObjectInputForCreate(properties=properties)
            ticket = self.api_client.crm.tickets.basic_api.create(contact_input)
            return ticket
        except ApiException as e:
            print(f"Exception when creating ticket: {e}")
            return None

#==================================================================================================

    def update_ticket(self, ticket_id):
        try:
            updated_properties = {
                
            }
            ticket_input = SimplePublicObjectInputForCreate(properties=updated_properties)
            response = self.api_client.crm.tickets.basic_api.update(
                ticket_id, simple_public_object_input=ticket_input
            )
            return response
        except ApiException as e:
            print(f"Exception when updating ticket: {e}")
            return None

#==================================================================================================

    def get_ticket_by_id(self, ticket_id):
        try:
            ticket = self.api_client.crm.tickets.basic_api.get_by_id(ticket_id)
            return ticket
        except ApiException as e:
            print(f"Exception when requesting ticket by id: {e}")
            return None

#==================================================================================================

    def get_all_tickets(self):
        try:
            response = self.api_client.crm.tickets.basic_api.get_page()
            return response
        except ApiException as e:
            print(f"Exception when getting all tickets: {e}")
            return None
        
#=================================================================================================

    def delete_ticket(self, ticket_id):
        try:
            response = self.api_client.crm.tickets.basic_api.archive(ticket_id)
            return response
        except ApiException as e:
            print(f"Exception when deleting ticket: {e}")
            return None


# ==========================================================================================
# Products
# ==========================================================================================

    def create_product(self):
        try:
            properties = {
                
            }
            contact_input = SimplePublicObjectInputForCreate(properties=properties)
            product = self.api_client.crm.companies.basic_api.create(contact_input)
            return product
        except ApiException as e:
            print(f"Exception when creating product: {e}")
            return None

#==================================================================================================

    def update_product(self, product_id):
        try:
            updated_properties = {
                
            }
            product_input = SimplePublicObjectInputForCreate(properties=updated_properties)
            response = self.api_client.crm.products.basic_api.update(
                product_id, simple_public_object_input=product_input
            )
            return response
        except ApiException as e:
            print(f"Exception when updating product: {e}")
            return None

#==================================================================================================

    def get_product_by_id(self, product_id):
        try:
            product = self.api_client.crm.products.basic_api.get_by_id(product_id)
            return product
        except ApiException as e:
            print(f"Exception when requesting product by id: {e}")
            return None

#==================================================================================================

    def get_all_products(self):
        try:
            response = self.api_client.crm.products.basic_api.get_page()
            return response
        except ApiException as e:
            print(f"Exception when getting all products: {e}")
            return None

#==================================================================================================

    def delete_product(self, product_id):
        try:
            response = self.api_client.crm.products.basic_api.archive(product_id)
            return response
        except ApiException as e:
            print(f"Exception when deleting product: {e}")
            return None
        


import requests
from django.conf import settings
#============================== HUBSPOT REST API ======================================
# CRM
def get_hubspot_token(code):
    try:
        url = f"{settings.HUBSPOT_BASE_URL}/oauth/v1/token"
        headers = {"Content-Type": "application/x-www-form-urlencoded"}
        data = {
            "grant_type": "authorization_code",
            "client_id": settings.HUBSPOT_CLIENT_ID,
            "client_secret": settings.HUBSPOT_CLIENT_SECRET,
            "redirect_uri": settings.HUBSPOT_REDIRECT_URI,
            "code": code
        }
        response = requests.post(url, headers=headers, data=data)
        return response.json().get('access_token')
    except Exception as e:
        return f"Error getting token: {str(e)}"

#====== CONTACTS ======
def create_contact(access_token, email, first_name, last_name):
    try:
        url = f"{settings.HUBSPOT_BASE_URL}/crm/v3/objects/contacts"
        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        data = {
            "properties": {
                "email": email,
                "firstname": first_name,
                "lastname": last_name
            }
        }
        response = requests.post(url, json=data, headers=headers)
        return response.json()
    except Exception as e:
        return f"Error creating contact: {str(e)}"


def update_contact(access_token, contact_id, **kwargs):
    try:
        url = f"{settings.HUBSPOT_BASE_URL}/crm/v3/objects/contacts/{contact_id}"
        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        data = {"properties": kwargs}
        response = requests.patch(url, json=data, headers=headers)
        return response.json()
    except Exception as e:
        return f"Error updating contact: {str(e)}"


def delete_contact(access_token, contact_id):
    try:
        url = f"{settings.HUBSPOT_BASE_URL}/crm/v3/objects/contacts/{contact_id}"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.delete(url, headers=headers)
        return response.status_code == 204
    except Exception as e:
        return f"Error deleting contact: {str(e)}"


def get_contact(access_token, contact_id):
    try:
        url = f"{settings.HUBSPOT_BASE_URL}/crm/v3/objects/contacts/{contact_id}"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        return f"Error getting contact: {str(e)}"


def get_all_contacts(access_token):
    pass

#====== COMPANIES ======
def create_company(access_token, name, domain, industry):
    try:
        url = f"{settings.HUBSPOT_BASE_URL}/crm/v3/objects/companies"
        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        data = {
            "properties": {
                "name": name,
                "domain": domain,
                "industry": industry
            }
        }
        response = requests.post(url, json=data, headers=headers)
        return response.json()
    except Exception as e:
        return f"Error creating company: {str(e)}"


def update_company(access_token, company_id, **kwargs):
    try:
        url = f"{settings.HUBSPOT_BASE_URL}/crm/v3/objects/companies/{company_id}"
        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        data = {"properties": kwargs}
        response = requests.patch(url, json=data, headers=headers)
        return response.json()
    except Exception as e:
        return f"Error updating company: {str(e)}"


def delete_company(access_token, company_id):
    try:
        url = f"{settings.HUBSPOT_BASE_URL}/crm/v3/objects/companies/{company_id}"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.delete(url, headers=headers)
        return response.status_code == 204
    except Exception as e:
        return f"Error deleting company: {str(e)}"


def get_company(access_token, company_id):
    try:
        url = f"{settings.HUBSPOT_BASE_URL}/crm/v3/objects/companies/{company_id}"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        return f"Error getting company: {str(e)}"

#====== DEALS ========
def create_deal(access_token, dealname, amount, pipeline, stage):
    try:
        url = f"{settings.HUBSPOT_BASE_URL}/crm/v3/objects/deals"
        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        data = {
            "properties": {
                "dealname": dealname,
                "amount": amount,
                "pipeline": pipeline,
                "dealstage": stage
            }
        }
        response = requests.post(url, json=data, headers=headers)
        return response.json()
    except Exception as e:
        return f"Error creating deal: {str(e)}"


def update_deal(access_token, deal_id, **kwargs):
    try:
        url = f"{settings.HUBSPOT_BASE_URL}/crm/v3/objects/deals/{deal_id}"
        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        data = {"properties": kwargs}
        response = requests.patch(url, json=data, headers=headers)
        return response.json()
    except Exception as e:
        return f"Error updating deal: {str(e)}"


def delete_deal(access_token, deal_id):
    try:
        url = f"{settings.HUBSPOT_BASE_URL}/crm/v3/objects/deals/{deal_id}"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.delete(url, headers=headers)
        return response.status_code == 204
    except Exception as e:
        return f"Error deleting deal: {str(e)}"


def get_deal(access_token, deal_id):
    try:
        url = f"{settings.HUBSPOT_BASE_URL}/crm/v3/objects/deals/{deal_id}"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        return f"Error getting deal: {str(e)}"


def get_all_deals(access_token):
    pass

#====== PRODUCTS ======
def create_product(access_token, name, price):
    try:
        url = f"{settings.HUBSPOT_BASE_URL}/crm/v3/objects/products"
        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        data = {
            "properties": {
                "name": name,
                "price": price
            }
        }
        response = requests.post(url, json=data, headers=headers)
        return response.json()
    except Exception as e:
        return f"Error creating product: {str(e)}"


def update_product(access_token, product_id, **kwargs):
    try:
        url = f"{settings.HUBSPOT_BASE_URL}/crm/v3/objects/products/{product_id}"
        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        data = {"properties": kwargs}
        response = requests.patch(url, json=data, headers=headers)
        return response.json()
    except Exception as e:
        return f"Error updating product: {str(e)}"


def delete_product(access_token, product_id):
    try:
        url = f"{settings.HUBSPOT_BASE_URL}/crm/v3/objects/products/{product_id}"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.delete(url, headers=headers)
        return response.status_code == 204
    except Exception as e:
        return f"Error deleting product: {str(e)}"


def get_product(access_token, product_id):
    try:
        url = f"{settings.HUBSPOT_BASE_URL}/crm/v3/objects/products/{product_id}"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        return f"Error getting product: {str(e)}"
    

def get_all_products(access_token):
    pass
    
#====== TICKETS ======
def create_ticket(access_token, subject, content, pipeline, status):
    try:
        url = f"{settings.HUBSPOT_BASE_URL}/crm/v3/objects/tickets"
        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        data = {
            "properties": {
                "subject": subject,
                "content": content,
                "pipeline": pipeline,
                "hs_pipeline": pipeline,
                "hs_pipelineStage": status
            }
        }
        response = requests.post(url, json=data, headers=headers)
        return response.json()
    except Exception as e:
        return f"Error creating ticket: {str(e)}"



def update_ticket(access_token, ticket_id, **kwargs):
    try:
        url = f"{settings.HUBSPOT_BASE_URL}/crm/v3/objects/tickets/{ticket_id}"
        headers = {"Authorization": f"Bearer {access_token}", "Content-Type": "application/json"}
        data = {"properties": kwargs}
        response = requests.patch(url, json=data, headers=headers)
        return response.json()
    except Exception as e:
        return f"Error updating ticket: {str(e)}"


def delete_ticket(access_token, ticket_id):
    try:
        url = f"{settings.HUBSPOT_BASE_URL}/crm/v3/objects/tickets/{ticket_id}"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.delete(url, headers=headers)
        return response.status_code == 204
    except Exception as e:
        return f"Error deleting ticket: {str(e)}"


def get_ticket(access_token, ticket_id):
    try:
        url = f"{settings.HUBSPOT_BASE_URL}/crm/v3/objects/tickets/{ticket_id}"
        headers = {"Authorization": f"Bearer {access_token}"}
        response = requests.get(url, headers=headers)
        return response.json()
    except Exception as e:
        return f"Error getting ticket: {str(e)}"
    

def get_all_tickets(access_token):
    pass