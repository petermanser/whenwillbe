from google.appengine.ext import webapp
from google.appengine.ext.webapp.util import run_wsgi_app
from google.appengine.ext.webapp import template

class MainPage(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        
        self.response.out.write(template.render('templates/index.html', {}))

class Create(webapp.RequestHandler):
    def get(self):
        self.redirect('/', permanent=True)

class Event(webapp.RequestHandler):
    def get(self):
        self.response.headers['Content-Type'] = 'text/html'
        self.response.out.write(template.render('templates/event.html', {'event': {'url':self.request.path.split('/')[2]}}))
        


application = webapp.WSGIApplication([('/', MainPage),
                                      ('/create', Create),
                                      ('/e/.*', Event),
                                     ],
                                     debug=True)

def main():
    run_wsgi_app(application)

if __name__ == "__main__":
    main()
