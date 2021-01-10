"X-road client example with JSON"
import requests
import pprint
import base64

class JsonClient:
    """Client class for using services.
    For each service here is a method which composes input message,
    calls the method and returns response data.
    """
    def __init__(self, xroad_client, server_url, userid=None, issue=None):
        self.xroad_client = xroad_client
        self.server_url = server_url
        self.userid = userid
        self.issue = issue
        
    def _args(self):
        headers = {'Content-Type': 'application/json; charset=utf-8',
                   'X-Road-Client': self.xroad_client,
                   }
        if self.userid:
            headers['X-Road-Userid'] = self.userid
        if self.issue:
            headers['X-Road-Issue'] = self.issue
        timeout = (5,20)
        args = {'headers': headers,
                'timeout': timeout,
                }
        return args

    def list_persons(self, givenname=None, surname=None, personcode=None):
        args = self._args()
        url = f'{self.server_url}/persons'
        print(f'\nSearch persons, GET {url}')
        params = {'givenname': givenname,
                  'surname': surname,
                  'personcode': personcode,
                  }
        return requests.get(url, params=params, **args)

    def get_person(self, code):
        args = self._args()
        url = f'{self.server_url}/person/{code}'
        print(f'\nGet person data, GET {url}')        
        return requests.get(url, **args)
        
    def put_photo(self, code, img):
        args = self._args()
        url = f'{self.server_url}/person/{code}/photo'
        print(f'\nUpload new photo, PUT {url}')                
        imgdata = base64.b64encode(img).decode('ascii')
        data = {'photo': imgdata}
        return requests.put(url, json=data, **args)

def show_response(response):
    try:
        json_data = response.json()
    except:
        print('Error - response is not JSON')
        print(response.text)
    else:
        print('Response received:')
        pprint.pprint(json_data)
        return json_data

def run_client():
    # security server URL
    security_server = 'http://1.2.3.4' # REPLACE WITH YOUR DATA
    json_protocol = 'r1'
    serviceid = 'roksnet-dev/COM/12998179/roksnet-producer' # REPLACE WITH YOUR DATA

    # normal URL (security server)
    url = f'{security_server}/{json_protocol}/{serviceid}'

    # local URL (without using security server, for testing only)
    url = 'http://localhost:6543/services'
    
    # X-Road-Client header value as xRoadInstance/memberClass/memberCode/subsystemCode    
    xroad_client = 'roksnet-dev/COM/12998179/roksnet-consumer'

    # X-Road-Userid header value as country code + person code
    userid = 'EE30101010007' # REPLACE WITH AUTHENTICATED USER ID

    # Service client
    reg = JsonClient(xroad_client, url, userid=userid)

    # Get list of persons
    response = reg.list_persons(surname='H%')
    data = show_response(response)
    try:
        # get first person's code
        person = data['items'][0]
        code = person['personcode']
    except:
        print('Persons list query did not succeed')
        return

    # Get data of a person
    response = reg.get_person(code)
    data = show_response(response)
    imgdata = data.get('photo')
    if imgdata:
        img = base64.b64decode(imgdata)
        with open('tmp.jpg', 'wb') as f:
            f.write(img)

    # Replace photo of the person
    fn = 'json_populationdb/scripts/init_photo2.jpg'
    with open(fn, 'rb') as f:
        img = f.read()
        response = reg.put_photo(code, img)
        show_response(response)
    
if __name__ == '__main__':
    run_client()

