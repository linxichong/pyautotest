
import yaml

class Const:
    def __init__(self):
        with open('const.yaml', encoding='utf-8') as const_cfg:
            self.values = yaml.load(const_cfg, Loader=yaml.SafeLoader)

    def get_const_val(self, val):
        if val in self.values:
            return self.values[val]
        return val

    def repalce_const_val(self, obj):
        for key in obj:
            val = obj[key]
            if val in self.values:
                obj[key] = self.values[val]

        return obj