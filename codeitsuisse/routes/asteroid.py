import json
import logging
from flask import request, jsonify
from codeitsuisse import app

global text 
logger = logging.getLogger(__name__)
@app.route('/asteroid', methods=['POST'])
def evaluate_Asteriod():
    global sentence
    global mark
    global origin_position
    global inputValue
    global data
    global text
    data = request.get_json()
    logging.info("data sent for evaluation {}".format(data))
    #inputValue = data.get("input")
    result=[]
    for test_case in data:
        result.append(main(test_case))
    logging.info("input :{}".format(text))
    logging.info("score :{}".format(mark))
    logging.info("origin :{}".format(origin_position))
    return json.dumps(result)

mark=0
#split the sentence
def split_by_unique_groups(list_):
    to_return = []

    idx = 0
    while idx != len(list_):
        curr = list_[idx]

        next_bad_idx = None
        for x in range(idx+1, len(list_)):
            if list_[x] != curr:
                next_bad_idx = x
                break

        sub_str = list_[idx:next_bad_idx] # [x:None] returns x to len(s)
        to_return.append(sub_str)

        if next_bad_idx is None:
            break
        idx = next_bad_idx
    return to_return
def main(sentence):
    global mark
    global origin_position
    global inputValue
    global data
    global text
    sentence_split = split_by_unique_groups(sentence)


    #test
    while len(sentence_split)>1:
        origin=int(len(sentence_split)/2)
        global index
        index=len(sentence_split[origin])
        if sentence_split[origin-1][0]==sentence_split[origin+1][0]:
            if (len(sentence_split[origin-1])+len(sentence_split[origin+1]))>=10:
                mark+=2*(len(sentence_split[origin-1])+len(sentence_split[origin+1]))

            elif (len(sentence_split[origin-1])+len(sentence_split[origin+1]))>=7:
                mark+=1.5*(len(sentence_split[origin-1])+len(sentence_split[origin+1]))

            else:
                mark+=(len(sentence_split[origin-1])+len(sentence_split[origin+1]))

            sentence_split.pop(origin-1)
            sentence_split.pop(origin)

        else:
            break
    if index>=10:
        mark+=2*index
    elif index>=7:
        mark+=1.5*index
    else:
        mark+=index

    sentence_copy=split_by_unique_groups(sentence)

    origin_position=int(len(sentence_copy)/2)
    numberOfOrigin=0
    i=0
    while i < origin_position:
        numberOfOrigin+=len(sentence_copy[i])
        i+=1
    numberOfOrigin+=int(len(sentence_copy)/2)-1

    return {"input" : sentence,"score" : mark, "origin" : origin_position}
