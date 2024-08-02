from ..bitmask_type_renderer import BitmaskTypeRenderer


class BitmaskTypePyRenderer(BitmaskTypeRenderer):
    def render(self):
        enum_name = self.node.name.CamelCase()

        self.out << f"py::enum_<{enum_name}>(m, \"{enum_name}\", py::arithmetic())" << "\n"

        '''
        PYEXTEND_SCOPED_ENUM_BEGIN(wgpu::TextureUsage, TextureUsage)
            //TextureUsage.def(py::self | py::self); //Doesn't work
            TextureUsage.def("__or__", [](wgpu::TextureUsage& a, wgpu::TextureUsage& b) {
            return (wgpu::TextureUsage)(a | b);
                }, py::is_operator());
        PYEXTEND_END
        '''
        self.out.indent()

        for value in self.node.values:
            value_name = self.as_cppEnum(value.name)
            py_value_name = self.as_pyEnum(value.name)
            #self.out << f"{value_name} = WGPU{enum_name}_{suffix}," << "\n"
            self.out << f".value(\"{py_value_name}\", {enum_name}::{value_name})" << "\n"


        #self.out << ".export_values()"

        self.out(f"""
        .def("__or__", [](wgpu::{enum_name}& a, wgpu::{enum_name}& b) {{
            return (wgpu::{enum_name})(a | b);
        }}, py::is_operator());
        """)

        self.out.dedent()
        self.out << "\n"