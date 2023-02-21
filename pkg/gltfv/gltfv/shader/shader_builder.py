from ..builder import Builder


class ShaderBuilder(Builder):
    def __init__(self, shader_code: str) -> None:
        super().__init__()
        self.shader_code = shader_code
        self.indentation = 0

    def __call__(self, line=""):
        if len(line):
            self.shader_code += ' ' * self.indentation * 4
            self.shader_code += line.replace('>>', '> >')
        self.shader_code += '\n'

    def __enter__(self):
        self.indent()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.dedent()

    def indent(self):
        self.indentation +=1

    def dedent(self):
        self.indentation -=1
