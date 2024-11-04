from query import Query
from verifier import Verifier
import json

query_util = Query()
verifier = Verifier()


file_path = "dataset/preliminary/questions_example.json"
with open(file_path, 'r') as f:
    raw_data = json.load(f)


data = raw_data['questions']

answer = []

for i, question in enumerate(data):
    # if question['category'] != "faq":
    #     continue
    # print(i)
    # print(question['query'] + question['category'])
    result = query_util.query(question['query'], question['category'])
    found = False
    for i in result:
        if i in question['source']:
            found = True
            verifier.answer(question['qid'], question['category'], i)
            answer.append({"qid": question['qid'], "retrieve": i, "category": question['category']})
            break
    if not found:
        verifier.answer(question['qid'], question['category'], -1)
        answer.append({"qid": question['qid'], "retrieve": -1, "category": question['category']})

verifier.print_result()

with open('answer.json', 'w') as f:
    json.dump({"answer": answer}, f, indent=4)