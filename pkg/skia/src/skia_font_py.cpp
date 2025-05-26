#include <iostream>
#include <limits>

#include <pybind11/pybind11.h>
#include <pybind11/functional.h>
#include <pybind11/stl.h>

#include <cxbind/cxbind.h>
#include <crunge/skia/crunge-skia.h>
#include <crunge/skia/conversions.h>

#include <include/core/SkFont.h>
#include <include/core/SkFontMgr.h>

#ifdef __APPLE__
#include "include/ports/SkFontMgr_mac_ct.h"
#endif

#ifdef __linux__
#include "include/ports/SkFontMgr_fontconfig.h"
#endif

#ifdef _WIN32
#include "include/ports/SkTypeface_win.h"
#endif

namespace py = pybind11;

namespace {

    bool g_factory_called = false;
    
    }  // namespace
    
    static sk_sp<SkFontMgr> fontmgr_factory() {
    #if defined(__APPLE__)
      return SkFontMgr_New_CoreText(nullptr);
    #elif defined(__linux__)
      return SkFontMgr_New_FontConfig(nullptr);
    #elif defined(_WIN32)
      return SkFontMgr_New_DirectWrite();
    #else
      return SkFontMgr_New_Custom_Empty(); /* last resort: SkFontMgr::RefEmpty(); */
    #endif
    }
    
    sk_sp<SkFontMgr> SkFontMgr_RefDefault() {
      static std::once_flag flag;
      static sk_sp<SkFontMgr> mgr;
      std::call_once(flag, [] {
        mgr = fontmgr_factory();
        g_factory_called = true;
      });
      return mgr;
    }    

void init_skia_font_py(py::module &_skia, Registry &registry) {
    PYEXTEND_BEGIN(SkFont, Font)

    _Font.def(py::init(
        [] () {
            auto warnings = pybind11::module::import("warnings");
            auto builtins = pybind11::module::import("builtins");
            warnings.attr("warn")(
                "\"Default font\" is deprecated upstream. Please specify name/file/style choices.",
                builtins.attr("DeprecationWarning"));
            return SkFont(SkFontMgr_RefDefault()->legacyMakeTypeface("", SkFontStyle()));
        }));

    PYEXTEND_END
}
