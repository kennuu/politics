import json
import pandas as pd

candidatefile = '../data/candidateanswers.json'


with open(candidatefile) as file:
    candidates = json.load(file)

for (ind, candidate) in enumerate(candidates):
    answers = candidate.pop('answers')
    numanswers = {'question_' + f"{answer['questionId']:02d}": answer['answer'] for answer in answers}
    explanations = {'explanation_' + f"{answer['questionId']:02d}": answer['explanation'] for answer in answers}

    candidates[ind] = {**candidate, **numanswers, **explanations}

candidates = pd.DataFrame.from_dict(candidates)
print("done")
