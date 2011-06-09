from datetime import datetime
import time 

from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import db

### MODELS ###

class Event(db.Model):
    url = db.StringProperty(required=True)
    when = db.DateTimeProperty(required=True)
    name = db.StringProperty(required=True)
    description = db.StringProperty(multiline=True)


### REQUEST HANDLERS ###

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        
        self.response.out.write(template.render('templates/index.html', {}))

class CreateHandler(webapp.RequestHandler):
    def get(self):
        self.redirect('/', permanent=True)

    def post(self):
        when = datetime.fromtimestamp(float(self.request.get('when')))
        name = self.request.get('name')
        description = self.request.get('description')
        url = '1234' # TODO

        event = Event(url=url, when=when, name=name, description=description)
        event.put()

        self.response.out.write('"%s" written to db.\n' % name)

class EventHandler(webapp.RequestHandler):
    def get(self, url):
        self.response.headers['Content-Type'] = 'text/html'
        
        self.response.out.write(template.render('templates/event.html', {'event': {'name':'foobar', 'time':'', 'url':url}}))
        

### APP HANDLER ###

application = webapp.WSGIApplication([('/', MainPage),
                                      ('/create', CreateHandler),
                                      ('/e/(.*)', EventHandler),
                                     ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
