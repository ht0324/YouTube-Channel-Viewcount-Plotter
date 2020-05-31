from io import BytesIO
import http.server
import json
import socketserver

import YouTube_channel_graph_plotter as result
PORT = 8004

class Handler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)
        self.end_headers()

        if self.path == '/':
            with open('index.html', 'rb') as file: 
                self.wfile.write(file.read())
        if self.path == '/hello':
            self.wfile.write(b'Hello yourself!')
        return

    def do_POST(self):
        if self.path == '/main':
            content_length = int(self.headers['Content-Length'])
            body = self.rfile.read(content_length)
            self.send_response(200)
            self.end_headers()
            response = BytesIO()
            response.write(b'Received the following input through POST request: ')
            response.write(body)
            
            string_response = str(body, 'utf-8')
            key_val = string_response.split('=')
            key, val = key_val[0], key_val[1]
            
#            result.main(val)
            Username = val
            input_channel = result.channel(Username)
            video_list = input_channel.video_id_list
            view = result.video_data(video_list,"viewCount")
            like = result.video_data(video_list,"likeCount")
            dislike = result.video_data(video_list,"dislikeCount")
            comment = result.video_data(video_list,"commentCount")
            input_channel.print_graph(view, like, dislike, comment)
            
            print(f'key:{key}, val: {val}')
                
            with open(f"{val}.png", 'rb') as file:
                self.wfile.write(file.read())
            
            self.wfile.write(response.getvalue())

print('Starting the server ...')
httpd = socketserver.TCPServer(('',PORT), Handler)
print("serving at port", PORT)
httpd.serve_forever()
