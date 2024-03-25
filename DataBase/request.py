import requests
import yaml
import pprint as pp


def info_creating():
    with open("config_example.yaml", "r") as file:
        self_config_ = yaml.load(file, Loader=yaml.FullLoader)
    simulator_type_ = 'benign'
    return self_config_, simulator_type_


self_config, simulator_type = info_creating()


def preparing_task_dict():
    task_list_for_db = set()
    assignee_key = list(self_config["assignee"].keys())[0]
    for elem in self_config["assignee"][assignee_key]:
        index = elem[elem.rfind('/rf_')+4:elem.rfind('_rgb')]
        task_list_for_db.add(index)
    task_list_for_db = list(task_list_for_db)
    tasks_for_db_ = {
        'project': self_config['project'],
        'task_list': task_list_for_db
    }
    return tasks_for_db_


tasks_for_db = preparing_task_dict()
pp.pprint(tasks_for_db)

# db_indexes = requests.get("/PATH/")
# post_status = requests.post(f"PATH/filling/{simulator_type}", json=db_indexes)

"""
params = {
    "name": "Aleksei",
    "surname": "Kozharin",
    "age": 77,
    "registration_date": "2022-01-01"
}


resp = requests.post("http://127.0.0.1:8000/user/validate", json=params)
print(resp.json())


paramm = {'name': 'AL'}

resp = requests.post("http://127.0.0.1:8000/user", params=paramm)
pprint.pprint(resp.text)

r = requests.get("/PATH/") # метод get
r_post = requests.post("/PATH/", json = {'name': 'Aleksei'}) # метод post

"""
