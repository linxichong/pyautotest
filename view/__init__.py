import yaml

with open('autotest.yml', encoding='utf-8') as cfg:
    config = yaml.load(cfg, Loader=yaml.SafeLoader)

with open('const.yml', encoding='utf-8') as cfg:
    const = yaml.load(cfg, Loader=yaml.SafeLoader)
