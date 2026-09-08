"""The map displayed in the map application."""

import ipyvuetify as v
from ipyleaflet import FullScreenControl, TileLayer
from leafmap.leafmap import Map
from sepal_ui import mapping as sm
from sepal_ui import sepalwidgets as sw

# CARTO answers keyless requests with HTTP 200 and an "API KEY REQUIRED" watermark,
# which is why the Positron/DarkMatter pair this app used to rely on is unusable.
# Esri's canvas basemaps are the closest keyless equivalent, but they only carry
# global data to zoom 16 and serve a placeholder past it, hence max_native_zoom.
ESRI_CANVAS_URL = (
    "https://server.arcgisonline.com/ArcGIS/rest/services/Canvas/"
    "World_{}_Gray_Base/MapServer/tile/{{z}}/{{y}}/{{x}}"
)


class MapTile(sw.Tile):
    def __init__(self):
        """Specific Map integrating all the widget components.

        Use this map to gather all your widget and place them on it. It will reduce the amount of work to perform in the notebook
        """
        basemap = TileLayer(
            url=ESRI_CANVAS_URL.format("Dark" if v.theme.dark else "Light"),
            name="Esri Gray Canvas",
            attribution="Tiles &copy; Esri",
            max_native_zoom=16,
            max_zoom=24,
        )
        self.m = Map(basemap=basemap, zoom=3)
        self.m._id = "leafmap"
        self.m.add_class(self.m._id)

        # don't add the control to the map simply set it to fullscreen
        sm.FullScreenControl(self.m, fullscreen=True, fullapp=True)
        self.m.remove_control(
            next(c for c in self.m.controls if isinstance(c, FullScreenControl))
        )

        # create the tile
        super().__init__("map_tile", "", [self.m])
