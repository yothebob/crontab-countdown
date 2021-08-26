from flask import Flask, render_template, request, g, url_for
from cronruntime import CronRunTime
from wtforms import Form, SelectField, SubmitField, validators
import os
import re

app = Flask(__name__)
filename = "crontab_cases.txt"
filepath = os.getcwd()
print(filepath)

app.static_folder = "static"

@app.route("/",methods=['GET','POST'])
def index():

    crontab = CronRunTime(filename,filepath)
    functions = crontab.create_functions_dictionary()
    tupled_keys = [(key,key) for key in functions.keys()]

    class FunctionForm(Form):
        select_function = SelectField("Select your function: ",choices=tupled_keys)
        submit = SubmitField("Submit")

    form = FunctionForm(request.form)
    if request.method == "POST":
        time_fields = functions[form.select_function.data]
        time_remaining_fields = crontab.return_function_next_run_time(time_fields)
        real_times = ["min","hour","day","month","day of week"]
        return render_template("index.html",form=form,time_remaining_fields=time_remaining_fields,real_times=real_times)

    return render_template("index.html",form=form)


if __name__ == "__main__":
    app.run()
