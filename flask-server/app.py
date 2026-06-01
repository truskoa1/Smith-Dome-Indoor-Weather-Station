from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
	return "<h1>Meow!</h1><p>Meow meow meow meow >:)</p>"

@app.route("/evil")
def evil():
	return "<h3>I am evil cat</h3><p>Woem woem woem</p>"

if __name__ == "__main__":
	app.run(debug=True, port=5000)

