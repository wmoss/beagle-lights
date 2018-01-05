import webapp2
import json
import logging


class RequestHandler(webapp2.RequestHandler):
    def post(self):
        logging.info('Body: ' + repr(self.request.body))
        logging.info('Headers: ' + repr(self.request.headers))

        response = {
            'speech': 'Done.',
            'displayText': 'Done.',
        }

        self.response.headers['Content-Type'] = 'application/json'
        self.response.write(json.dumps(response))


app = webapp2.WSGIApplication([
    ('/v1/request', RequestHandler),
], debug=True)
