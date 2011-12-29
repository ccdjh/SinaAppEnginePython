#############################################################################
#######
####### 1, 框架的 Hello World
#######
#############################################################################
"""
搭建在SinaAppEngine的 tornadoWeb 框架，下面是简单的 Hello World 使用。

创建 SinaAppEngine 应用程序的过程非常简单，只需几分钟时间，而且可以免费开始使用。
本案例使用的是Python语言。SinaAppEngine的环境是Python 2.6 Tornado 2.1.1

在本教程结束前，您将实现一个可运行的应用程序 - 可让用户将消息发布到公共留言板的简单留言簿。
"""
import os
import tornado.wsgi
import sae
 
 
class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.write("Hello, world")
 
app = tornado.wsgi.WSGIApplication([
    (r"/", MainHandler),
])
 
application = sae.create_wsgi_app(app)

#############################################################################
#######
####### 2, 处理表单
#######
#############################################################################

"""

知识点至于建立函数 
在GuestbookHandler上,通过建立函数def post(self):
self.get_argument('content')，来接收单post过来的 name="content"

"""

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

#############################################################################
#######
####### 3, 开通数据库，创建表
#######
#############################################################################
"""

知识点至于:
首先 import tornado.database 和 import sae.const
通过tornado.database.Connection 与 SinaAppEngine的Mysql数据库连接
sae.const的作用是通过SinaAppEngine提供的变量，而不会在自己的案例代码上,暴露相关资料!

添加一个新类InstallHandler，用来初始化Mysql数据：

SinaDatabase.execute("Create table sinaTest(info varchar(100))")
创建表sinaTest，添加info字段

SinaDatabase.execute("INSERT INTO sinaTest (info) VALUES (%s)",a);
插入 a 变量的内容进 info

SinaDatabase.query("SELECT * FROM sinaTest ")
查找sinaTest里面的内容

"""
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

#############################################################################
#######
####### 4, 使用模板 Template,整理前面的例子代码
#######
#############################################################################
"""
通过案例1,2,3 ，你应该感觉到代码和Html混在一起，会显得很乱，不好看，不好处理。
所以引进模板，建立一个Guestbook.html文件，把之前MainHandler的Html放进去

知识点：
self.render(path,tpl=template_values) 
path是模板的文件路径
tpl=template_values是放进模板里面的变量，例如{{ t['info'] }}

self.redirect('/') 是重定向

"""
import os

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

####Guestbook.html 文件

<html>
    <head>
        <title>GuestBook | Sina App Engine</title>
    </head>
    <body>
        <h3>{% for t in tpl['test'] %}<p> {{ t['info'] }} </p>{% end %}</h3>
    <form action="/" method="post">
    <div><textarea name="content" rows="3" cols="60"></textarea></div>
    <div><input type="submit" value="Submit Guestbook"></div>
         </form>
    </body>
</html>

#############################################################################
#######
####### 5, 添加静态文件 static文件夹
#######
#############################################################################
"""
创建文件夹static,这是SinaAppengine提供的。把文件放里面，例如Css,Javascript ,logo之类的
例如：
<link href="/static/style.css" type="text/css" rel="stylesheet"></link>
<a href="/"><img src="/static/logo.gif"></a>
"""

#############################################################################
#######
#######Guestbook.html 文件
#######
#############################################################################
"""
<html>
<head>
<title>GuestBook | Sina App Engine</title>
<link href="/static/style.css" type="text/css" rel="stylesheet"></link>
</head>
<body>
        <h3>{% for t in tpl['test'] %}<p> {{ t['info'] }} </p>{% end %}</h3>
    <form action="/" method="post">
    <div><textarea name="content" rows="3" cols="60"></textarea></div>
    <div><input type="submit" value="Submit Guestbook"></div>
        </form>
        <a href="/"><img src="/static/logo.gif"></a>
</body>
</html>
"""

####/static/style.css 文件
"""
body{background:#ddd;}
"""
