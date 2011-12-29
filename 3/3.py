import os
import tornado.wsgi
import tornado.database
import sae
import sae.const


SinaDatabase = tornado.database.Connection(
        "%s:%s"%(sae.const.MYSQL_HOST,str(sae.const.MYSQL_PORT)), 
        sae.const.MYSQL_DB, 
        sae.const.MYSQL_USER, 
        sae.const.MYSQL_PASS, 
        max_idle_time = 30
)

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
        d = SinaDatabase.query("SELECT * FROM sinaTest ")
        self.write('<h1>')
        self.write(d[0]['info'])
        self.write('</h1>')
        self.write('<html><body>You wrote:<pre>')
        self.write(self.get_argument('content'))
        self.write('</pre></body></html>')

class InstallHandler(tornado.web.RequestHandler):
    def get(self):
        SinaDatabase.execute("Create table sinaTest(info varchar(100))")
        a = 'Welcome SinaAppEngine !'
        SinaDatabase.execute("INSERT INTO sinaTest (info) VALUES (%s)",a);
        self.write('</h1>ok</h1>')
        

app = tornado.wsgi.WSGIApplication([
    (r"/", MainHandler),
    (r"/sign", GuestbookHandler),
    (r"/install", InstallHandler),
])

application = sae.create_wsgi_app(app)
