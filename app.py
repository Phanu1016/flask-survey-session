from flask import Flask, flash, request, render_template, redirect, session
from surveys import satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret"

# responses = []
# question_number = 0

@app.route("/")
def home():
    """ Home page where user prompts to start the survey """
    survey_title = satisfaction_survey.title
    survey_instructions = satisfaction_survey.instructions
    return render_template("home.html", survey_title=survey_title, survey_instructions=survey_instructions)

@app.route('/start-survey', methods=['POST'])
def start_survey():
    """ Create an empty session and redirect to the questions """
    session['responses'] = []
    session['question_number'] = 0
    return redirect(f"/questions/{session['question_number']}")

@app.route("/questions/<int:number>")
def question(number):
    """ Questions page where user answer the survey questions """
    if session['question_number'] == len(satisfaction_survey.questions):
        return redirect(f"/thank_you")
    elif session['question_number'] != number:
        flash("Error - Trying to access an invalid question.")
        return redirect(f"/questions/{session['question_number']}")

    survey_question = satisfaction_survey.questions[session['question_number']].question
    survey_choices = satisfaction_survey.questions[session['question_number']].choices
    return render_template("question.html", survey_question=survey_question, choice_1=survey_choices[0], choice_2=survey_choices[1])

@app.route("/thank_you")
def thank_you():
    """ Thank you page where user gets a thank you """
    if session['question_number'] != len(satisfaction_survey.questions):
        return redirect(f"/questions/{session['question_number']}")
    print(session['responses'])
    return """<h1> Thank you!! </h1>"""

@app.route("/answer", methods=["POST"])
def answer():
    """ Answer page where answers being posted """
    # global question_number
    if request.form.get('choice_1') == None and request.form.get('choice_2') == None:
        flash("Error - Please select an answer.")
        return redirect(f"/questions/{session['question_number']}")
    elif request.form.get('choice_1') != None:
        # responses.append(request.form.get('choice_1'))
        updateResponses(request.form.get('choice_1'))
    else:
        # responses.append(request.form.get('choice_2'))
        updateResponses(request.form.get('choice_2'))
    session['question_number'] += 1
    # question_number += 1

    if session['question_number'] == len(satisfaction_survey.questions):
        return redirect(f"/thank_you")
    else:
        return redirect(f"/questions/{session['question_number']}")

def updateResponses(value):
    """ Update responses in the session """
    responses = session['responses']
    responses.append(value)
    session['responses'] = responses