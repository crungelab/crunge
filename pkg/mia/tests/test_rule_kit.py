import unittest

from crunge.core import BaseNode
from crunge.mia.run import Clause, __

from crunge.mia.run.message import Message, Trigger
from crunge.mia.run.rule_kit import Match, Rule, RuleKit, rule

ALWAYS = Trigger(Message, Clause, __, __, __)
NEVER = Trigger(Message, Clause, object(), __, __)

def a_message() -> Message:
    return Message(Clause("kurt", "likes", "turtles"))

async def noop(self, msg):
    pass


#
# The kit on its own. No host, no node, no lifecycle.
#
class TestRuleKit(unittest.TestCase):
    def test_match_yields_in_declaration_order(self):
        first = Rule(ALWAYS, noop, prodname="first")
        second = Rule(ALWAYS, noop, prodname="second")
        kit = RuleKit([first, second])

        matches = list(kit.match(a_message()))

        self.assertEqual([m.rule for m in matches], [first, second])
        self.assertIsInstance(matches[0], Match)

    def test_non_matching_rules_are_skipped(self):
        kit = RuleKit([Rule(NEVER, noop), Rule(ALWAYS, noop)])
        self.assertEqual(len(list(kit.match(a_message()))), 1)

    def test_no_rules_matches_nothing(self):
        self.assertEqual(list(RuleKit().match(a_message())), [])

    def test_fork_copies_the_list(self):
        original = RuleKit([Rule(ALWAYS, noop)], owner="a")
        forked = original.fork("b")
        forked.add_rule(Rule(ALWAYS, noop))

        self.assertEqual(len(original), 1)
        self.assertEqual(len(forked), 2)
        self.assertEqual(forked.owner, "b")

    def test_constructor_does_not_alias(self):
        rules = [Rule(ALWAYS, noop)]
        RuleKit(rules).add_rule(Rule(ALWAYS, noop))
        self.assertEqual(len(rules), 1)

    def test_trigger_must_be_a_trigger(self):
        with self.assertRaises(TypeError):
            Rule("+ $x likes Turtles", noop)


#
# The decorator, which needs a host class for __init_subclass__ to scan.
#
class Host(BaseNode):
    @rule(ALWAYS)
    async def turtles(self, msg):
        pass

    @rule(ALWAYS)
    async def turtle_soup(self, msg):
        pass


class Sub(Host):
    @rule(ALWAYS)
    async def snapping_turtles(self, msg):
        pass


class Bare(BaseNode):
    pass


class TestRuleDecorator(unittest.TestCase):
    def test_declared_rules_land_on_the_class(self):
        kit = Host.get_cls_chip(RuleKit)
        self.assertEqual(len(kit), 2)
        self.assertIs(kit.owner, Host)
        self.assertEqual(
            sorted(r.prodname for r in kit.rules), ["turtle_soup", "turtles"]
        )

    def test_provenance_is_recorded(self):
        rule_ = Host.get_cls_chip(RuleKit).rules[0]
        self.assertTrue(rule_.filename.endswith(".py"))
        self.assertIsInstance(rule_.lineno, int)

    def test_subclass_inherits_and_extends(self):
        self.assertEqual(len(Sub.get_cls_chip(RuleKit)), 3)

    def test_subclass_does_not_pool_into_its_parent(self):
        # The original bug: every class appended to one shared kit, so
        # declaring a rule anywhere gave it to everything.
        self.assertEqual(len(Host.get_cls_chip(RuleKit)), 2)
        self.assertIs(Sub.get_cls_chip(RuleKit).owner, Sub)

    def test_unrelated_class_gets_nothing(self):
        self.assertIsNone(Bare.get_cls_chip(RuleKit))

    def test_instances_share_the_class_kit(self):
        self.assertIs(Host().get(RuleKit), Host().get(RuleKit))

    def test_multiple_triggers_make_multiple_rules(self):
        class Multi(BaseNode):
            @rule(ALWAYS, ALWAYS, ALWAYS)
            async def three_ways(self, msg):
                pass

        self.assertEqual(len(Multi.get_cls_chip(RuleKit)), 3)


if __name__ == "__main__":
    unittest.main()