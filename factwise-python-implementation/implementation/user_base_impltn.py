import user_base
import json
import implementation.utils as utils
from datetime import datetime
import implementation.load_data as load_data
import implementation.dump_data as dump_data
from tinydb import where
from tinydb.operations import set

class User():
  def __init__(self,name,display_name,description="Some description"):
    self.name = name
    self.display_name = display_name
    self.description = description
    self.creation_time = str(datetime.now())
    # self.user_data = load_data.user_data
    self.id = int(utils.get_serial_number())

  def get_data(self):
    result = {"name" : self.name,"description" : self.description,"id" : self.id, "display_name" : self.display_name, "creation_time":self.creation_time}
    return result

class user_base_impltn(user_base.UserBase):
    """
    Base interface implementation for API's to manage users.
    """
    def __init__(self):
        # self.user_data = load_data.user_data  # type dictionary it is
        # print(type(load_data.user_data))
        pass


    # create a user
    def create_user(self, request: str) -> str:
        json_object = json.loads(request)

        if len(json_object["name"]) > 64 or len(json_object["display_name"]) > 64: return str({"error" : "name and display name should not have more than 64 characters"})
        
        if not utils.is_name_unique(json_object["name"],"user_table"):
            return str({"error": "User name not unique, please give different and unique user name"})
        
        try:
          user = User(name = json_object["name"], display_name = json_object["display_name"], description =json_object["description"])
        except:
          user = User(name = json_object["name"], display_name = json_object["display_name"],description = "<description not given while creating user>" )
        load_data.user_table.insert(user.get_data())
        return str({"id" : user.get_data()["id"]})


    # list all users
    def list_users(self) -> str:
        response = []
        # response = [{"name":value["name"],"display_name":value["display_name"],"creation_time":value["creation_time"]} for value in self.user_data.values()]
        for user_data in load_data.user_table.all():
            response.append({"name":user_data["name"],"display_name":user_data["display_name"],"creation_time":user_data["creation_time"]})
        print(response)
        return response

    # describe user
    def describe_user(self, request: str) -> str:
        json_object = json.loads(request)
        if json_object["id"] == '': return str({"error" : "Please provide valid input"})
        user_data = load_data.user_table.search(where('id') == int(json_object["id"]))
        if len(user_data) == 0:
            print(str({"error" : "No such user found"}))
            return str({"error" : "No such user found"}) 
        user_data = user_data[0]
        return str({"name":user_data["name"],"description":user_data["description"],"creation_time":user_data["creation_time"]})

    # update user
    def update_user(self, request: str) -> str:
        json_object = json.loads(request)
        if not load_data.user_table.contains((where('id') == int(json_object["id"])) & (where('name') == json_object["user"]["name"])) : return str({"error":"No such user found"})
        # user_data = load_data.user_table.contains((where('id') == int(json_object["id"])) & (where('user')["name"] == json_object["name"]))
        # if len(user_data) == 0 :
        #     print("No such user found for updating the value")
        #     return str({"error":"No such user found"})
        load_data.user_table.update(set("display_name",json_object["user"]["display_name"]),where('id') == int(json_object["id"]))
        return str({"response" : "Value Updated Successfully"})

    def get_user_teams(self, request: str) -> str:
        json_object = json.loads(request)
        result = load_data.user_team_table.search(where('id') == int(json_object["id"]))
        if len(result) == 0: return str({"error" : "User is not found in any teams"})
        result = result[0]
        response = []
        temp = {}
        for team_id in result['teams']:
            team_data = load_data.team_table.search(where('id') == int(team_id))[0]
            temp["name"] = team_data["name"]
            temp["description"] = team_data["description"]
            temp["creation_time"] = team_data["creation_time"]
            response.append(temp)
        return str(response)
      # def load_user_data()