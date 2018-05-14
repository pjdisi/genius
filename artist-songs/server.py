#USER_ID ="C4Vb94UtPS5C0W8HmwXyJNbCz43CkNjPZswJUt5egu6ewD31bRp9ROqayJcN-Yit"
#SECRET = "166HDMVL_hmC4JL8Lncc821AizJcj2AVRhoncIBVkyKAK41okmtIyOStmil4au5UkH_e7r4UaWMHDpqN9gHX5w"
#TOKEN= "-GXCUDSvuPxZOOo55wmFdWdJFIUEfU0jrnqDkjhJXK_fMZZXllX3VLcnNi7b8wkO"

import http.client
import json
import http.server
import socketserver
import sys
import codecs


class GeniusClient():
    repostory= None
    def client(self,name):
        name=name.replace(" ","%20")
        headers = {"Authorization": "Bearer "+ sys.argv[1]}

        conn = http.client.HTTPSConnection("api.genius.com")
        conn.request("GET", "/search?q=%s" % name, None, headers)
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        repos_raw = r1.read().decode("utf-8")
        repos = json.loads(repos_raw)
        GeniusClient.repostory = repos
        conn.close()
        print("A done")
        return
A = GeniusClient()


class GeniusParser():
    info1=None

    def parser(self):
        id = GeniusClient.repostory["response"]["hits"][0]["result"]["primary_artist"]["id"]
        GeniusParser.info1 = id
        print("B done")
        return

B =GeniusParser()

class GeniusClient2():
    repostory2 =None
    def client2(self):
        headers = {"Authorization": "Bearer " + sys.argv[1]}
        conn = http.client.HTTPSConnection("api.genius.com")
        conn.request("GET", "/artists/%s/songs?sort=popularity&page=1&per_page=30" % GeniusParser.info1, None, headers)
        r1 = conn.getresponse()
        print(r1.status, r1.reason)
        repos_raw = r1.read().decode("utf-8")
        repos = json.loads(repos_raw)
        GeniusClient2.repostory2 = repos
        conn.close()
        print("D done")
        return
D=GeniusClient2()

class GeniusParser2():
    info1=None
    info2=None
    def parser2(self):
        results1=[]
        results2=[]
        for element in GeniusClient2.repostory2["response"]["songs"]:
            try:
                results1.append(element["title"])
                results2.append(str(element["song_art_image_thumbnail_url"]))
            except KeyError:
                results1.append("Unknown")
                results2.append("Unknown picture")

        GeniusParser2.info1=results1
        GeniusParser2.info2=results2
        print(results2)
        print("B done")
        return

E =GeniusParser2()

class GeniusHTML:
    message=None
    def html(self):
        with codecs.open("geniushtml.html", "w","utf-8") as f:
            f.write("<meta charset='utf-8'>")
            f.write("<ul>" + "\n")
            print(GeniusParser2.info1)
            for x in range(len(GeniusParser2.info1)):
                link=GeniusParser2.info2[x]
                elementli = "<li>" + GeniusParser2.info1[x]+"<img src={0} style='width:100px;height:100px;'>".format(link) +"</li>"
                try:
                    f.write(elementli)
                except UnicodeEncodeError:
                    f.write("<li> Error </li>")
            f.write("</ul>")
        with codecs.open("geniushtml.html", "r","utf-8") as f:
            hello = str(f.read())
            GeniusHTML.message = hello
            print("C done")
        return
    def default(self):
        with open("final html default.html", "r") as f:
            hello = str(f.read())
            GeniusHTML.message = hello
            print("C done")

C = GeniusHTML()

socketserver.TCPServer.allow_reuse_address = True
# -- IP and the port of the server
IP = "localhost"  # Localhost means "I": your local machine
PORT = 8000


# HTTPRequestHandler class
class testHTTPRequestHandler(http.server.BaseHTTPRequestHandler):
    # GET
    def do_GET(self):
        # Send response status code
        self.send_response(200)
        # Send headers
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        if self.path =="/":
            C.default()
            self.wfile.write(bytes(GeniusHTML.message, "utf8"))

        elif "searchSongs?artist=" in self.path:
            name = self.path[self.path.find("=")+1:]
            A.client(name)
            B.parser()
            D.client2()
            E.parser2()
            C.html()
            self.wfile.write(bytes(GeniusHTML.message, "utf8"))

        print("File served!")
        return

    # Handler = http.server.SimpleHTTPRequestHandler
Handler = testHTTPRequestHandler

httpd = socketserver.TCPServer((IP, PORT), Handler)
print("serving at port", PORT)
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    pass

httpd.server_close()
print("")
print("Server stopped!")
