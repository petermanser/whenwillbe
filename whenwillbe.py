from datetime import datetime
import time 
import random
import string

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


### HELPER FUNCTION ###

def generate_url():
    return ''.join(random.choice(string.ascii_lowercase + string.digits) for x in range(6))


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
        while 1:
            url = generate_url()
            if Event.all().filter('url =', url).count() == 0:
                break

        event = Event(url=url, when=when, name=name, description=description)
        event.put()

class EventHandler(webapp.RequestHandler):
    def get(self, url):
        self.response.headers['Content-Type'] = 'text/html'
        
        event = Event.all().filter('url =', url).get()
        if not event:
            self.error(404)
            self.response.out.write('404 not found')
        else:
            data = {'event': event}
            self.response.out.write(template.render('templates/event.html', data))
        

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
