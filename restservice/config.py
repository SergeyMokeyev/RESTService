import os
import yaml


class Config:
    def __init__(self, file):
        self.env = os.environ.get('ENVIRONMENT')
        with open(file) as f:
            self.config = yaml.safe_load(f)

    def __getattr__(self, item):
        return os.environ.get(item.upper()) or self.config.get(self.env, {}).get(item)
