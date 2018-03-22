import random
import string
from xml.dom import minidom
import re

def id_generator(size=6, chars=string.ascii_uppercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


test_code = id_generator()


def chunks(l, n):
    n = max(1, n)
    return (l[i:i+n] for i in range(0, len(l), n))


class Answer:
    """TODO"""

    def __init__(self):
        """"""
        self.is_answer_correct = False
        self.text = '?'

    def is_correct(self):
        """ """
        return self.is_answer_correct

    def get_text(self):
        """"""
        return self.text

    def set_text(self, text):
        """"""
        if text.startswith("+"):
            self.is_answer_correct = True
        else:
            self.is_answer_correct = False

        self.text = text.replace('+ ', '')


class Item:
    """TODO"""

    def __init__(self, new_item_id):
        """"""
        self.item_id = new_item_id
        self.question = '?'
        self.answers = []
        self.answer_letter_map = {0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'H'}

    def set_question(self, question):
        """Sets something"""
        self.question = question

    def add_answer(self, new_answer):
        self.answers.append(new_answer)

    def get_question(self):
        """Returns item's question"""
        return self.question

    def __str__(self):
        """"""
        st = self.item_id + ". " + self.question
        for i in range(0, 4):
            answer = self.answers[i]
            if answer.is_correct():
                st += "(*)"
            st = st + answer.get_text() + " "
        return st

    def to_html(self, no):
        """"""
        st = "<div class=question>" \
             "<div class=question_id_text><div class=question_id>" +\
             no +\
             ". </div><div class=question_text>" +\
             self.question + "</div></div>"

        st += "<div class=answers>"
        answer_index = 0
        for answer in self.answers:
            st += "<div class=answer>"
            st += "<div class=answer_id>"
            print(answer.get_text())
            print(answer_index)
            st += self.answer_letter_map[answer_index]
            st += "."
            st += "</div><div class=answer_text>"
            st += answer.get_text()
            st += "</div>"
            st += "</div>"
            answer_index += 1
        st += "</div>"

        st += "</div>"
        return st

    def shuffle_answers(self):
        """"""
        random.shuffle(self.answers, random.random)

    def get_correct_answer(self):
        """"""
        answer_letter = '?'
        i = 0
        for answer in self.answers:
            if answer.is_correct():
                answer_letter = self.answer_letter_map[i]
                break
            i += 1
        return answer_letter


# --------------------------------------------------------------------------
items = []

# questions_file_name = 'questions-pwir-kol2.txt'
# questions_file_name = 'questions-pwir.txt'
# questions_file_name = 'questions-iswddum.txt'
#questions_file_name = 'questions-ai2-test-1.txt'
#questions_file_name = 'questions-ai2-exam-niestacj.txt'
#questions_file_name = 'questions-ai2-exam-stacj-2017.txt'
#questions_file_name = 'questions-ai2-kol2-stacj-2017.txt'
questions_file_name = 'questions-paum-2017-12.txt'
#questions_file_name = 'questions-iswddum-2017-12.txt'

f = open(questions_file_name, encoding='utf-8')
# f = open(questions_file_name, 'r', 'utf-8')
lines = f.readlines()
count = len(lines)
i = 0
title = lines[i]
i += 1
date = lines[i]
i += 1
while i < count:
    line = lines[i]                             # id
    if line.startswith('#'):
        item_id = line.strip().split(' ')[1]
        item = Item(item_id)

        i += 1
        line = lines[i]

        question = ""
        while not line.startswith("---"):
            question += line
            i += 1
            line = lines[i]

        question = question.strip('\r\n')                 # question
        question = question.replace('\n', ' ')
        question = question.replace("<cs>", "<br><code>")
        question = question.replace("</cs>", "</code><br>")
        question = question.replace("<c>", "<code>")
        question = question.replace("</c>", "</code>")
        question = question.replace("`", "&nbsp;")
        item.set_question(question)

        i += 1

        while i < count:
            if lines[i].strip().startswith("#"):
                break
            answer_text = lines[i].strip()
            answer_text = answer_text.replace("<c>", "<code>")
            answer_text = answer_text.replace("</c>", "</code>")
            answer = Answer()
            answer.set_text(answer_text)
            item.add_answer(answer)
            i += 1

        item.shuffle_answers()
        items.append(item)
    else:
        i += 1

#
items_ids = [i for i in range(len(items))]
random.shuffle(items_ids, random.random)
items_ids = random.sample(items_ids, 22)

test_file_name = questions_file_name.replace('questions-', '')
test_file_name = test_file_name.replace('.txt', '')

file_test_path = test_file_name + '-test.html'
file_key_path = test_file_name + '-key.html'

template_test_path = 'template-test' + '.html'
template_key_path = 'template-key' + '.html'

file_test = open(file_test_path, 'w', encoding='utf-8')
file_key = open(file_key_path, 'w', encoding='utf-8')

#print('Openning file: ' + template_test_path)
template_file_test = open(template_test_path, 'r', encoding='utf-8')
#print('Openning file: ' + template_key_path)
template_file_key = open(template_key_path, 'r', encoding='utf-8')

template_html_test = str(template_file_test.read())
template_html_key = str(template_file_key.read())

answer_ids = ''
answer_key = ''
content = ''
chunk_size = (int)(len(items_ids) / 2)
# :w
chunk_size = 22
items_ids_chunks = chunks(items_ids, chunk_size)

i = 0
for items_ids_chunk in items_ids_chunks:
    while len(items_ids_chunk) < chunk_size:
        items_ids_chunk.append(-1)
    answer_key += '<table class=answer_table>'
    answer_ids += '<table class=answer_table>'
    answer_key += '<tr>'
    answer_ids += '<tr>'
    for item_id in items_ids_chunk:
        i += 1
        answer_key += '<td>' + str(i) + '</td>'
        if item_id < 0:
            answer_ids += '<td class="empty_answer">' + str(i) + '</td>'
        else:
            answer_ids += '<td>' + str(i) + '</td>'
    answer_key += '</tr>'
    answer_ids += '</tr>'
    answer_key += '<tr>'
    answer_ids += '<tr>'

    for item_index in items_ids_chunk:
        answer_code = ''
        if item_index >= 0:
            item = items[item_index]
            print(item.get_question())
            answer_code = '<td>'+item.get_correct_answer()+'</td>'
        else:
            answer_code = '<td></td>'
        answer_key += answer_code
        answer_ids += '<td></td>'
    answer_key += '</tr>'
    answer_ids += '</tr>'
    answer_key += '</table>'
    answer_ids += '</table>'

no = 1
for item_index in items_ids:
    print("-----------------> " + str(no))
    item = items[item_index]
    content += item.to_html(str(no))
    no += 1

template_html_test = template_html_test.replace('{ANSWER_TABLE}', answer_ids)
template_html_test = template_html_test.replace('{QUESTIONS}', content)
template_html_test = template_html_test.replace('{CODE}', test_code)
template_html_test = template_html_test.replace('{TITLE}', title)
template_html_test = template_html_test.replace('{DATE}', date)
template_html_test = template_html_test.replace('{MAX_POINTS}', str(len(items_ids)))

template_html_key = template_html_key.replace('{ANSWER_KEY}', answer_key)
template_html_key = template_html_key.replace('{CODE}', test_code)

file_test.write(str(template_html_test))
print('Test: ' + file_test_path)
file_key.write(str(template_html_key))
print('Key : ' + file_key_path)


