import anvil.files
from anvil.files import data_files
import anvil.tables as tables
import anvil.tables.query as q
from anvil.tables import app_tables
import anvil.server
import sqlite3
import urllib.parse

@anvil.server.callable
def get_login_state():
  if "login" not in anvil.server.session:
    anvil.server.session["login"] = False
  return anvil.server.session["login"]
  
@anvil.server.callable
def get_user(username, pwd, secON):
  conn = sqlite3.connect(data_files['userData.db'])
  cursor = conn.cursor()
  if secON:
    query = "SELECT username FROM Users WHERE username = ? AND password = ?"
  else:
    query = f"SELECT username FROM Users WHERE username = '{username}' AND password = '{pwd}'"
  acc_noQuery = f"SELECT AccountNo FROM Users WHERE username = '{username}' AND password = '{pwd}'"
  userQuery = f"SELECT username FROM Users WHERE username = '{username}'"
  print(query)
  try:
    if secON:
      data = list(cursor.execute(query, (username, pwd)))
    else:
      data = list(cursor.execute(query))
    acc_no = list(cursor.execute(acc_noQuery))
    user = list(cursor.execute(userQuery))
    print(data)
    if len(acc_no) > 0:
      acc_no = acc_no[0][0]
    print(acc_no)
    if len(user) > 0:
      user = user[0][0]
    print(user)
    if data == []:
      return f"Login failed\nSELECT username FROM Users WHERE username = '{username}' AND password = '{pwd}'"
    if acc_no and username == user:
      return f"Welcome {username}!"
    elif data != [] and username != user:
      anvil.server.session["login"] = True
      return f"Login successful but AccountNo was not passed\nSELECT username FROM Users WHERE username = '{username}' AND password = '{pwd}'"
  except Exception as e:
    print(e)
    return f"Login failed\nSELECT username FROM Users WHERE username = '{username}' AND password = '{pwd}'"
    
  conn.close()

def get_query_params(url):
  # Ich weis nicht ob man das mit den Abständen berücksichtigen sollte, aber habe es trotzdem zum teil
  # in der url darf kein anderes get property stehen außer AccountNo sonst wird programm verwirrt
  accNoWithSpaceAfter = "AccountNo "
  accNoNoSpace = "AccountNo"
  query_string = url.split('?')[-1] if '?' in url else ''
  if query_string:
    query_params = urllib.parse.parse_qs(query_string[-1])
    print(query_params)
    if accNoWithSpaceAfter in query_params:
      return query_params["AccountNo "][0]
    elif accNoNoSpace in query_params:
      return query_params["AccountNo"][0]
  return None
  
@anvil.server.callable
def get_data_accountno(url):
  AccountNo = get_query_params(url)
  
  conn = sqlite3.connect(data_files["userData.db"])
  cursor = conn.cursor()
  if AccountNo:
    # Query the balance and user details based on AccountNo
    query_balance = f"SELECT balance FROM Balances WHERE AccountNo = {AccountNo}"
    query_user = f"SELECT username FROM Users WHERE AccountNo = {AccountNo}"
    try:
      balance = cursor.execute(query_balance).fetchall()
      user = cursor.execute(query_user).fetchall()
    except Exception as e:
      return f"User not found.<br>{query_user}<br>{query_balance}<br>{e}"
    # formatting start
    user = [u[0] for u in user if isinstance(u, tuple)]
    balance = [b[0] for b in balance if isinstance(b, tuple)]
    user = user[0] if len(user) == 1 else user
    balance = balance[0] if len(balance) == 1 else balance
    # formatting end
    if user:
      return f"Welcome {user}! Your balance is {balance}."
    else:
      return f"User not found.<br>{query_user}<br>{query_balance}"

    return "Login successful but 'AccountNo' was not passed."
    
@anvil.server.callable
def logout():
  anvil.server.session["login"] = False