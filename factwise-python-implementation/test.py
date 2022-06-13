import implementation.user_base_impltn as user
import implementation.team_base_impltn as team
import implementation.project_board_base_impltn as project

if __name__ == "__main__":
    obj = user.user_base_impltn()
    obj.create_user('{"name" : "user1","display_name" : "spiderman", "description" : "full time employee"}')
    obj.create_user('{"name" : "user3","display_name" : "batman", "description" : "full time employee"}')
    obj.create_user('{"name" : "user5","display_name" : "joker", "description" : "full time employee"}')
    print(obj.list_users())

    # print("---------x---------")
    objt = team.team_base_impltn()
    print(objt.create_team('{"name" : "team1","admin" : "1", "description" : "Threat intelligence team"}'))
    print(objt.list_teams())
    print("---------x---------")
    print(objt.add_users_to_team('{"id" : "1","users" : ["2"]}'))


    objp = project.project_base_impltn()
    print(objp.create_board('{"name" : "board_1","description" : "some description here - 2","team_id" : 1}'))
    print(objp.list_boards('{"id" : "1"}'))
    print(objp.add_task('{"title" : "board_1","description" : "make a task schedulee","team_id" : 1}'))
    print(objp.export_board('{"id" : 1}'))
    
    print(" ========== Describe user ==========")
    print(obj.describe_user('{"id" : "1"}'))
    print(" ========== update user ==========")
    print(obj.update_user('{"id" : "1","user" : {"name" : "user1","display_name" : "pinkman"}}'))
    print(" ========== get user teams ==========")
    print(obj.get_user_teams('''{
          "id" : "2"
        }'''))

    print(" ========== describe team ==========")
    print(objt.describe_team('''{
          "id" : "1"
        }'''))
    
    print(" ========== list team users ==========")
    print(objt.list_team_users('{"id":"1"}'))

    print(" ========== update team ==========")
    print(objt.update_team('''{
          "id" : "1",
          "team" : {
            "name" : "team1",
            "description" : "some updated description here",
            "admin": "2"
          }
        }'''))

    print(" ========== remove team users ==========")
    print(objt.remove_users_from_team('''{
          "id" : "1",
          "users" : ["1"]
        }'''))

    print(" ========== update task status ==========")
    print(objp.update_task_status('''{
            "id" : "1",
            "status" : "COMPLETE"
        }'''))
    print(objp.close_board('{"id":"1"}'))
    print(objp.export_board('{"id" : 1}'))