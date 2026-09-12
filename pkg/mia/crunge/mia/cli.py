"""python -m crunge.mia run program.mia [--agent NAME] [--priority NAME] [--trace PATH]"""

from __future__ import annotations

import argparse
import sys

import crunge.mia.runtime as rt
from crunge.mia.load import agent_classes, load_file

PRIORITIES = {
    "a_star": rt.a_star(),
    "breadth_first": rt.breadth_first,
    "depth_first": rt.depth_first,
}


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("run", help="compile and run a Mia program")
    run.add_argument("file")
    run.add_argument("--agent", help="agent to run (default: the first one in the file)")
    run.add_argument("--priority", choices=PRIORITIES, help="search priority for every agency")
    run.add_argument("--trace", metavar="PATH", help="record a trace for miascope")
    run.add_argument("--act", action="store_true", help="replay the plan's effects after solving")
    args = parser.parse_args(argv)

    module = load_file(args.file)
    agents = {cls.__name__: cls for cls in agent_classes(module)}
    if not agents:
        parser.error(f"{args.file} defines no agents")
    name = args.agent or next(iter(agents))
    if name not in agents:
        parser.error(f"no agent {name}; choose from {', '.join(agents)}")
    if args.priority:
        rt.Agent.priority = PRIORITIES[args.priority]

    tracer = rt.Tracer(rt.JsonlSink(args.trace)) if args.trace else None
    try:
        host = rt.AgentHost(agents[name], tracer=tracer)
        status = host.run()
    finally:
        if tracer is not None:
            tracer.close()

    print(f"{name}: {status.name}")
    if host.solution is not None:
        print_plan(host.solution, depth=1)
        plan = host.plan
        if len(plan):
            print(f"\nPlan ({len(plan)} actions):")
            for action in plan:
                print(f"  {action.text}")
            if args.act:
                print("\nActing:")
                plan.run()
    if args.trace:
        print(f"trace written to {args.trace}")
    return 0 if status is rt.Status.SUCCEEDED else 1


def print_plan(solution: rt.Agent, depth: int):
    """Print the commits leading to `solution`, and the plans of experts spawned along the way."""
    path = [solution]
    while path[-1].solution is None and path[-1].parent is not None:
        path.append(path[-1].parent)
    pad = "  " * depth
    for message, plan in zip(solution.history, solution.chosen):
        print(f"{pad}{rt.to_mia(message)}" + (f"  [{plan}]" if plan else ""))
    for agent in reversed(path):
        for child in agent.agents:
            if child.spawned and child.solution is not None:
                print(f"{pad}{type(child).__name__} (cost {child.solution.cost:g}):")
                print_plan(child.solution, depth + 1)


if __name__ == "__main__":
    sys.exit(main())
