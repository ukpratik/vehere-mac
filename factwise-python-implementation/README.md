
### Team Project Planner Tool
This Project is designed and developed to manage users, teams, projects, tasks within the projects in an organization.


## Project Description
This Tool manages users users data, teams data, projects and tasks data.
It is build using python programming language completely.
Some non-builtin libiraries used in this project includes:
    abc
    tinydb

Json files are used as a database here.

## Explanation of the module
There are three base abstract classes defined in the module : 
    user_base
    team_base
    project_board_base
These abstract classes are implemented inside the implementation folder as:
    user_base_impltn
    team_base_impltn
    project_board_base_impltn

Apart from this there few other scripts are written in implementation folder using in those implented classes
    utils -> This file has several defined functions that are used for:
                - to check the field value is unique in the database
                - to get the id for the new entry in the tables of the database and updating it's value
                - to check the length of some of the input fields

    load_data -> This file is created for database related operations,

db Folder Contains the database of the application
In this project json files are used as the database
There are mainly three databases here:
    user_db
    team_db
    project_db

user_db -> this database is used to store the information of the users.
team_db -> this database is used to store the information of the team and the users in that team, admin of the team
project_db -> this database is used to store the information of the project, team assigned to the project, tasks within the project/project board, current status of the project, time interval of the project.            

## How to Use the module
To use this tool:
Create users first : create object of the user base implementation and use api to create the user, example as below:
#
    obj = user.user_base_impltn()
    obj.create_user('{"name" : "user1","display_name" : "spiderman", "description" : "full time employee"}')
#  

After this, similerly create team base implention object, create teams and add users to the team, e.g:
#
    objt = team.team_base_impltn()
    objt.create_team('{"name" : "team1","admin" : "uk4", "description" : "Threat intelligence team"}')
    print(objt.list_teams())
    objt.add_users_to_team('{"id" : "21","users" : ["user1","user2"]}')
# 

After creating the teams, project boards can be created and and task can be added to them as below:
#
    objp = project.project_base_impltn()
    objp.create_board('{"name" : "board_2","description" : "some description here - 2","team_id" : "t2"}')
    print(objp.list_boards('{"id" : "t2"}'))
    objp.add_task('{"title" : "board_1","description" : "make a task schedulee","team_id" : "t2"}')
#


## List of API's 
for User : 
    creat_user()
    list_users()
    describe_user()
    update_user()
    get_user_teams()


for Team :
    create_team()
    list_teams()
    describe_teams()
    update_team()
    add_users_to_team()
    remove_users_from_team()
    list_team_users()

for Project Board :
    create_board()
    close_board()
    add_task()
    update_task_status()
    list_boards()
    export_boards()


## Enhancements needed in this tool
    1. Validate the input that we are getting from the API's 
    2. Caching few of the data and updating it when some data is updated in the database (e.g users_names, team_names, project_names) because these list will repeatedly require to check. This will make the application faster.
    3. Logs should be collected for reference in future to debug the code or for forensic purposes.
    4. For Debugging purposes - blocks should be added with the debug level flag as condition and printing the values
    5. Configuration file should be included for few purposes like path of the database, path of the ouput file, setting the debugging level, caching the values,
    6. In the exported file, teams name could be added in place of id, all the team members for that assigned task could also be added for better information
    7. About creating the id for the entry in the tables of the database, these id should be different than just serial integer number, it can be string, whose prefix can be used determine the table or what kind of data this holds e.g ofr user id can be : user_98293882, also it is considered good if there is not any pattern for the id. So we can first create lot of random non-repeating ids and store in our database and later while we put new data in the database the id can be picked from this already created random ids. 
    8. Comments should be added to get brief explaination of the code
    9.more functions should be build to handle the task