from ..game_entity import GameEntity

from .dna import WyggleDna

#from .agents.reactive import ReactiveWyggleAgent
from .mind import WyggleMind


class WyggleSeg(GameEntity):
    dna: WyggleDna

    def __init__(self, dna):
        super().__init__(dna)
        self.next = None
        self.track = None
        self.track_ndx = 0
        self.track_max = 256
        self.on_track = False

    def put_on_track(self, track):
        self.track = track
        self.on_track = True
        self.position = track[self.track_ndx]

    def move(self):

        self.position = self.track[self.track_ndx]
        self.track_ndx += 1
        if self.track_ndx >= self.track_max:
            self.track_ndx = 0

        # else if there is a next segment and not on the track yet...
        if self.next and self.track_ndx > 16 and not self.next.on_track:
            self.next.put_on_track(self.track)


class WyggleTail(WyggleSeg):
    def __init__(self, dna):
        super().__init__(dna)
        self.name = WyggleDna.gen_id(self.kind)
        self.model = self.dna.tail_sprite


class WyggleHead(WyggleSeg):
    def __init__(self, dna):
        super().__init__(dna)
        self.face = "happy"

    def happy_face(self):
        self.face = "happy"
        self.model = self.dna.happy_face_sprite

    def munchy_face(self):
        self.face = "munchy"
        self.model = self.dna.munchy_face_sprite

    def open_mouth(self):
        self.munchy_face()

    def close_mouth(self):
        self.happy_face()


#
class Wyggle(WyggleHead):
    def __init__(self):
        super().__init__(WyggleDna(Wyggle))
        self.name = WyggleDna.gen_id(self.kind)
        self.length_max = 6
        self.segs: list[WyggleSeg] = []
        self.model = self.dna.happy_face_sprite

        self.track = [0] * self.track_max * 2
        self.length = 1
        self.butt = None

        """
        self.agent = ReactiveWyggleAgent(self)
        self.agent.schedule()
        """
        self.mind = WyggleMind()
        self.add(self.mind)

    def _create(self):
        super()._create()
        for i in range(self.length_max - 1):
            self.grow()

    def grow(self):
        length = len(self.segs)
        if length >= self.length_max:
            return
        seg = WyggleTail(self.dna)
        seg.position = self.position
        self.layer.attach(seg)
        self.segs.append(seg)
        self.length = length = len(self.segs)
        seg.z = -0.001 * length

        was_butt = self.butt
        self.butt = seg
        if was_butt != None:
            was_butt.next = self.butt
        else:
            self.next = self.butt

    def move(self, position):
        self.track[self.track_ndx] = position
        # super().move()
        for seg in self.segs:
            if seg.on_track:
                seg.move()
        super().move()
