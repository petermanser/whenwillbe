from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template
from google.appengine.ext import db

### MODELS ###

class Event(db.Model):
    url = db.StringProperty(required=True)
    time = db.DateProperty(required=True)
    name = db.StringProperty(required=True)
    description = db.StringProperty(multiline=True)


### REQUEST HANDLERS ###

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        
        self.response.out.write(template.render('templates/index.html', {}))

class Create(webapp.RequestHandler):
    def get(self):
        self.redirect('/', permanent=True)

    def post(self):
        self.response.out.write('fuck you!\n')

class Event(webapp.RequestHandler):
    def get(self, url):
        self.response.headers['Content-Type'] = 'text/html'
        
        self.response.out.write(template.render('templates/event.html', {'event': {'name':'foobar', 'time':'', 'url':url}}))
        

### APP HANDLER ###

application = webapp.WSGIApplication([('/', MainPage),
                                      ('/create', Create),
                                      ('/e/(.*)', Event),
                                     ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
