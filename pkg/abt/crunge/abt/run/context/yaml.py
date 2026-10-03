import yaml

from .context import Context

class YamlContext(Context):
    def load(self, filename):
        data = None
        with open(filename) as f:
            data = yaml.load(f, Loader=yaml.FullLoader)
            print(data)

        self.from_json(data)
        return self

yamlcontext_ = lambda cfg=None: YamlContext().config(cfg)
