import sae
import sae.const

import tornado.wsgi
import tornado.database


SinaDatabase = tornado.database.Connection(
        "%s:%s"%(sae.const.MYSQL_HOST,str(sae.const.MYSQL_PORT)), 
        sae.const.MYSQL_DB, 
        sae.const.MYSQL_USER, 
        sae.const.MYSQL_PASS, 
        max_idle_time = 30
)
 
class GuestbookHandler(tornado.web.RequestHandler):
    def get(self):
     template_values = {}
        template_values['test'] = SinaDatabase.query("SELECT * FROM sinaTest ")
        path = os.path.join(os.path.dirname(__file__),'Guestbook.html')
        self.render(path,tpl=template_values)

    def post(self):
        a = self.get_argument('content')
        SinaDatabase.execute("INSERT INTO sinaTest (info) VALUES (%s)",a)
        self.redirect('/')

class InstallHandler(tornado.web.RequestHandler):
    def get(self):
        SinaDatabase.execute("Create table sinaTest(info varchar(100))")
        a = 'Welcome SinaAppEngine !'
        SinaDatabase.execute("INSERT INTO sinaTest (info) VALUES (%s)",a)
        self.write("""<html><body><a href="/">Home</a></body></html>""")

app = tornado.wsgi.WSGIApplication([
    (r"/", GuestbookHandler),
    (r"/install", InstallHandler),
])
 
application = sae.create_wsgi_app(app)
