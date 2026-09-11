# Generated from counting.mia by the Mia compiler. Do not edit.
import crunge.mia.runtime as rt


t_Active = rt.noun("Active")
t_countingBrain = rt.verb("countingAgent")
t_countTo = rt.verb("countTo")
t_value = rt.verb("value")
t_counting = rt.verb("counting")
t_status = rt.verb("status")
t_increment = rt.verb("increment")


class CountingAgent(rt.Agent):
    # counting.mia:5  agent CountingAgent
    predicates = {"countTo": int, "value": int}

    class CountingAgent(rt.Task):
        # counting.mia:10  def CountingAgent(/countingAgent)
        trigger = rt.Trigger(rt.Attempt, rt.Perform, t_countingBrain)

        def bind(self, msg):
            return True

        def resume(self, agent, result=None):
            match self.pc:
                case 0:
                    _k = rt.Context()
                    _h = rt.Perform(rt.SELF, t_countTo, 5)
                    _k.add(_h)
                    _k.add(rt.Belief(_h, t_value, 0))
                    self.c_CountingContext = _k
                    self.pc = 1
                    return agent.propose(rt.Attempt(rt.Perform(rt.SELF, t_counting, None, {"context": self.c_CountingContext})), self)
                case 1:
                    if not result.succeeded:
                        return self.fail(agent)
                    return self.succeed(agent)

    class Counting(rt.Deliberator):
        # counting.mia:18  expert Counting(Deliberator)

        class Counting(rt.Task):
            # counting.mia:20  def Counting(/counting)
            trigger = rt.Trigger(rt.Attempt, rt.Perform, t_counting)

            def bind(self, msg):
                return True

            def resume(self, agent, result=None):
                print("Counting in sub-contexts")
                return self.succeed(agent)

        class Impasse(rt.Task):
            # counting.mia:23  def Impasse(impasse)
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
            # counting.mia:31  def GoalElab(+ Goal $g)
            trigger = rt.Trigger(rt.Assert, rt.Goal, None)

            def bind(self, msg):
                _c = msg.clause
                self.v_g = _c
                return True

            def resume(self, agent, result=None):
                agent.post(rt.Assert(rt.Belief(self.v_g, t_status, t_Active)))
                return self.succeed(agent)

        class NotGoalElab(rt.Task):
            # counting.mia:34  def NotGoalElab(- Goal $g)
            trigger = rt.Trigger(rt.Retract, rt.Goal, None)

            def bind(self, msg):
                _c = msg.clause
                self.v_g = _c
                return True

            def resume(self, agent, result=None):
                agent.post(rt.Retract(rt.Belief(self.v_g, t_status, t_Active)))
                return self.succeed(agent)

        class IncrementPropose(rt.Task):
            # counting.mia:37  def IncrementPropose(/countTo $v1 -> $g)
            trigger = rt.Trigger(rt.Attempt, rt.Perform, t_countTo)

            def bind(self, msg):
                _c = msg.clause
                self.v_v1 = _c.obj
                self.v_g = _c
                return True

            def resume(self, agent, result=None):
                ctx = agent.context
                _m0 = []
                for _c0 in ctx.find(rt.Belief, self.v_g, t_value, self.v_v1):
                    _m0.append(())
                for _ in _m0:
                    return self.succeed(agent)
                if not _m0:
                    agent.propose(rt.Attempt(rt.Perform(rt.SELF, t_increment, self.v_g)))
                    return self.return_(agent)
                return self.succeed(agent)

        class IncrementApply(rt.Task):
            # counting.mia:46  def IncrementApply(/increment $g)
            trigger = rt.Trigger(rt.Attempt, rt.Perform, t_increment)

            def bind(self, msg):
                _c = msg.clause
                self.v_g = _c.obj
                return True

            def resume(self, agent, result=None):
                ctx = agent.context
                _m0 = []
                for _c0 in ctx.find(rt.Belief, self.v_g, t_value, rt.ANY):
                    v_v1 = _c0.obj
                    _m0.append((v_v1,))
                for (v_v1,) in _m0:
                    agent.post(rt.Modify(rt.Belief(self.v_g, t_value, (v_v1 + 1))))
                    print(v_v1 + 1, "...")
                return self.succeed(agent)

        boot = Counting
        rules = (Impasse, GoalElab, NotGoalElab, IncrementPropose, IncrementApply)
        experts = ()

    boot = CountingAgent
    rules = ()
    experts = (Counting,)
