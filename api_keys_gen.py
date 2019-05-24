from __future__ import print_function
import time
import onshape_client
from onshape_client.rest import ApiException
from pprint import pprint

# Configure OAuth2 access token for authorization: OAuth2
configuration = onshape_client.Configuration()
configuration.access_token = 'OjhR9bjlePxL3lwoVGQNkJRD'

# create an instance of the API class
api_instance = onshape_client.AccountsApi(onshape_client.ApiClient(configuration))
aid = 'aid_example' # str | 
pid = 'pid_example' # str | 
cancel_immediately = False # bool |  (optional) (default to False)

try:
    # Cancel Recurring Subscription
    api_instance.cancel_purchase_new(aid, pid, cancel_immediately=cancel_immediately)
except ApiException as e:
    print("Exception when calling AccountsApi->cancel_purchase_new: %s\n" % e)
