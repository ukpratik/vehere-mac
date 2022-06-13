from datetime import datetime
import project_board_base
import implementation.utils as utils
import implementation.load_data as load_data
from tinydb import where
from tinydb.operations import set
import json
import os

class Task():
    def __init__(self, board_name : str, description : str, team_id : str):
      self.title = str(board_name)
      self.description = str(description)
      self.team_id = team_id
      self.creation_time = str(datetime.now())
      self.status = "OPEN"
      self.id = int(utils.get_task_serial_number())
      # print(type(self.title))

    def get_data(self):
        result = {"title" : self.title,"description" : self.description,"id" : self.id, "team_id" : self.team_id, "creation_time":self.creation_time, "status":self.status}
        return result

class Project():
    
    def __init__(self,name,description,team_id):
        self.id = int(utils.get_project_serial_number())
        self.name = name
        self.description = description
        self.team_id = team_id
        self.creation_time = str(datetime.now())
        self.end_time = ''
        self.status = 'OPEN'
        # self.tasks = []

    def get_data(self):
      result = {"name" : self.name,"description" : self.description,"id" : self.id, "team_id" : self.team_id, "creation_time":self.creation_time, "end_time":self.end_time, "status":self.status}
      return result

class project_base_impltn(project_board_base.ProjectBoardBase):
    """
    A project board is a unit of delivery for a project. Each board will have a set of tasks assigned to a user.
    """

    # create a board
    def create_board(self, request: str):
        json_object = json.loads(request)
        
        if not utils.is_name_unique(json_object["name"],"project_table"):
            return str({"error": "Project name not unique, please give different and unique Project name"})
        if not load_data.team_table.contains(where("id") == json_object["team_id"]):
            return str({"error": "no such team is present"})
        if load_data.project_table.contains(where("team_id") == json_object["team_id"]) : 
            return str({"error":"team id is already present in one the project"})

        board = Project(name=json_object["name"], team_id=json_object["team_id"], description=json_object["description"])
        load_data.project_table.insert(board.get_data())
        load_data.board_list.insert({"id" : board.get_data()["id"],"name":board.get_data()["name"]})
        return str({"id" : board.get_data()["id"]})

    # close a board
    def close_board(self, request: str) -> str:
        json_object = json.loads(request)
        board = load_data.project_table.search(where('id') == int(json_object['id']))
        if len(board) == 1:
            board = board[0]
            tasks = load_data.task_table.search(where('title') == board['name'])
            for task in tasks:
              if task["status"] != "COMPLETE":
                  return "Can't close board, task : " + str(task["title"]) + "is NOT complete"
            board["status"] = "CLOSED"
            board["end_time"] = str(datetime.now())
            return "Board Closed Successfully!"
        return "Could not close board, multiple or no ids found"

    # add task to board
    def add_task(self, request: str) -> str:
        """
        :param request: A json string with the task details. Task is assigned to a user_id who works on the task
        {
            "title" : "<board_name>",
            "description" : "<description>",
            "team_id" : "<team id>"
            "creation_time" : "<date:time when task was created>"
        }
        :return: A json string with the response {"id" : "<task_id>"}

        Constraint:
         * task title must be unique for a board
         * title name can be max 64 characters
         * description can be max 128 characters

        Constraints:
        * Can only add task to an OPEN board
        """
        json_object = json.loads(request)

        new_task = Task(board_name = json_object['title'], description = json_object['description'], team_id = json_object['team_id'])
        
        board = load_data.project_table.search(where('name') == json_object['title'])
        
        if len(board) == 1: 
          board = board[0]
        else : 
          print('No board found')
          return str(["No such project title found"])

        # new_tasks = prev_tasks.append(new_task.get_data()['id'])
        load_data.task_table.insert(new_task.get_data())
        # load_data.project_table.update(set('tasks', new_tasks),where('name') == json_object["title"])
        return str({"id" : new_task.get_data()["id"]})

    # update the status of a task
    def update_task_status(self, request: str):
        """
        :param request: A json string with the user details
        {
            "id" : "<task_id>",
            "status" : "OPEN | IN_PROGRESS | COMPLETE"
        }
        """
        json_object = json.loads(request)
        load_data.task_table.update(set('status',json_object['status']), where('id') == int(json_object['id']))
        

    # list all open boards for a team
    def list_boards(self, request: str) -> str:
        """
        :param request: A json string with the team identifier
        {
          "id" : "<team_id>"
        }

        :return:
        [
          {
            "id" : "<board_id>",
            "name" : "<board_name>"
          }
        ]
        """
        json_object = json.loads(request)
        result = []
        for item in load_data.project_table.search(where('team_id') == json_object['id']):
            result.append({"id":item["id"], "name":item["name"]})
        return str(result)

    def export_board(self, request: str) -> str:
        """
        Export a board in the out folder. The output will be a txt file.
        We want you to be creative. Output a presentable view of the board and its tasks with the available data.
        :param request:
        {
          "id" : "<board_id>"
        }
        :return:
        {
          "out_file" : "<name of the file created>"
        }
        """
        json_object = json.loads(request)
        print(json_object)
        result = load_data.project_table.search(where('id') == int(json_object["id"]))
        
        if len(result) > 0:
            result = result[0]
        else:
            return str({"error" : "board id not found"})
        print(result)
        
        filename = str(os.path.join(os.path.dirname(__file__),"../out/Project_Board_id_" + str(result["id"]) + "_" + str(datetime.now().strftime("%d-%m-%Y-%H-%M-%S")) + ".txt"))
        with open(filename, "w") as file:
            file.write("######################## Project Board INFO #########################\n")
            file.write("\n")
            file.write("This INFO created at time : " + str(datetime.now()) + '\n')
            file.write("\n")
            file.write("PROJECT ID : " + str(result["id"]) + '\n')
            file.write("PROJECT NAME : " + str(result["name"]) + '\n')
            file.write("PROJECT DESCRIPTION : " + str(result["description"]) + '\n')
            file.write("PROJECT STARTED ON : " + str(result["creation_time"]) + '\n')
            if result["status"] == 'CLOSED':
                file.write("PROJECT ENDED ON : " + str(result["end_time"]) + '\n')
            else:
                file.write("PROJECT UNDER PROGRESS CURRENTLY" + '\n')
            file.write("\n")
            file.write("TASKS : " + '\n')
            file.write("\n")
            sr_num = 1
            for task in load_data.task_table.search(where('title') == result['name']):
                # task = load_data.task_table.search(where('id') == task_id)[0]
                file.write(str(sr_num) + " : \n")
                sr_num += 1
                file.write("\t Task Title : " + str(task['title']) + '\n')
                file.write("\t Task Description : " + str(task['description']) + '\n')
                file.write("\t Task Started on : " + str(task['creation_time']) + '\n')
                file.write("\t Task assigned to team : " + str(load_data.team_table.search(where('id') == task['team_id'])[0]['name']) + '\n\n\n')
            file.write("#####################################################################")
            return str({"out_file" : filename })