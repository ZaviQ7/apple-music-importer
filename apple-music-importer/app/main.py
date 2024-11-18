from flask import Flask, render_template, jsonify
from automation import open_downloads_folder

app = Flask(__name__, 
            template_folder='../templates',
            static_folder='../static')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/open-downloads', methods=['POST'])
def handle_open_downloads():
    success, error = open_downloads_folder()
    if success:
        return jsonify({"status": "success"})
    else:
        return jsonify({"status": "error", "message": error})

if __name__ == '__main__':
    app.run(debug=True, port=5000)