from xml.dom.minidom import Element

from xmllet.builtin import parse_stream, get_node_value, select


def pointCoordinates_parser(element: Element):
    """Parses datex2:pointCoordinates XML elements."""

    assert element.tagName == 'pointCoordinates', "Wrong element type: expected pointCoordinates."

    parsed = {'longitude': float(get_node_value(element, 'longitude')),
              'latitude': float(get_node_value(element, 'latitude'))}
    return parsed

def ItineraryByIndexedLocations_parser(element: Element):
    """Parses datex2:ItineraryByIndexedLocations XML elements."""

    assert element.tagName == 'groupOfLocations', "Wrong element type: expected groupOfLocations."
    assert element.getAttribute('xsi:type') == 'ItineraryByIndexedLocations', 'Wrong element attribute: expected ItineraryByIndexedLocations'

    locations = select([element], 'locationContainedInItinerary')
    itinerary = {loc.getAttribute('index'):
                     list(parse_stream([loc], 'locationContainedInItinerary')) for loc in locations}

    return itinerary


NDW_TYPES = {'pointCoordinatesParser': pointCoordinates_parser,
             'ItineraryByIndexedLocationsParser': ItineraryByIndexedLocations_parser}
NDW_FILTERS = {
    'situationRecord': ['s|SOAP:Envelope.SOAP:Body.d2LogicalModel.payloadPublication.situation',
                        's|situationRecord',
                        'fa|xsi:type|MaintenanceWorks',
                        'fv|f|validity.validityTimeSpecification.overallStartTime|<%d',
                        'fv|f|validity.validityTimeSpecification.overallEndTime|>%d',
                        's|groupOfLocations',
                        'p|groupOfLocation-Point|groupOfLocations-ItineraryByIndexedLocations'],

    'groupOfLocation-Point': ['fa|xsi:type|Point',
                              'p|pointCoordinates'],

    'groupOfLocations-ItineraryByIndexedLocations': ['fa|xsi:type|ItineraryByIndexedLocations',
                                                     'a|ItineraryByIndexedLocationsParser'],

    'locationContainedInItinerary': ['s|location',
                                     'p|location-point|location-linear'],

    'location-point': ['fa|xsi:type|Point',
                       'p|pointCoordinates'],

    'location-linear': ['fa|xsi:type|Linear',
                        's|linearExtension.linearByCoordinatesExtension',
                        'p|linearByCoordinatesExtension-start|linearByCoordinatesExtension-end'],

    'linearByCoordinatesExtension-start': ['s|linearCoordinatesStartPoint',
                                           's|pointCoordinates',
                                           'a|pointCoordinatesParser'],

    'linearByCoordinatesExtension-end': ['s|linearCoordinatesEndPoint',
                                         's|pointCoordinates',
                                         'a|pointCoordinatesParser'],

    'pointCoordinates': ['s|pointByCoordinates',
                         's|pointCoordinates',
                         'a|pointCoordinatesParser']}
