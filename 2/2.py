import os
import tornado.wsgi
import sae

class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("""
        <html>
        <body>
        <form action="/sign" method="post">
        <div><textarea name="content" rows="3" cols="60"></textarea></div>
        <div><input type="submit" value="Sign Guestbook"></div>
        </form>
        </body>
        </html>""")
    
    
class GuestbookHandler(tornado.web.RequestHandler):
    def post(self):
        self.write('<html><body>You wrote:<pre>')
        self.write(self.get_argument('content'))
        self.write('</pre></body></html>')
    
    
app = tornado.wsgi.WSGIApplication([
    (r"/", MainHandler),
    (r"/sign", GuestbookHandler),
])
    
application = sae.create_wsgi_app(app)
