from typing import List, Optional, Dict, Union, Literal, Annotated, Any
from pydantic import BaseModel, Field, ValidationError, RootModel, ConfigDict

from .name import Name


class Node(BaseModel):
    tags: Optional[List[str]] = None
    _comment: Optional[str] = None

    #model_config = ConfigDict(arbitrary_types_allowed = True, strict=True, populate_by_name=True)
    #model_config = ConfigDict(arbitrary_types_allowed = True, populate_by_name=True)
    model_config = ConfigDict(arbitrary_types_allowed = True)


class RecordMember(Node):
    name: Name
    type: str
    annotation: Optional[str] = None
    optional: Optional[bool] = False
    no_default: Optional[bool] = False
    #default_value: Optional[str] = Field(alias="default", default=None)
    default_value: Union[str, int] = Field(alias="default", default=None)
    #default_val: Optional[str] = Field(default=None, alias="default")
    length: Optional[Union[str, int]] = None


class Method(Node):
    name: Name
    returns: Optional[str] = None
    args: Optional[List[RecordMember]] = None
    no_autolock: Optional[bool] = Field(alias="no autolock", default=None)


class Entry(Node):
    category: str
    name: Optional[Name] = None
    
    def __hash__(self):
        return hash(self.name)


class EnumValue(Node):
    name: Name
    value: int


class EnumType(Entry):
    category: Literal["enum"]
    values: List[EnumValue]


class BitmaskValue(Node):
    name: Name
    value: int


class BitmaskType(Entry):
    category: Literal["bitmask"]
    values: List[BitmaskValue]


class ObjectType(Entry):
    category: Literal["object"] = "object"
    methods: Optional[List[Method]] = []
    no_autolock: Optional[bool] = Field(alias="no autolock", default=None)


class StructureType(Entry):
    category: Literal["structure"]
    members: List[RecordMember]
    extensible: Optional[Union[str, bool]] = None
    chained: Optional[str] = None
    chain_roots: Optional[List[str]] = Field(alias="chain roots", default=None)
    extensions: Optional[List[Any]] = Field(None, exclude=True, repr=False)

    def model_post_init(self, __context: Any) -> None:
        super().model_post_init(__context)
        # Chained structs inherit from wgpu::ChainedStruct, which has
        # nextInChain, so setting both extensible and chained would result in
        # two nextInChain members.
        assert not (self.extensible and self.chained)

        if self.chained:
            assert self.chained == "in" or self.chained == "out"
            assert self.chain_roots
            self.add_next_in_chain()

        if self.extensible:
            assert self.extensible == "in" or self.extensible == "out"
            self.add_next_in_chain()
        # self.extensions = []

    def add_next_in_chain(self):
        self.members.insert(
            0,
            RecordMember(
                name=Name("next in chain"),
                #type="const void*",
                #type="chained struct",
                type="chained struct" if not self.output else "chained struct out",
                #annotation="value",
                #annotation="const*",
                annotation="const*" if not self.output else "*",
                optional=True,
            ),
        )

    @property
    def output(self):
        return self.chained == "out" or self.extensible == "out"

    @property
    def has_free_members_function(self):
        if not self.output:
            return False
        for m in self.members:
            #if m.annotation != "value":
            if m.annotation is not None:
                return True
        return False


class CallbackInfoType(StructureType):
    category: Literal["callback info"] = Field(
        default="callback info", alias="callback info"
    )


class NativeType(Entry):
    category: Literal["native"]
    wasm_type: Optional[str] = Field(alias="wasm type", default=None)


class FunctionPointerType(Entry):
    category: Literal["function pointer"] = Field(
        default="function pointer", alias="function pointer"
    )
    returns: Optional[str] = None
    args: Optional[List[RecordMember]] = None


class CallbackFunctionType(Entry):
    category: Literal["callback function"] = Field(
        default="callback function", alias="callback function"
    )
    args: Optional[List[RecordMember]] = None


class ConstantDefinition(Entry):
    category: Literal["constant"]
    type: str
    value: str


class FunctionDeclaration(Entry):
    category: Literal["function"]
    returns: Optional[str] = None
    args: Optional[List[RecordMember]] = None


TypeUnion = Union[
    ObjectType,
    EnumType,
    BitmaskType,
    StructureType,
    NativeType,
    FunctionPointerType,
    ConstantDefinition,
    FunctionDeclaration,
    CallbackInfoType,
    CallbackFunctionType,
]


class Root(RootModel):
    #root: Dict[str, TypeUnion]
    root: Dict[str, TypeUnion] = Field(default_factory=dict)

    model_config = ConfigDict(populate_by_name=True)

    def __init__(self, **data):
        super().__init__(**data)
        for key, value in self.root.items():
            native = isinstance(value, NativeType)
            value.name = Name(key, native=native)

        self.root["chained struct"] = StructureType(
            name=Name("chained struct"),
            category="structure",
            members=[
                RecordMember(
                    name=Name("next_in_chain"),
                    #type="const void*",
                    type="chained struct",
                    #annotation="value",
                    annotation="const*",
                    #optional=True,
                )
            ],
        )

        self.root["chained struct out"] = StructureType(
            name=Name("chained struct out"),
            category="structure",
            members=[
                RecordMember(
                    name=Name("next_in_chain"),
                    #type="const void*",
                    type="chained struct out",
                    #annotation="value",
                    annotation="const*",
                    #optional=True,
                )
            ],
        )

    def __iter__(self):
        return iter(self.root.items())

    def __getitem__(self, key):
        return self.root[key]

    def __setitem__(self, key, value):
        self.root[key] = value

    def __delitem__(self, key):
        del self.root[key]

    """
    def __iter__(self):
        return iter(self.root)
    """

    def __len__(self):
        return len(self.root)

    def keys(self):
        return self.root.keys()

    def values(self):
        return self.root.values()

    def items(self):
        return self.root.items()
