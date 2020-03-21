from turf.helpers._units import geometry_types
from abc import ABC, abstractmethod


class Feature:
    """
    Class that encapsulates a certain geometry, along with its properties.
    Equivalent to a GeoJSON feature
    """

    def __init__(self, geom=None, properties=None):
        self.type = "Feature"
        self.geometry = geom or []
        self.properties = properties or {}

    def __repr__(self):
        return f"Feature({self.geometry})"


class FeatureCollection:
    """
    Class that encapsulates a group of features in a FeatureCollection.
    Equivalent to a GeoJSON FeatureCollection
    """

    def __init__(self, features=None):
        self.type = "FeatureCollection"
        self.features = features or []

    def __repr__(self):
        return f"FeatureCollection({self.features})"


class _FeatureBaseClass(ABC):
    """
    Base class for Point, LineString and Polygon sub-classes.
    """

    def __init__(self, coordinates: list):

        self._check_input(coordinates)

        self.type = "Point"
        self.coordinates = coordinates

    def __repr__(self):
        return f"{self.__class__.__name__}({self.coordinates})"

    @staticmethod
    @abstractmethod
    def _check_input(coordinates):
        pass


class Point(_FeatureBaseClass):
    """
    Class for creating Point objects with certain coordinates.
    Equivalent to a GeoJSON Point.
    """

    def __init__(self, coordinates: list):
        _FeatureBaseClass.__init__(self, coordinates)
        self.type = "Point"

    @staticmethod
    def _check_input(coordinates):
        if not isinstance(coordinates, list) or len(coordinates) != 2:
            raise Exception("Coordinates must be an array of [lng, lat]")

        if any(not isinstance(x, (int, float)) for x in coordinates):
            raise Exception("Coordinates contains invalid numbers")


class MultiPoint(Point):
    def __init__(self, coordinates: list):
        Point.__init__(self, coordinates)
        self.type = "MultiPoint"

    def _check_input(self, coordinates):
        if not isinstance(coordinates, list):
            raise Exception("Coordinates must be an array of Positions")

        for coord in coordinates:
            super(MultiPoint, self)._check_input(coord)


class LineString(_FeatureBaseClass):
    """
    Class for creating LineString objects with certain coordinates.
    Equivalent to a GeoJSON LineString.
    """

    def __init__(self, coordinates: list):
        _FeatureBaseClass.__init__(self, coordinates)
        self.type = "LineString"

    @staticmethod
    def _check_input(coordinates):
        if not isinstance(coordinates, list) or len(coordinates) < 2:
            raise Exception("Coordinates must be an array of two or more positions")

        if any(any(not isinstance(x, (int, float)) for x in y) for y in coordinates):
            raise Exception("Coordinates contains invalid numbers")


class MultiLineString(LineString):
    def __init__(self, coordinates: list):
        LineString.__init__(self, coordinates)
        self.type = "MultiLineString"

    def _check_input(self, coordinates):
        if not isinstance(coordinates, list):
            raise Exception("Coordinates must be an array of Position arrays")

        for coord in coordinates:
            super(MultiLineString, self)._check_input(coord)


class Polygon(_FeatureBaseClass):
    """
    Class for creating Polygon objects with certain coordinates.
    Equivalent to a GeoJSON Polygon.
    """

    def __init__(self, coordinates: list):
        _FeatureBaseClass.__init__(self, coordinates)
        self.type = "Polygon"

    @staticmethod
    def _check_input(coordinates):
        if not isinstance(coordinates, list):
            raise Exception("Coordinates must be a list of LinearRings")

        for ring in coordinates:
            if not isinstance(ring, list):
                raise Exception("LinearRing coordinates must be a list of Positions")

            if len(ring) < 4:
                raise Exception(
                    "Each LinearRing of a Polygon must have 4 or more Positions."
                )

            if ring[-1] != ring[0]:
                raise Exception("First and last Position are not equivalent.")


class MultiPolygon(Polygon):
    def __init__(self, coordinates: list):
        Polygon.__init__(self, coordinates)
        self.type = "MultiPolygon"

    def _check_input(self, coordinates):
        if not isinstance(coordinates, list):
            raise Exception("Coordinates must be an array of Polygons")

        for coord in coordinates:
            super(MultiPolygon, self)._check_input(coord)


def feature(geom, properties=None, options=None):
    """
    Wraps a GeoJSON Geometry in a GeoJSON Feature.

    :param geom: input geometry
    :param properties: a dictionary of key-value pairs to add as properties
    :param options: an options dictionary:
        [options["bbox"] Bounding Box Array [west, south, east, north] associated with the Feature
        [options["id"] Identifier associated with the Feature
    :return: a GeoJSON feature
    """

    if not options:
        options = {}

    if not properties:
        properties = {}

    feat = Feature(geom, properties)

    if "id" in options:
        feat.id = options["id"]

    if "bbox" in options:
        feat.bbox = options["bbox"]

    return feat


def feature_collection(features, options):
    """
    Takes one or more Feature and creates a FeatureCollection.

    :param features: input features
    :param options: an options dictionary:
        [options["bbox"] Bounding Box Array [west, south, east, north] associated with the Feature
        [options["id"] Identifier associated with the Feature
    :return: a FeatureCollection of Features
    """

    if not options:
        options = {}

    feat_collection = FeatureCollection(features)

    if "id" in options:
        feat_collection.id = options["id"]

    if "bbox" in options:
        feat_collection.bbox = options["bbox"]

    return feat_collection


def geometry(geom_type, coordinates, options=None):
    """
    Creates a GeoJSON {@link Geometry} from a Geometry string type & coordinates.
    For GeometryCollection type use `helpers.geometryCollection`

    :param geom_type: one of "Point" | "LineString" | "Polygon" | "MultiPoint" | "MultiLineString" | "MultiPolygon"
    :param coordinates: array of coordinates [lng, lat]
    :param options: an options dictionary:
        [options["bbox"] Bounding Box Array [west, south, east, north] associated with the Feature
        [options["id"] Identifier associated with the Feature
    :return: a GeoJSON geometry
    """

    if not options:
        options = {}

    try:
        geom_type = geometry_types[geom_type]
    except KeyError:
        raise Exception(f"{geom_type} is invalid")

    if geom_type == "Point":
        return point(coordinates).geometry
    elif geom_type == "LineString":
        return line_string(coordinates).geometry
    elif geom_type == "Polygon":
        return polygon(coordinates).geometry
    elif geom_type == "MultiPoint":
        return multi_point(coordinates).geometry
    elif geom_type == "MultiLineString":
        return multi_line_string(coordinates).geometry
    elif geom_type == "MultiPolygon":
        return multi_polygon(coordinates).geometry


def point(coordinates, properties=None, options=None):
    """
    Creates a Point Feature from a Position.

    :param coordinates: coordinates longitude, latitude position in degrees - Position
    :param properties: a dictionary of key-value pairs to add as properties
    :param options: an options dictionary:
        [options["bbox"] Bounding Box Array [west, south, east, north] associated with the Feature
        [options["id"] Identifier associated with the Feature
    :return: a Point Feature
    """

    geom = Point(coordinates)

    return feature(geom, properties, options)


def points(coordinates, properties=None, options=None):
    """
    Creates a Point FeatureCollection from an Array of Point coordinates.

    :param coordinates: a list of Points - Position[]
    :param properties: a dictionary of key-value pairs to add as properties
    :param options: an options dictionary:
        [options["bbox"] Bounding Box Array [west, south, east, north] associated with the Feature
        [options["id"] Identifier associated with the Feature
    :return: Point FeatureCollection
    """

    if not isinstance(coordinates, list):
        raise Exception("Coordinates must be a list")

    return feature_collection(
        list(map(lambda coord: point(coord, properties), coordinates)), options
    )


def multi_point(coordinates, properties=None, options=None):
    """
    Creates a MultiPoint Feature based on a coordinate array.
    Properties can be added optionally.

    :param coordinates: a list of Points - Position[]
    :param properties: a dictionary of key-value pairs to add as properties
    :param options: an options dictionary:
        [options["bbox"] Bounding Box Array [west, south, east, north] associated with the Feature
        [options["id"] Identifier associated with the Feature
    :return: a MultiPoint feature
    """

    geom = MultiPoint(coordinates)

    return feature(geom, properties, options)


def line_string(coordinates, properties=None, options=None):
    """
    Creates a LineString Feature from an Array of Positions.

    :param coordinates: a list of Positions - Position[]
    :param properties: a dictionary of key-value pairs to add as properties
    :param options: an options dictionary:
        [options["bbox"] Bounding Box Array [west, south, east, north] associated with the Feature
        [options["id"] Identifier associated with the Feature
    :return: a LineString feature
    """

    if not options:
        options = {}

    if not properties:
        properties = {}

    geom = LineString(coordinates)

    return feature(geom, properties, options)


def line_strings(coordinates_list, properties=None, options=None):
    """
    Creates a LineString FeatureCollection from an Array of LineString coordinates.

    :param coordinates_list: a list of a list of Positions - Position[][]
    :param properties: a dictionary of key-value pairs to add as properties
    :param options: an options dictionary:
        [options["bbox"] Bounding Box Array [west, south, east, north] associated with the Feature
        [options["id"] Identifier associated with the Feature
    :return: LineString FeatureCollection
    """

    if not isinstance(coordinates_list, list):
        raise Exception("Coordinates_list must be a list")

    return feature_collection(
        list(map(lambda coord: line_string(coord, properties), coordinates_list)),
        options,
    )


def multi_line_string(coordinates, properties=None, options=None):
    """
    Creates a MultiLineString Feature based on a coordinate array.
    Properties can be added optionally.

    :param coordinates: a list of a list of Positions - Position[][]
    :param properties: a dictionary of key-value pairs to add as properties
    :param options: an options dictionary:
        [options["bbox"] Bounding Box Array [west, south, east, north] associated with the Feature
        [options["id"] Identifier associated with the Feature
    :return: a MultiLineString feature
    """

    geom = MultiLineString(coordinates)

    return feature(geom, properties, options)


def polygon(coordinates, properties=None, options=None):
    """
    Creates a Polygon Feature from an Array of LinearRings.

    :param coordinates: a list of a list of Positions - Position[][]
    :param properties: a dictionary of key-value pairs to add as properties
    :param options: an options dictionary:
        [options["bbox"] Bounding Box Array [west, south, east, north] associated with the Feature
        [options["id"] Identifier associated with the Feature
    :return: a Polygon Feature
    """

    if not options:
        options = {}

    if not properties:
        properties = {}

    geom = Polygon(coordinates)

    return feature(geom, properties, options)


def polygons(coordinates_list, properties=None, options=None):
    """
    Creates a Polygon FeatureCollection from an Array of Polygon coordinates.

    :param coordinates_list: an array of polygons - Position[][][]
    :param properties: a dictionary of key-value pairs to add as properties
    :param options: an options dictionary:
        [options["bbox"] Bounding Box Array [west, south, east, north] associated with the Feature
        [options["id"] Identifier associated with the Feature
    :return: Polygon FeatureCollection
    """

    if not isinstance(coordinates_list, list):
        raise Exception("Coordinates_list must be a list")

    return feature_collection(
        list(map(lambda coords: polygon(coords, properties), coordinates_list)), options
    )


def multi_polygon(coordinates, properties=None, options=None):
    """
    Creates a MultiPolygon Feature based on a coordinate array.
    Properties can be added optionally.

    :param coordinates: an array of polygons - Position[][][]
    :param properties: a dictionary of key-value pairs to add as properties
    :param options: an options dictionary:
        [options["bbox"] Bounding Box Array [west, south, east, north] associated with the Feature
        [options["id"] Identifier associated with the Feature
    :return: a MultiPolygon feature
    """

    geom = MultiPolygon(coordinates)

    return feature(geom, properties, options)