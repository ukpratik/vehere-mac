import team_base
import implementation.load_data as load_data
import implementation.utils as utils
from datetime import datetime
import json
from tinydb.operations import delete, add, set
from tinydb import where

class Team():
    def __init__(self, name: str, description: str, admin : int, users:list = []):
      self.name = name
      self.description = description
      self.admin = int(admin)
      self.creation_time = str(datetime.now())
      self.id = int(utils.get_team_serial_number())
      if admin in users:
        users.remove(admin)
      self.users = users
      self.users.append(int(admin))
      

    
    def get_data(self):
      result = {"name" : self.name,"description" : self.description,"id" : self.id, "admin" : self.admin, "creation_time":self.creation_time, "users":self.users}
      return result

class team_base_impltn(team_base.TeamBase):
    """
    Base interface implementation for API's to manage teams.
    For simplicity a single team manages a single project. And there is a separate team per project.
    Users can be
    """

    # create a team
    def create_team(self, request: str) -> str:
        # validate and sanitize 
        json_object = json.loads(request)

        if not utils.is_name_unique(json_object["name"],"team_table"):
            return str({"error": "Team name not unique, please give different and unique team name"})

        team = Team(name=json_object["name"], admin=int(json_object["admin"]), description=json_object["description"])
        load_data.team_table.insert(team.get_data())
        load_data.user_team_table.insert({"id" : int(json_object["admin"]),"name" : load_data.user_table.search(where('id') == int(json_object["admin"]))[0]['name'], "teams" : [int(team.get_data()['id'])]})
        return str({"id" : team.get_data()["id"]})

    # list all teams
    def list_teams(self) -> str:
        team_list = []
        print(load_data.team_table.all())
        for row in load_data.team_table.all():
          temp_dict = {}
          temp_dict["name"] = row["name"]
          temp_dict["description"] = row["description"]
          temp_dict["creation_time"] = row["creation_time"]
          temp_dict["admin"] = row["admin"]
          team_list.append(temp_dict)
        return str(team_list)


    # describe team
    def describe_team(self, request: str) -> str:
        json_object = json.loads(request)
        result = load_data.team_table.search(where('id') == int(json_object["id"]))
        if len(result) == 0:
            return str({"error":"No such team is present"})
        result = result[0]
        return str({"name" : result["name"], "description" : result["description"], "creation_time" : result["creation_time"], "admin" : result["admin"]})


    # update team
    def update_team(self, request: str) -> str:
        json_object = json.loads(request)
        team_data = load_data.team_table.search((where('id') == json_object["id"]) and (where('name') == json_object["team"]["name"]))
        if len(team_data) == 0:
            print("No such team found for updating the value")
            return str({"error":"No such team found"})
        # print(team_data)
        team_data = team_data[0]
        if int(json_object["team"]["admin"]) not in team_data['users']:
            new_team = team_data['users'].append(int(json_object['team']["admin"]))
            load_data.team_table.update(set("users",new_team),where('id') == int(json_object["id"]))
            # update in user_team_table
            if not load_data.user_team_table.contains(where('id') == int(json_object['team']["admin"])):
                load_data.user_team_table.insert({"id" : int(json_object['team']["admin"]),"name" : load_data.user_table.search(where('id') == int(json_object['team']["admin"]))[0]['name'], "teams" : [int(json_object['id'])]})
            else:
                utt = load_data.user_team_table.search(where('id') == int(json_object['team']["admin"]))[0]
                if int(json_object["id"]) not in utt['teams']:
                    temp = utt['teams'].append(int(json_object["id"]))
                    load_data.user_team_table.update(set("teams",temp),where('id') == int(json_object['team']["admin"]))

        load_data.team_table.update(set("description",json_object['team']["description"]),where('id') == int(json_object["id"]))
        load_data.team_table.update(set("admin",int(json_object['team']["admin"])),where('id') == int(json_object["id"]))
        return str({"response" : "Value Updated Successfully"})


    # add users to team
    def add_users_to_team(self, request: str):
        json_object = json.loads(request)
        # validate the request data
        new_users = json_object["users"]
        if load_data.team_table.contains(where("id") == int(json_object["id"])):
            existing_users = load_data.team_table.search(where('id') == int(json_object["id"]))[0].get("users")
            for user in new_users:
                if not load_data.user_table.contains(where('id') == int(user)) : 
                    print(str({"error" : "invalid user id, no such user found, skipping this userd_id"}))
                    continue 
                    # return str({"error" : "invalid user id, no such user found"})
                
                if int(user) not in existing_users:
                    existing_users.append(int(user))

        else:
          return str({"error":"no such team found"})
        load_data.team_table.update(set("users",existing_users)),load_data.team_query.id == int(json_object["id"])
        # Do not add admin or same users again

        # Add team information to the user_team_table in user_db database also
        for user in new_users:
            user_data = load_data.user_table.search(where('id') == int(user))
            if len(user_data) == 0 :
                print(str({"error" : "invalid user id, no such user found, skipping this userd_id"}))
                continue 
                # return str({"error" : "invalid user id, no such user found"})
            user_data = user_data[0]
            if load_data.user_team_table.contains(where("id") == user_data['id']):
              existing_teams = load_data.user_team_table.search(where('id') == int(user))[0]["teams"]
              if int(json_object["id"]) not in existing_teams:
                  existing_teams.append(int(json_object["id"]))
                  load_data.user_team_table.update(set("teams",existing_teams),where("id") == int(user))
            else:
              load_data.user_team_table.insert({"id" : int(user),"name" : user_data['name'], "teams" : [int(json_object["id"])]})
        
        return str({"response" : "users : " + str(new_users) + " added successfully to team : " + str(json_object["id"])})



    # add users to team
    def remove_users_from_team(self, request: str):
        try:
          json_object = json.loads(request)
          data = load_data.team_table.search(where('id') == int(json_object["id"]))[0]
          admin = data["admin"]
          existing_users = data.get("users")
          remove_users = json_object["users"]
          for user in remove_users:
              if int(user) == int(admin):
                  print("Warning : Can't remove admin, first change the admin from the team.")
                  continue
              existing_users.remove(int(user))
              utt_existing_teams = load_data.user_team_table.search(where('id') == int(user))[0].get('teams')
              try:
                  utt_existing_teams.remove(int(json_object["id"]))
              except:
                  print("team id can't be removed from the user team table teams list")
              load_data.user_team_table.update(set("teams",utt_existing_teams),where('id') == int(user))
          load_data.team_table.update(set("users",existing_users)),where('id') == int(json_object["id"])
          
          return "Users : " + str(existing_users) + ", REMOVED SUCCESSFULLY from team id : " + str(json_object["id"])
        except:
          print("Users : " + str(remove_users) + ", CANNOT be removed from team id : " + str(json_object["id"]))
          return "Users : " + str(remove_users) + ", CANNOT be removed from team id : " + str(json_object["id"])

    # list users of a team
    def list_team_users(self, request: str):
        json_object = json.loads(request)
        if not load_data.team_table.contains(where('id') == int(json_object["id"])): return str({"error":"no such team found"})
        user_ids = load_data.team_table.search(where('id') == int(json_object["id"]))[0].get("users")
        response = []
        for user_id in user_ids:
          user_data = load_data.user_table.search(where('id') == int(user_id))[0]
          response.append({"id":user_data['id'],"name":user_data['name'],"display_name":user_data['display_name']})
        return response
