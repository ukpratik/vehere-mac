import json

def dump_user_data(data: dict):
    user_table = open("./db/user_table.json",'a')
    # self.user_data[user.get_data()["name"]] = user.get_data()
    for key, value in data.items():
        json_object = json.loads(str(value).replace("'",'"'))
        json_object = json.dumps(json_object)
        user_table.write(json_object + '\n')
    user_table.close()