#!/usr/bin/python3
# Andrew Kerr
# 3/9/2020

'''
--==[ Description ]==--
This file will contain a game that is capable of allowing a user to select a trivia category from 5 different categories - history, geography, music, games, random.
Once a category is selected it will display question after question, showing the correct answer(s) between each question.
Once the category is completed a score will be produced from the number of correct questions, this score will be compared to a high score board.
If the score is higher than an existing score it will be added to the high scores.

--==[ The Model ]==--
The model for this game will be stored in a dictionary format.
{
   "questions" : {
      "history" : [
         {
            "question_text" : <String>, # A question.
            "answers" : [...], # A list of answers, can be anything however will be converted to string when displayed. 
            "correct_answer" : <Integer> # Indicates which index from answers is the correct one. 
         },
         ...
      ],
      ...
   },
   "high_scores" : {
      "history" : [
         {
            "name" : <String>,
            "value" : <Integer>
         },
         ...
      ],
      ...
   }
}

--==[ View/Flow ]==--
+> MainMenu (tk.Frame)
|-+> Title (tk.Label)
| |-+> __init__
| | |--> self
| | |--> text = "Trivia Game"
| |
| |-+> Grid
|   |--> row = 1
|   |--> column = 0
|   |--> sticky = "news"
|   |--> columnspan = 3
|
|-+> Play (tk.Button)
| |-+> [On Click]
| | |--> Create a popup for the SelectCategoryFrame frame.
| | |--> Withdraw MainMenu window.
| |
| |-+> Grid
|   |--> row = 3
|   |--> column = 1
|   |--> sticky = "news"
|
|-+> High Scores (tk.Button)
| |-+> [On Click]
| | |--> Create a popup for the HighScoreFrame frame.
| | |--> Withdraw MainMenu window.
| |
| |-+> Grid
|   |--> row = 4
|   |--> column = 1
|   |--> sticky = "news"
|
|-+> Quit (tk.Button)
| |-+> [On Click]
| | |--> Exit
| |
| |-+> Grid
|   |--> row = 5
|   |--> column = 1
|   |--> sticky = "news"
|
|-+> Grid
| |--> row = 0
| |--> column = 0
| |--> sticky = "news"
|
|-+> grid_columnconfigure
| |--> 0, weight = 1
| |--> 1, weight = 1
| |--> 2, weight = 1
|
|-+> grid_rowconfigure
  |--> 0, weight = 1
  |--> 2, weight = 1
  |--> 6, weight = 1
'''

import tkinter as tk
from tkinter import messagebox as mb
from tkinter.scrolledtext import ScrolledText
import pickle
import random

class Model(object):
    
    def __init__(self):
        self.raw_model = {}
        self.questions = {}
        self.highscores = {}
        
        self.categories = []
        
        try:
            self.load()
        except:
            self.load_defaults()
            self.save()
        
    def load(self):
        datafile = open("data.pickle","rb")
        self.raw_model = pickle.load(datafile)
        datafile.close()
        
        self.questions = self.raw_model["questions"]
        self.highscores = self.raw_model["highscores"]
        for key in self.questions.keys():
            self.categories.append(key)
        
    def load_defaults(self):
        self.raw_model = {"questions":{},"highscores":{}}
        self.questions = self.raw_model["questions"]
        for category in ["history","geography","music","games"]:
            self.questions[category] = []
        
        self.questions["history"].append(
            Question(category="history",question_text="How much wood can a wood chuck chuck if a wood chuck could chuck wood?",
                     answers=[7,20,"No",None],correct_answer=2)
        )
        
        self.questions["geography"].append(
            Question(category="geography",question_text="Where is Missouri?",
                     answers=["Im in misery.","Below Kansas", "Florida", "West Virginia"],correct_answer=1)
        )        
        self.highscores = self.raw_model["highscores"]
    
    def save(self):
        datafile = open("data.pickle","wb")
        pickle.dump(self.raw_model,datafile)
        datafile.close()        
        
class Question(object):
    
    def __init__(self,category="UNSET",question_text="UNSET",answers=[None],correct_answer=0):
        self.category=category
        self.question_text = question_text
        self.answers = answers
        self.correct_answer = correct_answer
        
    '''Creates a QuestionFrame object using the information stored in this object.'''
    def prompt_question(self,next_question=None,master=None):
        master_ = master or Window(previous=TriviaGame.GUI.main_menu.master)
        master_.title("Trivia Question ["+self.category+"]")
        frame = QuestionFrame(master_,question=self)
        frame.grid(row=0,column=0,sticky="news")
        master_.grid_columnconfigure(0,weight=1)
        master_.grid_rowconfigure(0,weight=1)
        return frame
        
        
class Gui(object):
        
    def start(self):
        self.root = Window()
        self.root.title("TriviaGame")
        self.root.geometry("300x200")
        
        self.main_menu = MainMenu(master=self.root)
        self.main_menu.grid(row=0,column=0,sticky="news")
        
        self.root.grid_columnconfigure(0,weight=1)
        self.root.grid_rowconfigure(0,weight=1)
        
        self.root.mainloop()
    

'''
 Window(tk.Tk)
 A class that extends tk.Tk, used to override the destroy command so that the window is withdrawn instead of destroyed. When the window withdraws the previous window
 will be brought back.'''
class Window(tk.Tk):
    
    def __init__(self,previous=None,*args,**kwargs):
        tk.Tk.__init__(self,*args,**kwargs)
        self.previous = previous
        
    def destroy(self):
        if self.previous == None:
            exit()
        self.previous.update()
        self.previous.deiconify()
        self.withdraw()
    
class MainMenu(tk.Frame):
    
    def __init__(self,master=None):
        tk.Frame.__init__(self,master)
        
        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1,weight=1)
        self.grid_columnconfigure(2,weight=1)
        
        self.grid_rowconfigure(0,weight=1)
        
        self.lbl_title = tk.Label(self,text="Trivia Game")
        self.lbl_title.grid(row=1,column=0,columnspan=3,sticky="ews")
        
        self.grid_rowconfigure(2,weight=1)
        
        self.btn_start = tk.Button(self,text="Start Game",command=self.start_game)
        self.btn_start.grid(row=3,column=1,sticky="ews")
        
        self.btn_highscores = tk.Button(self,text="Highscores",command=self.goto_highscores)
        self.btn_highscores.grid(row=4,column=1,sticky="ews")        
        
        self.grid_rowconfigure(5,weight=1)
        self.create_category_frame()
    
    def create_category_frame(self):
        master = Window(previous=self.master)
        master.title("Category Selection")
        master.geometry("300x200")
        self.frm_category_select = CategorySelectionFrame(master)
        self.frm_category_select.grid(row=0,column=0,sticky="news")
        master.grid_columnconfigure(0,weight=1)
        master.grid_rowconfigure(0,weight=1)
        master.withdraw()

    def show(self):
        self.master.update()
        self.master.deiconify()

    def start_game(self):
        self.master.withdraw()
        self.frm_category_select.master.update()
        self.frm_category_select.master.deiconify()
    
    def goto_highscores(self):
        pass

class CategorySelectionFrame(tk.Frame):
    
    def __init__(self,master=None):
        tk.Frame.__init__(self,master)
        
        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1,weight=1)
        self.grid_columnconfigure(2,weight=1)
        
        self.grid_rowconfigure(0,weight=1)
        
        self.lbl_title = tk.Label(self,text="Select a Category:")
        self.lbl_title.grid(row=1,column=0,columnspan=3,sticky="news")
        
        self.tkvar_selected_category = tk.StringVar(self)
        self.tkvar_selected_category.set(TriviaGame.MODEL.categories[0])
        
        self.dbx_category_selection = tk.OptionMenu(self,self.tkvar_selected_category,*TriviaGame.MODEL.categories)
        self.dbx_category_selection.grid(row=2,column=1,sticky="ews")
        
        self.ent_amount = tk.Entry(self)
        self.ent_amount.insert(tk.END,"10")
        self.ent_amount.grid(row=3,column=1,sticky="ews")
        
        self.btn_select = tk.Button(self,text="Select",command=self.select)
        self.btn_select.grid(row=4,column=1,sticky="ews")
        
        self.grid_rowconfigure(5,weight=1)
        
    def select(self):
        self.master.withdraw()
        questions_dict = TriviaGame.MODEL.questions
        selection = self.tkvar_selected_category.get()
        
        questions_list = questions_dict[selection]
        
        game = TriviaGame.GAME
        game.correct_questions = 0
        try:
            size = int(self.ent_amount.get())
        except:
            size = 10
        
        if size > len(questions_list):
            size = len(questions_list)
        
        game.total_questions = size
        
        game.queued_questions = random.choices(questions_list,k=size)
        question = game.next_question()
        if question == None:
            game.end_game()
        else:
            question.prompt_question()
        

class QuestionFrame(tk.Frame):
    
    def __init__(self,master=None,question=None):
        tk.Frame.__init__(self,master)
        
        self.question_text = question.question_text or "UNSET"
        self.answers = question.answers or [None]
        self.correct_answer = question.correct_answer or 0
        
        self.grid_rowconfigure(0,weight=1)
        
        self.scr_question_text = ScrolledText(self,width=40,height=8)
        self.scr_question_text.insert(0.0,self.question_text)
        self.scr_question_text.grid(row=1,column=0,columnspan=3,sticky="nws")
        
        self.tkvar_chosen_answer = tk.StringVar(self)
        self.rad_answers_dictionary = {}
        
        self.grid_rowconfigure(2,weight=1)
        
        r = 3
        for answer in self.answers:
            rad_answer = tk.Radiobutton(self,variable=self.tkvar_chosen_answer,value=str(answer),text=str(answer))
            rad_answer.grid(row=r,column=1,sticky="nws")
            self.rad_answers_dictionary[str(answer)] = rad_answer
            r+=1
            
        self.grid_rowconfigure(r,weight=1)
        
        r+=1
        self.btn_quit = tk.Button(self,text="Quit",command=self.exit_quiz)
        self.btn_quit.grid(row=r,column=0,sticky="news")
        
        self.lbl_response = tk.Label(self,text="")
        self.lbl_response.grid(row=r,column=1,sticky="ews")        
        
        self.btn_select = tk.Button(self,text="Select",command=self.select_answer)
        self.btn_select.grid(row=r,column=2,sticky="news")
        
        r+=1
        self.grid_columnconfigure(r,weight=1)
        
        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1,weight=1)
        self.grid_columnconfigure(2,weight=1)
        
    def exit_quiz(self):
        if TriviaGame.GAME.end_game():
            self.master.destroy()
    
    def select_answer(self):
        answer = self.tkvar_chosen_answer.get()
        if answer == '':
            answer = "None"
        
        correct = self.answers[self.correct_answer]
        if answer == correct:
            rad_selected = self.rad_answers_dictionary[answer]
            rad_selected.configure(bg="green")
            self.lbl_response.configure(text="Correct",fg="green")
            TriviaGame.GAME.correct_questions += 1
        else:
            rad_selected = self.rad_answers_dictionary[answer]
            rad_selected.configure(bg="red")
            rad_correct = self.rad_answers_dictionary[correct]
            rad_correct.configure(bg="green")  
            self.lbl_response.configure(text="Wrong Answer",fg="red")
            
        self.btn_select.configure(text="Next Question",command=self.next_question)
    
    def next_question(self):
        game = TriviaGame.GAME
        #Get next question, if not found then end the game.
        next_question = game.next_question()
        if next_question != None:
            next_question.prompt_answer()
        else:
            game.end_game()
        tk.Tk.destroy(self.master)
    

class ScoreFrame(tk.Frame):
    
    def __init__(self,master=None):
        tk.Frame.__init__(self,master)
        
        self.grid_columnconfigure(0,weight=1)
        self.grid_columnconfigure(1,weight=1)
        self.grid_columnconfigure(2,weight=1)
        
        self.grid_rowconfigure(0,weight=1)
        
        try:
            self.score = (TriviaGame.GAME.correct_questions/TriviaGame.GAME.total_questions)*100.0
        except ZeroDivisionError:
            self.score = 100.0
        
        msg = ""
        if self.score >= 100:
            msg = "You scored a perfect [100%]!"
        else:
            msg = "You scored a ["+str(self.score)+"%]"
        
        self.lbl_title = tk.Label(self,text=msg)
        self.lbl_title.grid(row = 1, column = 0, columnspan = 3, sticky="news")
        
        self.grid_rowconfigure(2,weight=1)
        
        self.lbl_enter_initials = tk.Label(self,text="Enter Initials:")
        self.lbl_enter_initials.grid(row=3,column=1,sticky="s")
        
        self.tkvar_name = tk.StringVar(self)
        
        def limit_length_to_3(*args):
            value = self.tkvar_name.get()
            if len(value) > 3:
                self.tkvar_name.set(value[:3])
        
        self.tkvar_name.trace('w', limit_length_to_3)
        
        self.ent_name = tk.Entry(self,textvariable=self.tkvar_name,width=5)
        self.ent_name.grid(row=4,column=1,sticky="n")
        
        self.grid_rowconfigure(5,weight=1)
        
        self.btn_main_menu = tk.Button(self,text="MainMenu",command=self.goto_mainmenu)
        self.btn_main_menu.grid(row=6,column=1,sticky="news")
        
    def goto_mainmenu(self):    
        self.master.destroy()
        
    def show_score(master=None):
        root = master or Window(previous=TriviaGame.GUI.root)
        root.title("You scored...")
        root.geometry("300x200")
        
        frame = ScoreFrame(master=root)
        frame.grid(row=0,column=0,sticky="news")
        
        root.grid_columnconfigure(0,weight=1)
        root.grid_rowconfigure(0,weight=1)
        return frame

"""
 Game(object)
 Keeps track of the currently running game.
 Seperated from the model as this data will not be stored.
 Seperated from the gui as this doesnt display anything to the user.
"""        
class Game(object):
    
    def __init__(self):
        self.correct_questions = 0
        self.total_questions = 0
        self.queued_questions = []
        self.current_question = None
        
    def next_question(self):
        if len(self.queued_questions) == 0:
            self.current_question = None
            return None
        
        question = self.queued_questions.pop(0)
        self.current_question = question
        return question
    
    def end_game(self):
        if self.current_question != None:
            answer = mb.askyesno(title="Quit Quiz?",message="There are still questions left, are you sure you wish to quit?")
            if answer == False:
                return False
        else:
            ScoreFrame.show_score()
        return True
        
class TriviaGame(object):
    MODEL=Model()
    GUI=Gui()
    GAME=Game()
        
#main
if __name__ == "__main__":
    TriviaGame.GUI.start()