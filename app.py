from flask import Flask, render_template, request, jsonify
import testing_tweets as tt

app = Flask(__name__)

@app.route('/process_input', methods=['GET', 'POST'])
def process_input():
    if request.method == 'POST':
        input_text = request.json['input_text']
        
        # Process input_text using your Python code
        suicide_score = tt.main(input_text, 10)
        print(suicide_score)

        output_text = f'Risk factor: {suicide_score}'
        
        return render_template('index.html', output_text = output_text)
    
    else:
        return render_template('index.html', output_text = output_text)
    

if __name__ == '__main__':
    app.run(debug=True)

