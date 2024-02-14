from flask import Flask, render_template, request
import runpy
import sys
import io

class FlaskApp(Flask):
    def run_script(self, script_name):
        with open(script_name, 'r') as f:
            code = compile(f.read(), script_name, 'exec')

        # Capture stdout from the script
        old_stdout = sys.stdout
        new_stdout = io.StringIO()
        sys.stdout = new_stdout

        # Create a global namespace dictionary
        globals_dict = {'__builtins__': __builtins__}

        # Execute the script in the global namespace
        exec(code, globals_dict)

        sys.stdout = old_stdout

        output = new_stdout.getvalue()

        # Return the global namespace dictionary
        return output, globals_dict

app = FlaskApp(__name__)

@app.route("/", methods=['GET', 'POST'])
def home():
    output = ''
    my_variable = None
    
    if request.method == 'POST':
        script = request.form.get('script')
        if script:
            output, globals_dict = app.run_script(script)
            my_variable = globals_dict.get('my_variable')
        
    return render_template("index.html", scripts=["script1.py", "script2.py"], output=output, my_variable=my_variable)

if __name__ == "__main__":
    app.run(debug=True)