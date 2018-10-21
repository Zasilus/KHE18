from flask import Flask, render_template
from RMPLookup import RMPLookup


app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/RMPLookup.py<id>")
def displayresults(id):
    lookup = RMPLookup()
    return lookup.build_function(id)

    
if __name__ == "__main__":
    app.run(debug=True)
