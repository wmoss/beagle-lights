import webapp2
import json
import logging
import socket
from google.appengine.api import urlfetch


class RequestHandler(webapp2.RequestHandler):
    def post(self):
        logging.info('Body: ' + repr(self.request.body))
        logging.info('Headers: ' + repr(self.request.headers))

        result = urlfetch.fetch('http://52.119.125.163:5000/lights')
        if result.status_code == 201:
            logging.info('Successfully hit beagleboard')
        else:
            logging.error('failed to hit beagleboard, status code ' + result.status_code)

        response = {
            'speech': 'Done.',
            'displayText': 'Done.',
        }

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(response))


app = webapp2.WSGIApplication([
    ('/v1/request', RequestHandler),
], debug=True)
