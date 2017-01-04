import requests
from requests.auth import HTTPBasicAuth
requests.packages.urllib3.disable_warnings()


class TestRailAPI(object):
    def __init__(self, url, login, password):
        self.auth = HTTPBasicAuth(login, password)
        self.custom_header = {'Content-Type': 'application/json'}
        self.url = url + 'index.php?/api/v2/'

    def __get(self, uri):
        return requests.get(self.url + uri, auth=self.auth, headers=self.custom_header).json()

    def __post(self, uri, post_data):
        return requests.post(self.url + uri, json=post_data, auth=self.auth, headers=self.custom_header).json()

    def get_cases(self, project_id, section_id=None):
        url = 'get_cases/%s' % project_id
        if section_id is not None:
            url += '&section_id=%s' % section_id
        return self.__get(url)

    def get_section(self, section_id):
        return self.__get('get_section/%s' % section_id)

    def get_user(self, user_id):
        return self.__get('get_user/%s' % user_id)
