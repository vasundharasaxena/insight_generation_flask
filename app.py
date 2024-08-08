import sys
from insight_gen import insight  # Ensure this is the correct import based on your module
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS, cross_origin
 
app = Flask(__name__, static_folder='static', template_folder='template')
cors = CORS(app, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'
 
@app.route('/', methods=['GET', 'POST'])
def home():
    output = None
    if request.method == 'POST':
        try:
            user_query = request.form.get('query')
            print(f"Received query: {user_query}")  # Debugging line
            output = insight(user_query)  # Call the external function
            print(f"Response:\n{output}")  # Debugging line
        except Exception as e:
            print(f"Error processing query: {e}", file=sys.stderr)
 
    return render_template('index.html', output_json=output)
 
if __name__ == '__main__':
    app.run(debug=False)