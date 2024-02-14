from flask import Flask, request, render_template, redirect, url_for
from subprocess import check_output
import os

app = Flask(__name__)

CHOICES = ["script1.py", "script2.py"]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        script = request.form.get('script')
        print(script)
        if script:
            output = check_output(f"python {script}", shell=True).decode('utf-8')
            return redirect(url_for('result', output=output))
    return render_template('index.html', choices=CHOICES)

@app.route('/result')
def result():
    output = request.args.get('output', '')
    return render_template('result.html', output=output)

if __name__ == '__main__':
    app.run(debug=True)