from flask import Flask, render_template, request, jsonify

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/process_input', methods=['POST'])
def process_input():
    input_text = request.json['input_text']
    # Process input_text using your Python code
    output_text = input_text.upper()
    return jsonify({'output': output_text})

if __name__ == '__main__':
    app.run(debug=True)
