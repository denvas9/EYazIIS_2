from tkinter import *
from tkinter import filedialog as fd

import nltk
from striprtf.striprtf import rtf_to_text

from help import HELPTEXT
import time

import nltk

GRAMMAR_RULES = r"""
        P: {<IN>}
        V: {<V.*>}
        N: {<S.*>}
        NP:{<PR>*<A.*|A-PRO><CONJ>*<A.*|A-PRO>*<N|NP>}   
        NP:{<A.*|A-PRO>*<S.*>+<A.*|A-PRO>*} 
        VP: {<V.*>+<NP|N>}
        VP: {<V.*>+<V.*>}

        """


def open_file():
    file_name = fd.askopenfilename(filetypes=[("rtf file", "*.rtf")])
    
    if file_name== None:
       return

    with open(file_name) as file:
        content = file.read()
        file_str = rtf_to_text(content)
        calculated_text.insert(1.0, file_str)

def info():
    children = Toplevel()
    children.title('Help')
    children.geometry("600x300+500+350")
    outputHelpText = Text(children, height=20, width=80)
    scrollb = Scrollbar(children, command=outputHelpText.yview)
    scrollb.grid(row=4, column=8, sticky='nsew')
    outputHelpText.grid(row=4, column=0, sticky='nsew', columnspan=3)
    outputHelpText.configure(yscrollcommand=scrollb.set)
    outputHelpText.insert('end', HELPTEXT)
    outputHelpText.configure(state='disabled')

def draw_tree():
    start = time.time()
    text = calculated_text.get(1.0, END)
    for symbol in ['\n',',','.',';',':','-']:
        text = text.replace(symbol, '')
    if text != '':
        doc = nltk.word_tokenize(text)
        doc = nltk.pos_tag(doc, lang='rus')
        new_doc = []
        for item in doc:
            new_doc.append(item)
        cp = nltk.RegexpParser(GRAMMAR_RULES)
        result = cp.parse(new_doc)
        print(type(result))
        print(result)
        result.draw()
    else:
        return
    end = time.time()
    print("Total time: {:.1f} ms.".format(end - start))
    

root = Tk()
root.title("Sentence parse tree")

root.resizable(width=False, height=False)
root.geometry("620x150+500+250")

label = Label(root, text='Input text:', font=("Times new roman", 13, "bold"))
label.grid(row=0, column=0)

calculated_text = Text(root, height=5, width=50)
calculated_text.grid(row=1, column=1, sticky='nsew', columnspan=2)

help_button = Button(text="Help", width=10, command=info)
help_button.grid(row=0, column=3)

open_button = Button(text="Open file", width=10, command=open_file)
open_button.grid(row=1, column=3)

ok_button = Button(text="Parse sentence", width=14, command=draw_tree)
ok_button.grid(row=2, column=3)

root.mainloop()