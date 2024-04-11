from crunge import imgui
from crunge.engine import Renderer

from imdemo.page import Page

'''
mGuiViewport* viewport = ImGui::GetMainViewport();
ImGui::SetNextWindowPos(viewport->Pos);
ImGui::SetNextWindowSize(viewport->Size);
ImGui::SetNextWindowViewport(viewport->ID);
ImGui::SetNextWindowBgAlpha(0.0f);

ImGuiWindowFlags window_flags = ImGuiWindowFlags_MenuBar | ImGuiWindowFlags_NoDocking;
window_flags |= ImGuiWindowFlags_NoTitleBar | ImGuiWindowFlags_NoCollapse | ImGuiWindowFlags_NoResize | ImGuiWindowFlags_NoMove;
window_flags |= ImGuiWindowFlags_NoBringToFrontOnFocus | ImGuiWindowFlags_NoNavFocus;

ImGui::PushStyleVar(ImGuiStyleVar_WindowRounding, 0.0f);
ImGui::PushStyleVar(ImGuiStyleVar_WindowBorderSize, 0.0f);
ImGui::PushStyleVar(ImGuiStyleVar_WindowPadding, ImVec2(0.0f, 0.0f));
ImGui::Begin("DockSpace Demo", p_open, window_flags);
ImGui::PopStyleVar(3);

ImGuiID dockspace_id = ImGui::GetID("MyDockspace");
ImGuiDockNodeFlags dockspace_flags = ImGuiDockNodeFlags_PassthruCentralNode;
ImGui::DockSpace(dockspace_id, ImVec2(0.0f, 0.0f), dockspace_flags);
'''

class DockingPage(Page):
    def reset(self):
        io = imgui.get_io()
        io.config_flags |= imgui.CONFIG_FLAGS_DOCKING_ENABLE

    def draw(self, renderer: Renderer):
        #gui.begin(self.title, True, imgui.WINDOW_FLAGS_DOCK_NODE_HOST)
        imgui.begin(self.title, True)

        dockspace_id = imgui.get_id(self.title)
        #ImGui::DockSpace(dockspaceID , ImVec2(0.0f, 0.0f), ImGuiDockNodeFlags_None|ImGuiDockNodeFlags_PassthruCentralNode/*|ImGuiDockNodeFlags_NoResize*/);
        #gui.dock_space(dockspace_id , imgui.Vec2(0., 0.), imgui.DOCK_NODE_FLAGS_NONE|imgui.DOCK_NODE_FLAGS_PASSTHRU_CENTRAL_NODE)
        dockspace_flags = imgui.DOCK_NODE_FLAGS_NONE|imgui.DOCK_NODE_FLAGS_PASSTHRU_CENTRAL_NODE
        #dockspace_flags = imgui.DOCK_NODE_FLAGS_NONE
        imgui.dock_space(dockspace_id , (0., 0.), dockspace_flags)

        imgui.end()


        #ImGui::SetNextWindowDockID(dockspaceID , ImGuiCond_FirstUseEver);
        imgui.set_next_window_dock_id(dockspace_id , imgui.COND_FIRST_USE_EVER)


        imgui.begin('Dockable Window')
        imgui.begin_child("region", (150, -50), border=True)
        imgui.text("inside region")
        imgui.end_child()
        imgui.text("outside region")
        imgui.end()
        super().draw(renderer)

def install(app):
    app.add_page(DockingPage, "docking", "Docking")
