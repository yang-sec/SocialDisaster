import os
# import re
import json

from flask import Flask, request, flash, redirect, render_template, send_from_directory

app = Flask(__name__)
app.secret_key = 'development key'


app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'csv','rsv', 'xml', 'json'])

# initial load page
@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template('index.html')
@app.route('/compute', methods=['GET', 'POST'])
def compute():
	return "request data" + request.args.get('Month')
	#return render_template('compute.html')


if __name__ == "__main__":
    app.run(debug=True)
