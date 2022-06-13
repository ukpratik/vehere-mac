import json
from tinydb import TinyDB, Query
from tinydb.operations import delete, add
import os

team_db = TinyDB(os.path.join(os.path.dirname(__file__),"../db/team_db.json"))
team_query = Query()
team_table = team_db.table('team_table')

project_db = TinyDB(os.path.join(os.path.dirname(__file__),"../db/project_db.json"))
project_table = project_db.table('project_table')
board_list = project_db.table('board_list')
task_table = project_db.table('task_table')

user_db = TinyDB(os.path.join(os.path.dirname(__file__),"../db/user_db.json"))
user_table = user_db.table('user_table')
user_team_table = user_db.table('user_team_table')



# Ignore Below functions, those were build for different approaches which are implemented

# class Load_Data():

    # def __init__(self):
    #     self.user_data = {}

# user_data = {}
# team_data = {}
# board_data = {}

# def load_user_data():
#     user_table_lines = open("./db/user_table.json",'r').read().split('\n')
#     for line in user_table_lines:
#         if line == '' : continue
#         user_json_line = json.loads(line)
#         user_data[user_json_line["name"]] = user_json_line
    
# def load_team_data():
#     team_table_lines = open("./db/team_table.json",'r').read().split('\n')
#     for line in team_table_lines:
#         if line == '' : continue
#         team_json_line = json.loads(line)
#         team_data[team_json_line["name"]] = team_json_line

# def load_board_data():
#     team_board_lines = open("./db/board_table.json",'r').read().split('\n')
#     for line in team_board_lines:
#         if line == '' : continue
#         board_json_line = json.loads(line)
#         board_data[board_json_line["name"]] = board_json_line

# load_user_data()

#     if __name__ == '__main__':
#         user_data = {}