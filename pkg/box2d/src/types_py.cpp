#include <limits>
// #include <iostream>

#include <pybind11/functional.h>
#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include <cxbind/callback.h>
#include <cxbind/cxbind.h>

#include <crunge/box2d/conversions.h>
#include <crunge/box2d/crunge-box2d.h>

#include <box2d/box2d.h>


namespace py = pybind11;

py::list GetBeginEvents(b2ContactEvents events) {
    py::list result;
    for (int i = 0; i < events.beginCount; i++) {
        result.append(
            events.beginEvents[i]); // pybind11 copies each element by value
    }
    return result;
}

py::list GetEndEvents(b2ContactEvents events) {
    py::list result;
    for (int i = 0; i < events.endCount; i++) {
        result.append(events.endEvents[i]);
    }
    return result;
}

py::list GetHitEvents(b2ContactEvents events) {
    py::list result;
    for (int i = 0; i < events.hitCount; i++) {
        result.append(events.hitEvents[i]);
    }
    return result;
}

void init_types_py(py::module &_box2d, Registry &registry) {
    PYEXTEND_BEGIN(b2ContactEvents, ContactEvents)
    _ContactEvents.def("get_begin_events", &GetBeginEvents)
                  .def("get_end_events", &GetEndEvents)
                  .def("get_hit_events", &GetHitEvents)
    ;

    PYEXTEND_END
}