import cv2
from PIL import Image
import threading
from http.server import BaseHTTPRequestHandler,HTTPServer
from socketserver import ThreadingMixIn
from io import StringIO,BytesIO
import time

img = []

class CamHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type','multipart/x-mixed-replace; boundary=--jpgboundary')
        self.end_headers()

        global img

        while True:
            try:
                if not len(img):
                    continue

                imgRGB=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
                jpg = Image.fromarray(imgRGB)
                tmpFile = BytesIO()
                jpg.save(tmpFile,'JPEG')
                self.wfile.write("--jpgboundary".encode())
                self.send_header('Content-type','image/jpeg')
                self.send_header('Content-length',str(tmpFile.getbuffer().nbytes))
                self.end_headers()
                jpg.save(self.wfile,'JPEG')
                time.sleep(0.05)
            except KeyboardInterrupt:
                break

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    """Handle requests in a separate thread."""

class HttpPipeline:
    def __init__(self, pipeline_register):
        self.p_reg = pipeline_register
        try:
            host = '0.0.0.0'
            port = 8087

            server = ThreadedHTTPServer((host, port), CamHandler)
            print( "server started. see: http://{0}:{1} (chrome only)".format(host, port))

            server_thread = threading.Thread(target=server.serve_forever)
            server_thread.daemon = True
            server_thread.start()

        except KeyboardInterrupt:
            server.socket.close()

    def process(self, frame):
        global img
        img = frame
