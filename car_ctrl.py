from motorControl import *
from database import *
from global_interface import *
from flask import Flask, render_template

class RobotController:
    def __init__(self, host="192.168.1.244", port=5000):
        self.app = Flask(__name__)
        self.host = host
        self.port = port
        self.setup_routes()

    def setup_routes(self):
        @self.app.route("/")
        def index():
            return render_template("index.html")

        @self.app.route("/<cmd>")
        def move(cmd):
            if cmd == "forward":
                forward(45)
            elif cmd == "backward":
                backward(45)
            elif cmd == "left":
                turnLeft(50)
            elif cmd == "right":
                turnRight(50)
            else:
                brake()
            return ("", 204)

        @self.app.route("/shutdown")
        def shutdown():
            brake()
            return "Stopped"

    def run(self):
        self.app.run(host=self.host, port=self.port)

if __name__ == "__main__":
    controller = RobotController()
    controller.run()
