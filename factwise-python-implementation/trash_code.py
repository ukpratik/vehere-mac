

# for key,value in self.user_data.items():
#     if value["id"] == user_data["id"]:
#         return {"name" : value["name"], "description":value["description"], "creation_time":value["creation_time"]}
#     print("No such user found for describing the user")
#     return "error"

# try:
#     # user_data = json.loads(request)
#     # if len(user_data.keys()) != 2: return "Invalid input"
#     # if type(user_data["name"]) != str or len(user_data["name"]) > 64 : return "Invalid input"
#     # if type(user_data["display_name"]) != str or len(user_data["display_name"]) > 64: return "Invalid input"
#     # if user_data["name"] in self.user_data.keys(): 
#     #     print("User already exists")
#     #     return "User already exists"
#     pass
# except:
#     print("entered except")
#     return "Invalid input"

# user_table = open("./db/user_table.json",'a')
# json_object = json.loads(request)
# user = User(json_object["name"], json_object["display_name"], json_object["description"])
# print(str(user.get_data()))
# self.user_data[user.get_data()["name"]] = user.get_data()
# json_object = json.loads(str(user.get_data()).replace("'",'"'))
# json_object = json.dumps(json_object)
# user_table.write(json_object + '\n')
# user_table.close()


# user_data = json.loads(request)
#         for key,value in self.user_data.items():
#             if value["id"] == user_data["id"] and user_data["user"]["name"] == value["name"]:
#                 with open("./db/user_table.json", "r") as file:
#                     for line in file.readlines():
#                         if '"id": ' + str(value["id"]) + ',' in line :
#                             value["display_name"] = user_data["user"]["display_name"]
#                             # line = value
#                 return {"name" : value["name"], "description":value["description"], "creation_time":value["creation_time"]}
#             else:
#                 print("No such user found for updating the value")
#                 return "error"