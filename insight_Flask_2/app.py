import sys
from insight_gen import *
from flask import Flask, render_template, request, jsonify


app = app = Flask(__name__, static_folder='static', template_folder='template')

@app.route('/', methods=['GET', 'POST'])
def home():
    output = None
    if request.method == 'POST':
        try:
            user_query = request.form.get('query')
            print(f"Received query: {user_query}")  # Debugging line
            output = insight(user_query)  # Call the external function
            print(f"Response:\n{output}")  # Debugging line
            output = jsonify(output)
        except Exception as e:
            print(f"Error processing query: {e}", file=sys.stderr)

    return render_template('index.html',output)

if __name__ == '__main__':
    app.run(debug=False)

