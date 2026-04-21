from config.settings import *

def get_auth_url():
    return f"{ZOHO_AUTH_URL}?scope=ZohoProjects.portals.READ,ZohoProjects.projects.ALL,ZohoProjects.tasks.ALL,ZohoProjects.users.READ&client_id={ZOHO_CLIENT_ID}&response_type=code&access_type=offline&prompt=consent&redirect_uri={ZOHO_REDIRECT_URI}"