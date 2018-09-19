from http.server import BaseHTTPRequestHandler, HTTPServer
from cgi import parse_header, parse_multipart
from urllib.parse import parse_qs
import json
from hashlib import sha1
import hmac



# HTTPRequestHandler class
class extendedHTTPRequestHandler(BaseHTTPRequestHandler):

    def _set_headers(self,content_type):
        self.send_response(200)
        self.send_header('Content-type', content_type)
        self.send_header('Access-Control-Allow-Headers','Content-Type')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.end_headers()

    def do_OPTIONS(self):
        print ('hitting options')
        self.send_response(200, "ok")
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header("Access-Control-Allow-Headers", "X-Requested-With")


        # GET
    def do_GET(self):
        print ('hitting get')
        # Send headers
        self._set_headers('text/html')

        # The URL construct only accepts POST requests
        message = "No get requests to this URL please !!!!"
        self.wfile.write(bytes(message, "utf8"))
        return

    # POST
    def do_POST(self):
        print ('hitting post')
        post_request_variables = self.parse_POST()
        self._set_headers('application/json')

        for key in post_request_variables.keys():
            print ("keys  ",key)

        constructed_url = self.getUrl(post_request_variables["baseUrl"][0], post_request_variables["request"][0])

        # create a dict and convert is as a JSON and send it back
        print ("url created ", constructed_url)
        data = {'url': constructed_url}
        self.wfile.write(bytes(json.dumps(data), "utf8"))
        return

    def getUrl(self,baseURL, request):

        dev_id = 3000462
        key = '7416c1ad-4d13-4f02-8a49-aefcddfdd1d7'
        request = request + ('&' if ('?' in request) else '?')
        raw = request + 'devid={0}'.format(dev_id)
        hashed = hmac.new(bytes(key, 'latin-1'), bytes(raw, 'latin-1'), sha1)
        signature = hashed.hexdigest()
        return baseURL + raw + '&signature={1}'.format(dev_id, signature)

    def parse_POST(self):
        ctype, pdict = parse_header(self.headers['content-type'])
        if ctype == 'multipart/form-data':
            post_values = parse_multipart(self.rfile, pdict)
        elif ctype == 'application/x-www-form-urlencoded':
            length = int(self.headers['content-length'])
            post_values = parse_qs(self.rfile.read(length).decode("utf8"), keep_blank_values = 1)
        else:
            post_values = {}
        return post_values


def run():
    print('starting server...')

    #set URL and and appropriate Port
    address = ('127.0.0.1', 8081)
    httpd = HTTPServer(address, extendedHTTPRequestHandler)
    print('running server...')
    httpd.serve_forever()


run()

# References / code lifted off from :-)
#1. http://joelinoff.com/blog/?p=1658
#2. https://stackoverflow.com/questions/4233218/python-how-do-i-get-key-value-pairs-from-the-basehttprequesthandler-http-post-h