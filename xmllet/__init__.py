from xml.dom.minidom import parseString

import logging
import pathlib

from .builtin import parse_stream, FILTERS, MAGICS, TYPES, OPS


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def parse_file(fpath: str, filter: str):
    """Parses the root element present in file <fpath> through <filter>."""
    fpath = pathlib.Path(fpath)
    if not fpath.exists():
        logging.error('File not found! Exiting...')
        exit(-1)

    with open(fpath, 'r', encoding='utf8') as fh:
        xml = fh.read()

    try:
        dom = parseString(xml)
        pipe = iter([dom])  # Create the initial pipe containing only the root element.
        logger.info(f"Parsing {fpath} with filter {filter} started.")
        parsed = parse_stream(pipe, filter)
        logger.info(f"Parsing {fpath} with filter {filter} finished.")
        return parsed

    except Exception as e:
        logger.exception(e)
        exit(-1)

def register_types(types: dict):
    for type_id, type_ in types.items():
        if type_ in TYPES:
            logger.warning("Type already registered (skipping).")
        else:
            TYPES[type_id] = type_

def register_filters(filters: dict):
    for filter_id, filter_ in filters.items():
        if filter_id in FILTERS:
            logger.warning("Filter already registered (skipping).")
        else:
            FILTERS[filter_id] = filter_

def register_magics(magics: dict):
    for magic_id, magic in magics.items():
        if magic_id in MAGICS:
            logger.warning("Filter already registered (skipping).")
        else:
            MAGICS[magic_id] = magic
