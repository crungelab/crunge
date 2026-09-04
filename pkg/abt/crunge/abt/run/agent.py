from typing import List

from copy import copy
from collections import defaultdict
from uuid import uuid1
from loguru import logger

from . import _impasse
from .task import Task, Status
from .act import *
from .context import Context


class Agent(Sequence):
    def __init__(self, proposal: Propose = None):
        super().__init__(msg=proposal)
        self.id = uuid1()
        self.ctx = Context()
        self.tasks: List[Task] = []
        self.posts: List[Message] = []
        self.proposals: List[Message] = []
        self.scheduled: bool = False
        self.impassed: bool = False
        self.signals = defaultdict(list)

        # An agent is its own agent, so the whole subtree inherits a valid
        # reference through Task.add and Task.create.
        self.agent = self

        if proposal:
            attempt = Attempt(proposal.data, proposal.sender, proposal.to)
            self.posts.append(attempt)

    def broadcast(self, msg: Message):
        m = copy(msg)
        logger.debug("Broadcast:\t{}", m)
        # m.sender = self
        self.post(m)
        for t in self.tasks:
            t.broadcast(m)
        return m

    def post(self, msg: Message) -> None:
        if not msg.sender:
            msg.sender = self
        if isinstance(msg, Propose):
            logger.debug("Propose:\t{}", msg)
            self.proposals.append(msg)
        else:
            logger.debug("Post:\t{}", msg)
            self.posts.append(msg)

    def fork(self, proposal: Propose) -> None:
        logger.debug("Fork:\t{}", proposal)
        child = Agent(proposal)
        child.ctx = self.ctx.copy()
        child.runner = self.runner
        child.schedule()

    def dispatch(self, msg: Message) -> bool:
        match msg:
            case Assert():
                logger.debug("+ \t{}", msg)
                self.ctx.add(msg.data)

            case Retract():
                logger.debug("- \t{}", msg)
                self.ctx.remove(msg.data)

            case _: # Attempt() | Propose() | _:
                logger.debug("Eval:\t{}", msg)

        return super().dispatch(msg)

    async def main(self, proposal=None):
        status = await super().main(proposal)
        if status is Status.FAILURE:
            return status
        logger.debug("@main {}", self.id)

        posts = self.posts
        self.posts = []
        for post in posts:
            self.dispatch(post)

        if self.idle() and self.impasse() and not self.scheduled:
            for proposal in self.proposals:
                self.fork(proposal)

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
