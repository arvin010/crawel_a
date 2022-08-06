import os,shutil

platform_dir={1:"amazon",2:"aliexpress"}



def move_file(data,file_name):
    if data["save_dir"]:
        target_dir=""
        for dir in [data["save_dir"],platform_dir[data["platform"]],data["shop"],data["country"]]:
            target_dir=os.path.join(target_dir,dir)
            if not os.path.exists(target_dir):
                os.mkdir(target_dir)
        shutil.move(os.path.join(data["default_dir"],file_name),os.path.join(target_dir,file_name))