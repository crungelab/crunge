# atlas_format.py — parser for Spine's .atlas text format
# Ref: http://en.esotericsoftware.com/spine-atlas-format

from __future__ import annotations
from dataclasses import dataclass, field


@dataclass
class AtlasRegion:
    name: str
    index: int = -1
    x: int = 0
    y: int = 0
    width: int = 0
    height: int = 0
    # rotate: False, True (90° CCW), or a degree value 0-360 per spec.
    # Only False/no-rotation is handled downstream right now — see TODO
    # in atlas_loader.py. Stored as-is here so nothing is silently lost.
    #rotate: bool | float = False
    rotate: int = 0  # degrees, multiple of 90
    offset_x: int = 0        # whitespace stripped from left edge
    offset_y: int = 0        # whitespace stripped from bottom edge
    original_width: int = 0  # pre-strip size; equals width/height if no stripping
    original_height: int = 0
    extra: dict[str, str] = field(default_factory=dict)  # name/value pairs Spine doesn't define


@dataclass
class AtlasPage:
    image_path: str
    width: int = 0
    height: int = 0
    format: str = "RGBA8888"
    min_filter: str = "Nearest"
    mag_filter: str = "Nearest"
    repeat: str = "none"
    pma: bool = False
    regions: list[AtlasRegion] = field(default_factory=list)


@dataclass
class AtlasFile:
    pages: list[AtlasPage] = field(default_factory=list)

    def find_region(self, name: str, index: int = -1) -> AtlasRegion | None:
        for page in self.pages:
            for region in page.regions:
                if region.name == name and region.index == index:
                    return region
        return None


_PAGE_KEYS = {"size", "format", "filter", "repeat", "pma"}
_REGION_KEYS = {"index", "bounds", "offsets", "rotate", "split", "pad"}


def _parse_csv_ints(value: str) -> list[int]:
    return [int(v.strip()) for v in value.split(",")]


def parse_atlas(path: str) -> AtlasFile:
    with open(path) as f:
        lines = [line.rstrip("\n") for line in f]

    atlas = AtlasFile()
    i = 0
    n = len(lines)

    while i < n:
        # skip blank lines between pages
        while i < n and lines[i].strip() == "":
            i += 1
        if i >= n:
            break

        # page header: first non-blank line is the image filename
        page = AtlasPage(image_path=lines[i].strip())
        i += 1

        while i < n and ":" in lines[i] and lines[i].split(":", 1)[0].strip() in _PAGE_KEYS:
            key, value = (part.strip() for part in lines[i].split(":", 1))
            if key == "size":
                page.width, page.height = _parse_csv_ints(value)
            elif key == "format":
                page.format = value
            elif key == "filter":
                page.min_filter, page.mag_filter = (v.strip() for v in value.split(","))
            elif key == "repeat":
                page.repeat = value
            elif key == "pma":
                page.pma = value.lower() == "true"
            i += 1

        # region sections, until blank line or EOF
        while i < n and lines[i].strip() != "":
            region = AtlasRegion(name=lines[i].strip())
            i += 1

            while i < n and ":" in lines[i]:
                key, value = (part.strip() for part in lines[i].split(":", 1))
                if key == "index":
                    region.index = int(value)
                elif key == "bounds":
                    region.x, region.y, region.width, region.height = _parse_csv_ints(value)
                elif key == "offsets":
                    ox, oy, ow, oh = _parse_csv_ints(value)
                    region.offset_x, region.offset_y = ox, oy
                    region.original_width, region.original_height = ow, oh
                elif key == "rotate":
                    region.rotate = value.lower() == "true" if value.lower() in ("true", "false") else float(value)
                elif key in ("split", "pad"):
                    pass  # ninepatch data — unused, not needed for skeletal attachments
                else:
                    region.extra[key] = value  # e.g. Spine's frame-animation "origin" data
                i += 1

            if region.original_width == 0:
                region.original_width = region.width
                region.original_height = region.height

            page.regions.append(region)

        atlas.pages.append(page)

    return atlas