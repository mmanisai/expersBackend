from flask import Flask, request, abort, jsonify
import os

from questiongenerator import QuestionGenerator
qg = QuestionGenerator()

app = Flask(__name__)

@app.route('/hello')
def smile():
    return jsonify({'message': 'hello'})


@app.route('/api', methods=['POST'])
def api():
    body = request.get_json()
    text = body.get('text', None)
    Qtype = body.get('type', "multiple_choice")
    noOfQ = body.get('numberOfQuestions', 5)

    li = qg.generate(text, num_questions=noOfQ, answer_style=Qtype)
    if Qtype == "multiple_choice":
        newLi = []
        for i in range(len(li)):
            qn = {}
            qn["question"] = li[i]["question"]

            for j in range(len(li[i]["answer"])):
                if li[i]["answer"][j]["correct"] is True:
                    qn["answer"] = li[i]["answer"][j]["answer"]
            wrongeAnswers = []
            
            for j in range(len(li[i]["answer"])):
                if li[i]["answer"][j]["correct"] is False:
                    wrongeAnswers.append(li[i]["answer"][j]["answer"])
            qn["wrongeAnswers"] = wrongeAnswers
            newLi.append(qn)
        response = newLi
    else:
        response = li

    numberOfQuestions = len(response)
    return jsonify({
        'status': "Sucess",
        'apiResponse': response,
        'numberOfQuestions': numberOfQuestions,
        'type':Qtype,
        'numberOfQuestionsRequested':noOfQ
    })