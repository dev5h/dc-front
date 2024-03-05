from flask import Flask, Response, render_template, jsonify
from src.get_courses import getCourses, get_http
app = Flask(__name__)

@app.route("/api/percentages")
def api():
    return "HELLO"



def main():
    app.run(port=8080, debug=True)

if __name__ == "__main__":
    main()