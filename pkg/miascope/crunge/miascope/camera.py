"""Pan and zoom between screen and world coordinates."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Camera:
    x: float = 0.0     # world point at the screen's top-left corner
    y: float = 0.0
    zoom: float = 1.0  # screen pixels per world unit
    min_zoom: float = 0.05
    max_zoom: float = 8.0

    def to_screen(self, wx: float, wy: float) -> tuple[float, float]:
        return (wx - self.x) * self.zoom, (wy - self.y) * self.zoom

    def to_world(self, sx: float, sy: float) -> tuple[float, float]:
        return sx / self.zoom + self.x, sy / self.zoom + self.y

    def pan(self, dx: float, dy: float) -> None:
        """Move the view by a screen-space drag."""
        self.x -= dx / self.zoom
        self.y -= dy / self.zoom

    def zoom_at(self, sx: float, sy: float, factor: float) -> None:
        """Zoom by `factor`, keeping the world point under the screen point fixed."""
        wx, wy = self.to_world(sx, sy)
        self.zoom = min(max(self.zoom * factor, self.min_zoom), self.max_zoom)
        self.x = wx - sx / self.zoom
        self.y = wy - sy / self.zoom

    def fit(self, left: float, top: float, right: float, bottom: float,
            width: float, height: float, margin: float = 40.0) -> None:
        """Show the world rectangle centered horizontally, top-aligned, never magnified past 1."""
        if width <= 2 * margin or height <= 2 * margin:
            return
        w, h = max(right - left, 1.0), max(bottom - top, 1.0)
        zoom = min((width - 2 * margin) / w, (height - 2 * margin) / h, 1.0)
        self.zoom = min(max(zoom, self.min_zoom), self.max_zoom)
        self.x = left - (width / self.zoom - w) / 2
        self.y = top - margin / self.zoom

    def visible(self, width: float, height: float) -> tuple[float, float, float, float]:
        """The world rectangle currently on screen: left, top, right, bottom."""
        left, top = self.to_world(0, 0)
        right, bottom = self.to_world(width, height)
        return left, top, right, bottom
