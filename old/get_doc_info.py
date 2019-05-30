import onshape_client
from pprint import pprint

# Initialize the configuration with your credentials
configuration = onshape_client.Configuration()
configuration.api_key['ACCESS_KEY'] = '<YOUR_API_ACCESS_KEY>'
configuration.api_key['SECRET_KEY'] = '<YOUR_API_SECRET_KEY>'

# Initialize the documents API with the configuration
doc_instance = onshape_client.DocumentsApi(onshape_client.ApiClient(configuration=configuration))

# Call and print the results of the get Documents endpoint synchronously
api_response = doc_instance.get_documents()
pprint(api_response)

# Call and print the results of the get Documents endpoint asynchronously
thread = doc_instance.get_documents(async=True)
result = thread.get()
