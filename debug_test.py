from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return "<h1>Flask is working!</h1><p>If you see this, Flask is running correctly.</p>"

@app.route('/test')
def test():
    return "<h2>Test route works!</h2>"

if __name__ == '__main__':
    print("Starting debug Flask app on http://localhost:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)