error_codes = {
    "InvalidPoint": "InvalidInput",
    "InvalidLinePolygon": "InvalidInput",
    "InvalidPointInput": "InvalidInput",
}

error_code_corpus = {
    "InvalidUnits": lambda units: f"'{units}' is not a valid unit.",
    "InvalidLength": "<length> must be a positive number",
    "InvalidArea": "<area> must be a positive number",
    "InvalidDistance": "<distance> must be a positive number",
    "InvalidDegrees": "<degrees> must be a number",
    "InvalidRadians": "<radians> must be a number",
    "InvalidGeometry": lambda geometries: f"Input must be of type {', '.join(geometries)}",
    "InvalidFeature": "Input must be a FeatureCollection or Feature",
    "InvalidPoint": "Input must be a Point geoJSON feature or an array of numbers.",
    "InvalidMultiInput": "Input coordinates must be an array ",
    "InvalidPointInput": "Input coordinates must be an array of 2 valid numbers.",
    "InvalidLineStringInput": "Input coordinates must be an array of valid Points.",
    "InvalidLinePoints": "Input coordinates must be an array of 2 or more valid Points.",
    "InvalidPolygonInput": "Input coordinates must be an array of valid rings.",
    "InvalidLinearRing": "Each Polygon ring coordinates must be a list of 4 or more Points.",
    "InvalidFirstLastPoints": "First and last Points of Polygon ring are not equivalent.",
}

error_code_messages = {
    "InvalidUnits": error_code_corpus["InvalidUnits"],
    "InvalidLength": error_code_corpus["InvalidLength"],
    "InvalidArea": error_code_corpus["InvalidArea"],
    "InvalidDistance": error_code_corpus["InvalidDistance"],
    "InvalidDegrees": error_code_corpus["InvalidDegrees"],
    "InvalidRadians": error_code_corpus["InvalidRadians"],
    "InvalidGeometry": error_code_corpus["InvalidGeometry"],
    "InvalidFeature": error_code_corpus["InvalidFeature"],
    "InvalidPoint": error_code_corpus["InvalidPoint"],
    "InvalidPointInput": error_code_corpus["InvalidPointInput"],
    "InvalidMultiInput": error_code_corpus["InvalidMultiInput"],
    "InvalidLineStringInput": error_code_corpus["InvalidLineStringInput"],
    "InvalidLinePoints": error_code_corpus["InvalidLinePoints"],
    "InvalidPolygonInput": error_code_corpus["InvalidPolygonInput"],
    "InvalidLinearRing": error_code_corpus["InvalidLinearRing"],
    "InvalidFirstLastPoints": error_code_corpus["InvalidFirstLastPoints"],
}