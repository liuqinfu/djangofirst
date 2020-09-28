
from notify_setting import NOTIFY_LIST
import importlib

def sendAll():
    for path in NOTIFY_LIST:
        module_path,class_name = path.rsplit('.',maxsplit=1)
        module = importlib.import_module(module_path)
        class_obj = getattr(module, class_name)()
        class_obj.send()