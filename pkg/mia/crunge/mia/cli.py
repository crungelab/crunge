"""python -m crunge.mia run program.mia [--expert NAME] [--priority NAME] [--trace PATH]"""

from __future__ import annotations

import argparse
import sys

import crunge.mia.runtime as rt
from crunge.mia.load import expert_classes, load_file

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
    run.add_argument("--expert", help="expert to run (default: the first one in the file)")
    run.add_argument("--priority", choices=PRIORITIES, help="search priority for every problem space")
    run.add_argument("--trace", metavar="PATH", help="record a trace for miascope")
    run.add_argument("--act", action="store_true", help="replay the plan's effects after solving")
    args = parser.parse_args(argv)

    module = load_file(args.file)
    experts = {cls.__name__: cls for cls in expert_classes(module)}
    if not experts:
        parser.error(f"{args.file} defines no experts")
    name = args.expert or next(iter(experts))
    if name not in experts:
        parser.error(f"no expert {name}; choose from {', '.join(experts)}")
    if args.priority:
        rt.Expert.priority = PRIORITIES[args.priority]

    tracer = rt.Tracer(rt.JsonlSink(args.trace)) if args.trace else None
    try:
        solver = rt.ProblemSolver(experts[name], tracer=tracer)
        status = solver.run()
    finally:
        if tracer is not None:
            tracer.close()

    if solver.solution is not None:
        print(f"{name}: {status.name} (cost {solver.solution.cost:g})")
    else:
        print(f"{name}: {status.name}")
    if solver.solution is not None:
        print_plan(solver.solution, depth=1)
        plan = solver.plan
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


def print_plan(solution: rt.Expert, depth: int):
    """Print the commits leading to `solution`, and the plans of experts spawned along the way."""
    path = [solution]
    while path[-1].solution is None and path[-1].parent is not None:
        path.append(path[-1].parent)
    pad = "  " * depth
    for message, plan in zip(solution.history, solution.chosen):
        print(f"{pad}{rt.to_mia(message)}" + (f"  [{plan}]" if plan else ""))
    for state in reversed(path):
        for child in state.states:
            if child.spawned and child.solution is not None:
                print(f"{pad}{type(child).__name__} (cost {child.solution.cost:g}):")
                print_plan(child.solution, depth + 1)


if __name__ == "__main__":
    sys.exit(main())
