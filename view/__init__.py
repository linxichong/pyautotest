import yaml

with open('autotest.yaml', encoding='utf-8') as cfg:
    config = yaml.load(cfg, Loader=yaml.SafeLoader)

with open('const.yaml', encoding='utf-8') as cfg:
    const = yaml.load(cfg, Loader=yaml.SafeLoader)
