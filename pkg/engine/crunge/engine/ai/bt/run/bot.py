from typing import List

from copy import copy
from collections import defaultdict
from uuid import uuid1
from loguru import logger

from ..run import _impasse
from .task import Task, Status
from .act import *
from .context import Context


class Bot(Sequence):
    def __init__(self):
        super().__init__()
        self.id = uuid1()
        self.ctx = Context()
        self.tasks: List[Task] = []
        self.posts: List[Message] = []
        self.proposals: List[Message] = []
        self.scheduled: bool = False
        self.impassed: bool = False
        self.signals = defaultdict(list)

        # A bot is its own bot, so the whole subtree inherits a valid
        # reference through Task.add and Task.create.
        self.bot = self

    def broadcast(self, msg: Message):
        m = copy(msg)
        logger.debug("Broadcast:\t{}", m)
        m.sender = self
        self.post(m)
        for t in self.tasks:
            t.broadcast(m)
        return m

    def post(self, msg: Message):
        if not msg.sender:
            msg.sender = self
        logger.debug("Post:\t{}", msg)
        return self.posts.append(msg)

    def fork(self, t: Task):
        logger.debug("Fork:\t{}", t.msg)
        child = Bot()
        child.ctx = self.ctx.copy()
        child.runner = self.runner
        child.add(t)
        child.schedule()
        return child

    def dispatch(self, msg: Message):
        T = type(msg)
        if T is Propose:
            logger.debug("* \t{}", msg)
            pmsg = Attempt()
            pmsg.update(msg)

            self.proposals.append(pmsg)
            return
        elif T is Assert:
            logger.debug("+ \t{}", msg)
            self.ctx.add(msg.data)
            return self.fire(msg)
        elif T is Retract:
            logger.debug("- \t{}", msg)
            self.ctx.remove(msg.data)
            return self.fire(msg)
        else:
            logger.debug("Eval:\t{}", msg)
            return self.fire(msg)

    def fire(self, msg: Message):
        for m in msg.sender.match_rules(msg):
            logger.debug("Fire:\t{}:", m)
            self.schedule_task(m.rule.action, m)

    async def main(self, msg=None):
        status = await super().main(msg)
        if status is Status.FAILURE:
            return status
        logger.debug("@main {}", self.id)

        posts = self.posts
        self.posts = []
        for post in posts:
            self.dispatch(post)

        if self.idle() and self.impasse() and not self.scheduled:
            for msg in self.proposals:
                for m in msg.sender.match_rules(msg):
                    self.fork(m.to)

        self.proposals = []
        self.status = Status.SUCCESS

        return self.status

    def idle(self):
        return len(self.posts) == 0 and len(self.tasks) == 0

    def signal(self, trigger, task):
        logger.debug(trigger.verb)
        self.signals[trigger.verb].append(task)

    def impasse(self):
        if self.impassed:
            return True
        logger.debug("@impasse {}", self.id)
        self.impassed = True
        self.post(Attempt(Achieve(None, _impasse, None)))
        return False