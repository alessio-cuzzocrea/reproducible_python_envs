from doit.action import CmdAction
import yaml

def task_export_installed_packages():
    return {
        'actions': ["conda env export --no-builds -f .tmp-deps.yml"],
        'verbosity': 2,
        'targets': [".tmp-deps.yml"]
    }

def task_check_installed_packages():
    def get_yamls():
        with open(".tmp-deps.yml", 'r') as tmp_dep,\
             open("dependencies.yml", 'r') as my_deps:
                yaml_tmp_dep = set(yaml.safe_load(tmp_dep)["dependencies"])
                yaml_my_deps = set(yaml.safe_load(my_deps)["dependencies"])
                print("uninstalled dependencies: ", yaml_my_deps - yaml_tmp_dep)
                with open("conda_to_be_installed", "w") as outfile:
                    yaml.dump({"dependencies": list(yaml_my_deps - yaml_tmp_dep)}, outfile)

    return {
        'actions': [get_yamls],
        'verbosity': 2,
        "targets": ["conda_to_be_installed"]
    }

def task_install_packages():
    def get_deps():
        with open("conda_to_be_installed", "r") as deps:
            deps = yaml.safe_load(deps)["dependencies"]
            list_= list(map(lambda x: f"conda install -y {x.replace('=','==')}", deps))
            if len(list_) > 0:
                return list_
            return "echo env up to date"

    return {
            'actions': [CmdAction(get_deps)],
            'verbosity': 2,
            'file_dep': ["conda_to_be_installed"]
        }
