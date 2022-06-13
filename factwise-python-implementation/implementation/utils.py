import json
import implementation.load_data as load_data
from tinydb import where

# def is_str():
#     pass

# API's for USER database related functions
def get_serial_number() -> int:
    num = ''
    try:
        # with open(os.path.join())
        with open("./db/user_serial_number.txt", "r") as file:
            num = file.read()
    except FileNotFoundError:
        with open("./db/user_serial_number.txt",'w') as file:
            file.write('')
    if(num == ''): num = 1
    with open("./db/user_serial_number.txt", "w") as file :
        file.write(str(int(num) + 1))
    return int(num)

def update_serial_number(num : int):
    open("./db/serial_number.txt", "w").write(str(num + 1))

def create_user_input_validate(data : str) -> str:
    try:
        user_data = json.loads(data)
        if len(user_data.keys()) != 2: return "Invalid input: input data unexpected"
        if type(user_data["name"]) != str or len(user_data["name"]) > 64 : return "Invalid input : username length exceed"
        if type(user_data["display_name"]) != str or len(user_data["display_name"]) > 64: return "Invalid input : display_name length exceed"
        
    except Exception:
        print("entered except")
        return "Invalid input"

def check_user_exists(user_data):
    if user_data["name"] in load_data.user_data.keys(): 
        print("User already exists")
        return "User already exists"


# API's for TEAM database related functions
def get_team_serial_number() -> int:
    num = ''
    try:
        # with open(os.path.join())
        with open("./db/team_serial_number.txt", "r") as file:
            num = file.read()
    except FileNotFoundError:
        with open("./db/team_serial_number.txt",'w') as file:
            file.write('')
    if(num == ''): num = 1
    with open("./db/team_serial_number.txt", "w") as file :
        file.write(str(int(num) + 1))
    return int(num)


# API's for PROJECT database related functions
def get_project_serial_number() -> int:
    num = ''
    try:
        # with open(os.path.join())
        with open("./db/project_serial_number.txt", "r") as file:
            num = int(file.read())
    except FileNotFoundError:
        with open("./db/project_serial_number.txt",'w') as file:
            file.write('')
    except:
        print("Error during file opening project_serial_number.txt")
    if(num == ''): num = 1
    with open("./db/project_serial_number.txt", "w") as file :
        file.write(str(int(num) + 1))
    return int(num)

# API's for PROJECT-TASK database related functions
def get_task_serial_number() -> int:
    num = ''
    try:
        # with open(os.path.join())
        with open("./db/task_serial_number.txt", "r") as file:
            num = file.read()
    except FileNotFoundError:
        with open("./db/task_serial_number.txt",'w') as file:
            file.write('')
    except:
        print("Error during file opening project_serial_number.txt")
    if(num == ''): num = 1
    with open("./db/task_serial_number.txt", "w") as file :
        file.write(str(int(num) + 1))
    return int(num)



# Check Uniqueness : funtion
def is_name_unique(name,table) -> bool:
    res = False
    if table == "team_table":
        res = load_data.team_table.contains(where("name") == name)
    elif table == "user_table":
        res = load_data.user_table.contains(where("name") == name)
    elif table == "project_table":
        res = load_data.project_table.contains(where("name") == name)
    else:
        print("Error : Unknown table name")
        return False
    if res:
        print("INFO : " + str(name) + " is NOT UNIQUE in the database table : " + str(table))
        return False
    else:
        return True

def is_valid_input(request : str) -> bool:
    pass

def valid_length(value : str, length : int)->bool:
    if len(value) > length:
        return False
    return True