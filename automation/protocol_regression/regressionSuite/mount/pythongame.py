import os
import Label
def create_widgets(self):
    """ Create widgets to get story information and to display story. """
    # create instruction label
    Label(self,  text = "Enter information for a new story").grid(row = 0, column = 0, columnspan = 2, sticky = W)
# create a label and text entry for the name of a person
Label(self,
      text = "Person: "
      ).grid(row = 1, column = 0, sticky = W)
 
self.person_ent = Entry(self)
self.person_ent.grid(row = 1, column = 1, sticky = W)
# create a label and text entry for a plural noun
Label(self,
      text = "Plural Noun:"
      ).grid(row = 2, column = 0, sticky = W)
self.noun_ent = Entry(self)
self.noun_ent.grid(row = 2, column = 1, sticky = W)
# create a label and text entry for a verb
Label(self,
      text = "Verb:"
      ).grid(row = 3, column = 0, sticky = W)
self.verb_ent = Entry(self)
self.verb_ent.grid(row = 3, column = 1, sticky = W)
# create a label for adjectives check buttons
Label(self,
      text = "Adjective(s):"
      ).grid(row = 4, column = 0, sticky = W)
# create itchy check button
self.is_itchy = BooleanVar()
Checkbutton(self,
             text = "itchy",
             variable = self.is_itchy
             ).grid(row = 4, column = 1, sticky = W)
# create joyous check button
self.is_joyous = BooleanVar()
Checkbutton(self,
             text = "joyous",
             variable = self.is_joyous
             ).grid(row = 4, column = 2, sticky = W)
# create electric check button
self.is_electric = BooleanVar()
Checkbutton(self,
             text = "electric",
             variable = self.is_electric
             ).grid(row = 4, column = 3, sticky = W)
# create a label for body parts radio buttons
Label(self,
      text = "Body Part:"
      ).grid(row = 5, column = 0, sticky = W)
# create variable for single body part
self.body_part = StringVar()
# create body part radio buttons
body_parts = ["bellybutton", "big toe", "medulla oblongata"]
 
column = 1
for part in body_parts:
    Radiobutton(self,
                 text = part,
                 variable = self.body_part,
                 value = part
                 ).grid(row = 5, column = column, sticky = W)
    column += 1
# create a submit button
Button(self,
        text = "Click for story",
        command = self.tell_story
        ).grid(row = 6, column = 0, sticky = W)
self.story_txt = Text(self, width = 75, height = 10, wrap = WORD)
self.story_txt.grid(row = 7, column = 0, columnspan = 4)

