# Generated from blox.mia by the Mia compiler. Do not edit.
import crunge.mia.runtime as rt


class Table(rt.Entity):
    pass


class Block(rt.Entity):
    pass


t_Table1 = rt.noun("Table1", Table)
t_Block1 = rt.noun("Block1", Block)
t_Block2 = rt.noun("Block2", Block)
t_Block3 = rt.noun("Block3", Block)
t_Active = rt.noun("Active")
t_bloxBrain = rt.verb("bloxAgent")
t_isClear = rt.verb("isClear")
t_onTop = rt.verb("onTop")
t_stack = rt.verb("stack")
t_blox = rt.verb("blox")
t_status = rt.verb("status")
t_clear = rt.verb("clear")
t_beneath = rt.verb("beneath")


class BloxAgent(rt.Agent):
    # blox.mia:8  agent BloxAgent
    predicates = {"isClear": bool}

    class BloxAgent(rt.Task):
        # blox.mia:12  def BloxAgent(/bloxAgent)
        trigger = rt.Trigger(rt.Attempt, rt.Perform, t_bloxBrain)

        def bind(self, msg):
            return True

        def resume(self, agent, result=None):
            match self.pc:
                case 0:
                    _k = rt.Context()
                    _k.add(rt.Belief(t_Table1, t_isClear, True))
                    _k.add(rt.Belief(t_Block1, t_onTop, t_Table1))
                    _k.add(rt.Belief(t_Block2, t_onTop, t_Block1))
                    _k.add(rt.Belief(t_Block3, t_onTop, t_Block2))
                    _k.add(rt.Belief(t_Block3, t_isClear, True))
                    _k.add(rt.Perform(rt.SELF, t_stack, t_Block1, {"on": t_Block2}))
                    _k.add(rt.Perform(rt.SELF, t_stack, t_Block2, {"on": t_Block3}))
                    self.c_BloxContext = _k
                    self.pc = 1
                    return agent.post(rt.Attempt(rt.Perform(rt.SELF, t_blox, None, {"context": self.c_BloxContext})), self)
                case 1:
                    if not result.succeeded:
                        return self.fail(agent)
                    return self.succeed(agent)

    class Blox(rt.Agent):
        # blox.mia:33  expert Blox

        class Blox(rt.Task):
            # blox.mia:35  def Blox(/blox)
            trigger = rt.Trigger(rt.Attempt, rt.Perform, t_blox)

            def bind(self, msg):
                return True

            def resume(self, agent, result=None):
                return self.succeed(agent)

        class Impasse(rt.Task):
            # blox.mia:38  def Impasse(impasse)
            trigger = rt.IMPASSE

            def bind(self, msg):
                return True

            def resume(self, agent, result=None):
                ctx = agent.context
                _m0 = []
                for _c0 in ctx.find(rt.Belief, rt.ANY, t_status, t_Active):
                    v_g = _c0.subj
                    if isinstance(v_g, rt.Goal):
                        _m0.append((v_g,))
                for (v_g,) in _m0:
                    agent.propose(rt.Attempt(v_g))
                if not _m0:
                    return agent.halt()
                return self.succeed(agent)

        class GoalElab(rt.Task):
            # blox.mia:46  def GoalElab(+ Goal $g)
            trigger = rt.Trigger(rt.Assert, rt.Goal, None)

            def bind(self, msg):
                _c = msg.clause
                self.v_g = _c
                return True

            def resume(self, agent, result=None):
                agent.post(rt.Assert(rt.Belief(self.v_g, t_status, t_Active)))
                return self.succeed(agent)

        class NotGoalElab(rt.Task):
            # blox.mia:49  def NotGoalElab(- Goal $g)
            trigger = rt.Trigger(rt.Retract, rt.Goal, None)

            def bind(self, msg):
                _c = msg.clause
                self.v_g = _c
                return True

            def resume(self, agent, result=None):
                agent.post(rt.Retract(rt.Belief(self.v_g, t_status, t_Active)))
                return self.succeed(agent)

        class Stack(rt.Task):
            # blox.mia:52  def Stack(/stack $x on: $y -> $g)
            trigger = rt.Trigger(rt.Attempt, rt.Perform, t_stack)

            def bind(self, msg):
                _c = msg.clause
                self.v_x = _c.obj
                if "on" not in _c.slots:
                    return False
                self.v_y = _c.slots["on"]
                self.v_g = _c
                return True

            def resume(self, agent, result=None):
                ctx = agent.context
                _m0 = []
                if not ctx.exists(rt.Belief, self.v_x, t_isClear, True):
                    _m0.append(())
                for _ in _m0:
                    agent.post(rt.Attempt(rt.Perform(rt.SELF, t_clear, self.v_x)))
                if _m0:
                    return self.return_(agent)
                _m1 = []
                if not ctx.exists(rt.Belief, self.v_y, t_isClear, True):
                    _m1.append(())
                for _ in _m1:
                    agent.post(rt.Attempt(rt.Perform(rt.SELF, t_clear, self.v_y)))
                if _m1:
                    return self.return_(agent)
                _m2 = []
                for _c0 in ctx.find(rt.Belief, self.v_x, t_onTop, rt.ANY):
                    v_z = _c0.obj
                    _m2.append((v_z,))
                for (v_z,) in _m2:
                    agent.post(rt.Retract(rt.Belief(self.v_x, t_onTop, v_z)))
                agent.post(rt.Assert(rt.Belief(self.v_x, t_onTop, self.v_y)))
                agent.post(rt.Retract(self.v_g))
                return self.succeed(agent)

        class Clear(rt.Task):
            # blox.mia:76  def Clear(/clear $x)
            trigger = rt.Trigger(rt.Attempt, rt.Perform, t_clear)

            def bind(self, msg):
                _c = msg.clause
                self.v_x = _c.obj
                return True

            def resume(self, agent, result=None):
                ctx = agent.context
                _m0 = []
                for _c0 in ctx.find(rt.Belief, self.v_x, t_beneath, rt.ANY):
                    v_y = _c0.obj
                    for _c1 in ctx.find(rt.Belief, rt.ANY, t_isClear, True):
                        v_z = _c1.subj
                        if v_z != self.v_x:
                            if v_z != v_y:
                                _m0.append((v_y, v_z))
                for (v_y, v_z) in _m0:
                    agent.propose(rt.Attempt(rt.Perform(rt.SELF, t_stack, v_y, {"on": v_z})))
                return self.succeed(agent)

        class NotOnTopElab(rt.Task):
            # blox.mia:85  def NotOnTopElab(- $x onTop $y)
            trigger = rt.Trigger(rt.Retract, rt.Belief, t_onTop)

            def bind(self, msg):
                _c = msg.clause
                self.v_x = _c.subj
                self.v_y = _c.obj
                return True

            def resume(self, agent, result=None):
                agent.post(rt.Retract(rt.Belief(self.v_y, t_beneath, self.v_x)))
                agent.post(rt.Assert(rt.Belief(self.v_y, t_isClear, True)))
                return self.succeed(agent)

        class OntopElab(rt.Task):
            # blox.mia:89  def OntopElab(+ $x onTop $y)
            trigger = rt.Trigger(rt.Assert, rt.Belief, t_onTop)

            def bind(self, msg):
                _c = msg.clause
                self.v_x = _c.subj
                self.v_y = _c.obj
                return True

            def resume(self, agent, result=None):
                ctx = agent.context
                _m0 = []
                for _c0 in ctx.find(rt.Belief, self.v_y, t_isClear, True):
                    if isinstance(self.v_y, Block):
                        _m0.append(())
                for _ in _m0:
                    agent.post(rt.Retract(rt.Belief(self.v_y, t_isClear, True)))
                _m1 = []
                for _c1 in ctx.find(rt.Belief, self.v_x, t_onTop, self.v_y):
                    _m1.append(())
                for _ in _m1:
                    agent.post(rt.Assert(rt.Belief(self.v_y, t_beneath, self.v_x)))
                return self.succeed(agent)

        boot = Blox
        rules = (Impasse, GoalElab, NotGoalElab, Stack, Clear, NotOnTopElab, OntopElab)
        experts = ()

    boot = BloxAgent
    rules = ()
    experts = (Blox,)
