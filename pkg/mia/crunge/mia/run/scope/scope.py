import contextvars


class Scope[T]:
    """Innermost enclosing scope of a given kind.

    Subclasses get their own stack automatically -- `class TaskScope(Scope[Task])`
    is the whole definition. Declaring `stack` by hand is what previously let a
    forgetful subclass share the base class's stack with every other one.
    """

    stack: contextvars.ContextVar[tuple[T, ...]]

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        cls.stack = contextvars.ContextVar(f"{cls.__name__}_stack", default=())

    @classmethod
    def push(cls, item: T) -> T:
        cls.stack.set(cls.stack.get() + (item,))
        return item

    @classmethod
    def pop(cls, expected: T | None = None) -> T:
        """Pop the innermost scope.

        `expected` is the node that believes it owns the scope. A mismatch means
        an unbalanced push somewhere else, which would otherwise shift the whole
        stack and silently mis-parent everything built afterwards.
        """
        stack = cls.stack.get()
        if not stack:
            raise RuntimeError(f"{cls.__name__}: pop from empty scope stack")
        top = stack[-1]
        if expected is not None and top is not expected:
            raise RuntimeError(
                f"{cls.__name__}: unbalanced pop; expected {expected!r}, found {top!r}"
            )
        cls.stack.set(stack[:-1])
        return top

    @classmethod
    def top(cls) -> T | None:
        """Innermost open scope, or None outside any."""
        stack = cls.stack.get()
        return stack[-1] if stack else None

    @classmethod
    def depth(cls) -> int:
        return len(cls.stack.get())

    @classmethod
    def clear(cls) -> None:
        """Drop everything. For test teardown after an unbalanced build."""
        cls.stack.set(())