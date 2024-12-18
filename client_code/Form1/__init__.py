from ._anvil_designer import Form1Template
from anvil import *
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import anvil.tables as tables
import anvil.tables.query as q
import anvil.js
from anvil.tables import app_tables

# Ich habe es doch nicht mithilfe von anvil_extras gemacht,
# da ich es ziemlich schwierig fand auf eine Lösung zu kommen.
# ChatGPT hat auch nicht großartig geholfen. :(
# Aber ich habe es am Ende doch noch mit den Sessions es geschafft.

class Form1(Form1Template):
    def __init__(self, **properties):
      # Set Form properties and Data Bindings.
      self.init_components(**properties)
      self.secON = False
      # Any code you write here will run before the form opens.
      state = anvil.server.call('get_login_state')
      if state is True:
        open_form('Form2')

    def BtnLogin_click(self, **event_args):
      username = self.TBUsername.text
      passwort = self.TBPassword.text
      Resultpage = open_form('Form2')
      Resultpage.lblOutput.text = anvil.server.call("get_user", username, passwort, self.secON)

    def check_box_1_change(self, **event_args):
      """This method is called when this checkbox is checked or unchecked"""
      if self.check_box_1.checked:
        self.secON = True
      
      

    

    

    