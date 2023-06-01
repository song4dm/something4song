import requests
import configparser
import csv

# https://developers.asana.com/reference/rest-api-reference Asana APIガイド
# https://app.asana.com/0/my-appsでAsana API Tokenを作る
# Get Asana Token
config = configparser.ConfigParser()
config.read("./config.ini", encoding="utf-8")
asana_access_token = config["TOKENS"]["ASANA_TOKEN"]
project_gid = config["PJ_INFORMATION"]["PROJECT_GID"]

base_url = "https://app.asana.com/api/1.0"
headers = {
    "Authorization": f"Bearer {asana_access_token}"
}

# Get tasks from a project 
# https://app.asana.com/api/1.0/projects/{project_gid}/tasks
def get_tasks_from_project(project_gid, base_url, headers):
    tasks_url = base_url + f"/projects/{project_gid}/tasks"
    response = requests.get(tasks_url, headers=headers)
    data = response.json()
    print(data)

# get_tasks_from_project(project_gid, base_url, headers)

# Get a task
# https://app.asana.com/api/1.0/tasks/{task_gid}
def get_one_task(task_gid, base_url, headers):
    tasks_url = base_url + f"/tasks/{task_gid}"
    response = requests.get(tasks_url, headers=headers)
    data = response.json()
    
    # print(data)
    # 各タスクの情報を取得してデータに追加
    # for task in data["data"]:
    #     print(task)
        # task_id = task["gid"]
        # task_name = task["name"]
        # task_assignee = task["assignee"]["name"] if task["assignee"] else ""
        # task_due_date = task["due_on"] if task.get("due_on") else ""
        # task_completed = task["completed"]
        # data.append([task_id, task_name, task_assignee, task_due_date, task_completed])
    
    # print(data["data"]["gid"])
    return data

# task_gid = "1204190146371062"
# get_one_task(task_gid, base_url, headers)

# Get tasks from a section
# https://app.asana.com/api/1.0/sections/{section_gid}/tasks
def get_tasks_from_section(section_gid, base_url, headers):
    tasks_url = base_url + f"/sections/{section_gid}/tasks"
    response = requests.get(tasks_url, headers=headers)
    data = response.json()
    # print(data)
    return data

# setcion_gid = "1203935568832439"
# get_tasks_from_section(setcion_gid, base_url, headers)


# Get sections in a project
# https://app.asana.com/api/1.0/projects/{project_gid}/sections
def get_sections_in_project(project_gid, base_url, headers):
    sections_url = base_url + f"/projects/{project_gid}/sections"
    response = requests.get(sections_url, headers=headers)
    data = response.json()
    # print(data)git 
    return data


    
def out_put_to_csv(data, file_name):
    with open(file_name, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerows(data)
    
# get_sections_in_project(project_gid, base_url, headers)

def get_backlog_tasks(project_gid, base_url, headers):
    print("get_backlog_tasks")
    sections = get_sections_in_project(project_gid, base_url, headers)
    backlog_gid = ""
    for task in sections["data"]:
        if task["name"] == "Backlog":
            print(task["gid"])
            backlog_gid = task["gid"]
    
    if backlog_gid != "":
        backlog_tasks = get_tasks_from_section(backlog_gid, base_url, headers)
        task_gids = []
        for task in backlog_tasks["data"]:
           task_gids.append(task["gid"]) 
        # print(task_gids)  
        task_infos = [] 
        for gid in task_gids:
            task_info = get_one_task(gid, base_url, headers)
            print(task_info["data"]["assignee"])
            if task_info["data"]["assignee"] != None:
                task_infos.append({"gid":gid, "task_name":task_info["data"]["name"],"assignee":task_info["data"]["assignee"]["name"]})
        # print(task_infos)    
    else:
        print("Backlog section not exists.")
    
    
            
# get_backlog_tasks(project_gid, base_url, headers)

def get_inquiry_tasks(project_gid, base_url, headers):
    print("get_inquiry_tasks")
    sections = get_sections_in_project(project_gid, base_url, headers)
    dme_sections_tag_list = ["Pending(every Friday check)", "Archive", "Done(Weekly)", "Done(Weekly)", "In Review", "In Progress", "Todo(This week)", "Backlog"]
    section_gid_list = []
    # get specified section gid
    for task in sections["data"]:
        if task["name"] in dme_sections_tag_list:
            section_gid = task["gid"]
            section_gid_list.append(section_gid)
            break
    print(section_gid_list)
    
    # get every section's task gid
    section_task_gid_list = []
    for section_gid in section_gid_list:
        section_tasks = get_tasks_from_section(section_gid, base_url, headers)
        for task in section_tasks["data"]:
            section_task_gid_list.append(task["gid"])    
    print(section_task_gid_list)
    
    task_detail_list = []
    # dme_inquiry_tag_list = ["問い合わせ(Jira)", "問い合わせ(Slack)"]
    for task_gid in section_task_gid_list:
        task_detail = get_one_task(task_gid, base_url, headers)
        for field in task_detail["data"]["custom_fields"]:
            if field["display_value"] is not None and "問い合わせ" in field["display_value"]:
                # print(field["display_value"])
                task_detail_list.append(task_detail)
    print(task_detail_list)
        
    # section_task_gid = ""
    # for task in sections["data"]:
    #     if task["name"] == "Backlog":
    #         print(task["gid"])
    #         section_task_gid = task["gid"]
    
    # if section_task_gid != "":
    #     backlog_tasks = get_tasks_from_section(section_task_gid, base_url, headers)
    #     task_gids = []
    #     for task in backlog_tasks["data"]:
    #        task_gids.append(task["gid"]) 
    #     # print(task_gids)  
    #     task_infos = [] 
    #     for gid in task_gids:
    #         task_info = get_one_task(gid, base_url, headers)
    #         print(task_info["data"]["assignee"])
    #         if task_info["data"]["assignee"] != None:
    #             task_infos.append({"gid":gid, "task_name":task_info["data"]["name"],"assignee":task_info["data"]["assignee"]["name"]})
    #     # print(task_infos)    
    # else:
    #     print("Backlog section not exists.")
    
get_inquiry_tasks(project_gid, base_url, headers)