from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from database_setup import Restaurant, Base, MenuItem
engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)

DBSession = sessionmaker(bind=engine)
session = DBSession()

class webserverHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path.endswith("/hello"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "Hello!"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'> \
                <h2>What would you like me to say?</h2><input name='message' type='text'> <input type='submit' \
                 value='Submit'> </form>"
                output += "</body></html>"

                self.wfile.write(bytes(output, "utf-8"))
                print(output)
                return

            if self.path.endswith("/edit"):
                restaurant_id = self.path.split("/")[2]
                current_restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
                if current_restaurant:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "%s<br><br>" % current_restaurant.name
                    output += "<form method='POST' enctype='multipart/form-data' action='restaurants/%s/edit'>" % restaurant_id
                    output += '''<input style = 'font-size: 1em; border-radius: 4px; display: block; margin-bottom: 10px;
                                 box-shadow: none;' name='message' enctype='multipart/form-data' type='text'
                                 placeholder='new name'>'''
                    output += "<input type='submit' value='Rename'><br>"
                    output += "</form"
                    output += "</body></html>"
                    self.wfile.write(bytes(output, 'utf-8'))
                    return

            if self.path.endswith("/delete"):
                restaurant_id = self.path.split("/")[2]
                current_restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
                if current_restaurant:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    output = ""
                    output += "<html><body>"
                    output += "<form method='POST' enctype='multipart/form-data' action='restaurants/%s/delete'>" % restaurant_id
                    output += "Are you sure you want to delete %s?" % current_restaurant.name
                    output += "<input type='submit' value = 'delete'>"
                    output += "</form>"
                    output += "</body></html>"
                    self.wfile.write(bytes(output, 'utf-8'))
                    return

            if self.path.endswith("/restaurants"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                restaurants = session.query(Restaurant).all()
                for restaurant in restaurants:
                    output += "<p> %s <p>" % restaurant.name
                    output += "<a href='/restaurants/%s/edit'>Edit</a><br>" % restaurant.id
                    output += "<a href='/restaurants/%s/delete'>Delete</a>" % restaurant.id
                    output += "<div style='margin-bottom: 50px'></div>"

                output += "<a href='/restaurants/new'> Create A New Restaurant </a>"
                output += "</body></html>"

                self.wfile.write(bytes(output, "utf-8"))
                return

            if self.path.endswith("/hola"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "&#161Hola <a href='/hello'> Back to hello</a>"
                output += "<form method='POST' enctype='multipart/form-data' action='/hello'> \
                <h2>What would you like me to say?</h2><input name='message' type='text'> <input type='submit' \
                 value='Submit'> </form>"
                output += "</body></html>"

                self.wfile.write(bytes(output, "utf-8"))
                return

            if self.path.endswith("/restaurants/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()

                output = ""
                output += "<html><body>"
                output += "<h1> Make A New Restaurant </h1>"
                output += "<form method='POST' enctype='multipart/form-data' action='/restaurants/new'>"
                output += "<input style = 'font-size: 1em; border-radius: 4px; display: block; margin-bottom: 10px; box-shadow: none;' name='message' enctype='multipart/form-data' type='text' placeholder='restaurant name'>"
                output += "<input type='submit' value='Submit'>"
                output += "</form>"
                output += "</body></html>"
                self.wfile.write(bytes(output, "utf-8"))
                return

        except IOError:
            self.send_error(404, "File Not Found %s" % self.path)

    def do_POST(self):
        try:
            if self.path.endswith("/edit"):
                self.send_response(301)
                self.send_header("Content-type", "text/html")
                self.send_header("Location", "/restaurants")
                self.end_headers()
                length = self.headers['content-length']
                post_data = self.rfile.read(int(length))
                post_data = str(post_data,'utf-8')
                content = post_data.split("\n")[3]
                restaurant_id = self.path.split("/")[2]
                current_restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
                current_restaurant.name = content
                session.add(current_restaurant)
                session.commit()
                return

            if self.path.endswith("/delete"):
                self.send_response(301)
                self.send_header('Content-type', 'text/html')
                self.send_header('Location', '/restaurants')
                self.end_headers()
                restaurant_id = self.path.split('/')[2]
                current_restaurant = session.query(Restaurant).filter_by(id=restaurant_id).one()
                session.delete(current_restaurant)
                session.commit()
                return

            if self.path.endswith("/restaurants/new"):
                    self.send_response(301)
                    self.send_header("Content-type", "text/html")
                    self.send_header("Location", "/restaurants")
                    self.end_headers()
                    length = self.headers['content-length']
                    post_data = self.rfile.read(int(length))
                    post_data = str(post_data,'utf-8')
                    content = post_data.split("\n")[3]
                    restaurant = Restaurant(name = content)
                    session.add(restaurant)
                    session.commit()

        except:
            pass
            #python 2.7code
            '''
            ctype, pdict = cgi.parse_header(self.headers.getheader('content-type'))
            if ctype == 'multipart/form-data':
                fields = cgi.parse_multipart(self.rfile, pdict)
                messagecontent = fields.get('message')[0]
                output = ""
                output += "<html><body>"
                output += "<h2> Okay, how about this: </h2>"
                output += "<h1> %s </h1>" % messagecontent[0]

                output += "<form method='POST' enctype='multipart/form-data' action='/hello'> \
                <h2>What would you like me to say?</h2><input name='message' type='text'> <input type='submit' \
                 value='Submit'> </form>"
                output += "</body></html>"
                self.wfile.write(bytes(output, "utf-8"))
            '''


def main():
    try:
        port =  8080
        server = HTTPServer(('', port), webserverHandler)
        print("Web server runnig on port %s" % port)
        server.serve_forever()

    except:
        print("^C entered, stopping web server...")
        server.socket.close()


if __name__ == '__main__':
    main()
