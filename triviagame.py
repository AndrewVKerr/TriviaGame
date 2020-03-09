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
            "question" : <String>, # A question.
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