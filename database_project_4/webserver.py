from http.server import BaseHTTPRequestHandler, HTTPServer
import cgi
from database_setup import Restaurant, Base, MenuItem
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

engine = create_engine('sqlite:///restaurantmenu.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()

class WebServerHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        try:
            if self.path.endswith("/restaurant/new"):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                message = "<html><body>"
                message += "<h1>Make a New Restaurant</h1>"
                message += "<form method='POST' enctype='multipart/form-data' action='/restaurant/new'>"
                message += "<input name='newRestaurantName' type='text' placeholder='New Restaurant Name'>"
                message += "<input type='submit' value='Create'>"
                message += "</form></body></html>"
                self.wfile.write(message.encode("utf-8"))
                return
            
            elif self.path.endswith("/edit"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    message = "<html><body>"
                    message += "<h1>"
                    message += myRestaurantQuery.name
                    message += "</h1>"
                    message += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/edit'>" % restaurantIDPath
                    message += "<input name='newRestaurantName' type='text' placeholder='%s'>" % myRestaurantQuery.name
                    message += "<input type='submit' value='Rename'>"
                    message += "</form>"
                    message += "</body></html>"
                    self.wfile.write(message.encode("utf-8"))
                    return
            
            elif self.path.endswith("/restaurant"):
                self.send_response(200)
                self.send_header("Content-type", "text/html")
                self.end_headers()
                restaurants = session.query(Restaurant).all()
                message = "<html><body>"
                message += "<h1>Restaurants</h1>"
                for restaurant in restaurants:
                    message += restaurant.name
                    message += "</br>"
                    message += "<a href='/restaurants/%s/edit'>Edit</a> " % restaurant.id
                    message += "</br>"
                    message += "<a href='/restaurants/%s/delete'>Delete</a>" % restaurant.id
                    message += "</br></br></br>"
                message += "</body></html>"
                self.wfile.write(message.encode("utf-8"))
                return
            
            elif self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if myRestaurantQuery:
                    self.send_response(200)
                    self.send_header('Content-type', 'text/html')
                    self.end_headers()
                    message = "<html><body>"
                    message += "<h1>Are you sure you want to delete %s?</h1>" % myRestaurantQuery.name
                    message += "<form method='POST' enctype='multipart/form-data' action='/restaurants/%s/delete'>" % restaurantIDPath
                    message += "<input type='submit' value='Delete'>"
                    message += "</form>"
                    message += "</body></html>"
                    self.wfile.write(message.encode("utf-8"))
                    return

            else:
                self.send_error(404, 'File Not Found: %s' % self.path)
        except Exception as e:
            self.send_error(500, 'Internal Server Error: %s' % str(e))

    def do_POST(self):
        try:
            if self.path.endswith("/delete"):
                restaurantIDPath = self.path.split("/")[2]
                myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one()
                if myRestaurantQuery:
                    session.delete(myRestaurantQuery)
                    session.commit()
                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurant')
                    self.end_headers()
                    
            elif self.path.endswith("/edit"):
                ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
                if ctype == 'multipart/form-data':
                    pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    messagecontent = fields.get('newRestaurantName')[0].decode('utf-8')
                    restaurantIDPath = self.path.split("/")[2]
                    myRestaurantQuery = session.query(Restaurant).filter_by(id=restaurantIDPath).one_or_none()
                    if myRestaurantQuery:
                        myRestaurantQuery.name = messagecontent
                        session.add(myRestaurantQuery)
                        session.commit()
                        self.send_response(301)
                        self.send_header('Content-type', 'text/html')
                        self.send_header('Location', '/restaurant')
                        self.end_headers()

            elif self.path.endswith("/restaurant/new"):
                ctype, pdict = cgi.parse_header(self.headers.get('content-type'))
                if ctype == "multipart/form-data":
                    pdict['boundary'] = bytes(pdict['boundary'], "utf-8")
                    fields = cgi.parse_multipart(self.rfile, pdict)
                    new_restaurant_name = fields.get('newRestaurantName')[0].decode('utf-8')

                    new_restaurant = Restaurant(name=new_restaurant_name)
                    session.add(new_restaurant)
                    session.commit()

                    self.send_response(301)
                    self.send_header('Content-type', 'text/html')
                    self.send_header('Location', '/restaurant')
                    self.end_headers()
        except Exception as e:
            print("Error:", e)
            self.send_error(500, 'Internal Server Error: %s' % str(e))

def main():
    try:
        port = 8080
        server = HTTPServer(('', port), WebServerHandler)
        print("Web Server running on port %s" % port)
        server.serve_forever()
    except KeyboardInterrupt:
        print("^C entered, stopping web server...")
        server.socket.close()

if __name__ == '__main__':
    main()
