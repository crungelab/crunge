from loguru import logger

from crunge import imgui, imnodes

from imflo.wire import Wire

class Graph:
    def __init__(self):
        self.nodes = []
        self.node_map = {}
        self.wires = []
        self.wire_map = {}
        self.pins = []
        self.pin_map = {}

    def reset(self):
        for node in self.nodes:
            node.reset()

    def add_node(self, node):
        node.graph = self
        self.nodes.append(node)
        self.node_map[node.id] = node
        return node

    def remove_node(self, node):
        self.nodes.remove(node)
        self.node_map.pop(node.id)

    def add_wire(self, wire):
        self.wires.append(wire)
        self.wire_map[wire.id] = wire

    def remove_wire(self, wire):
        wire.destroy()
        self.wires.remove(wire)
        self.wire_map.pop(wire.id)

    def add_pin(self, pin):
        self.pins.append(pin)
        self.pin_map[pin.id] = pin

    def remove_pin(self, pin):
        pin.destroy()
        self.pins.remove(pin)
        self.pin_map.pop(pin.id)

    def connect(self, output, input):
        self.add_wire(Wire(output, input))

    def disconnect(self, wire):
        self.remove_wire(wire)

    def update(self, delta_time):
        for node in self.nodes:
            node.update(delta_time)

    def draw(self):
        imgui.begin('Node Editor')

        imnodes.begin_node_editor()

        for node in self.nodes:
            node.draw()
        for wire in self.wires:
            wire.draw()

        def cb (node, data):
            #print(node, data)
            pass

        cb_data = True
        imnodes.mini_map(.1, imnodes.MINI_MAP_LOCATION_TOP_LEFT, cb, cb_data)
        #imnodes.mini_map()
        imnodes.end_node_editor()

        if (result := imnodes.is_link_created(0,0))[0]:
            logger.debug(result)
            output = self.pin_map[result[1]]
            input = self.pin_map[result[2]]
            logger.debug('output:  {output}')
            logger.debug('input:  {input}')
            self.connect(output, input)

        if (result := imnodes.is_link_destroyed(0))[0]:
            wire = self.wire_map[result[1]]
            logger.debug('destroyed: ', wire)
            self.disconnect(wire)

        imgui.end()
