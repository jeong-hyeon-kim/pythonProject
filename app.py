from flask import Flask, render_template
app = Flask(__name__)

@app.route('/<word>')
def jinja2test(word):
    return render_template('index.html', name=word)


@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5050, debug=True)