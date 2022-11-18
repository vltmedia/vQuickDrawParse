
# Turns a dictionary into a class
class DictClass(object):
    def __init__(self, my_dict):
        for key in my_dict:
            setattr(self, key, my_dict[key])