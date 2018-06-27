from typing import Iterable, Any
from xml.dom.minidom import Element
from datetime import datetime
from itertools import filterfalse, starmap, chain, tee
from logging import getLogger


logger = getLogger(__name__)
TIME_FORMAT = '%Y-%m-%dT%H:%M:%S'


def _get_descendant(element: Element, path: str):
    path = path.split('.')

    if len(path) > 1:
        childs = element.getElementsByTagName(path[0])
        if len(childs) != 1:
            msg = "Only the deepest descendant in selection query can be non-unique. Perhaps break the filter into multiple selections?"
            logger.error(msg)
            raise NotImplementedError(msg)
        child = childs[0]

        return _get_descendant(child, '.'.join(path[1:]))

    else:
        rel = element.getElementsByTagName(path[0])
        return rel


def _get_text(element: Element):
    rc = []
    for node in element.childNodes:
        if node.nodeType == node.TEXT_NODE:
            rc.append(node.data)
    return ''.join(rc)


def get_node_value(element: Element, path: str):
    value = _get_descendant(element, path)
    # logger.debug(f"get_node_value: {element},{path} -> {value}.")
    if len(value) > 0:
        return _get_text(value[0])
    else:
        return ""


def parse_stream(stream: Iterable[Element], filter: str):
    """Parses all elements in <pipe> through <filter>."""

    logger.debug(f'Parsing stream through filter {filter}...')
    for op, *args in [command.split('|') for command in FILTERS[filter]]:
        if op not in OPS:
            logger.error(f'Unrecognized operation: {op}.')
            raise TypeError

        logger.debug(f'Executing command: {op} on {args}.')
        stream = OPS[op](stream, *args)

    return stream


def select(stream: Iterable[Element], path: str):
    iter_ = [iter(_get_descendant(element, path)) for element in stream]
    return chain.from_iterable(iter_)


def filter_attribute(stream: Iterable[Element], attr: str, cond: str):
    if cond in MAGICS:
        f = lambda el: not MAGICS[cond](True, el.getAttribute(attr))
    else:
        f = lambda el: not (el.getAttribute(attr) == cond)

    return filterfalse(f, stream)


def filter_value(stream: Iterable[Element], strict: str, path: str, cond: str):
    _strict = {'t': True, 'f': False}
    strict = _strict[strict]

    if cond in MAGICS:
        f = lambda el: not MAGICS[cond](strict, get_node_value(el, path))

    else:
        def f(el):
            value = get_node_value(el, path)
            if cond == value:
                return False  # We filter out True values (see filterfalse)
            elif not strict and value == '':
                return False  # We filter out True values (see filterfalse)
            else:  # Strict is True and cond != value
                return True  # We filter out True values (see filterfalse)

    return filterfalse(f, stream)


def apply(stream: Iterable[Element], type_: str):
    if type_ not in TYPES:
        logger.error(f"Unknown type: {type_}.")
        raise TypeError

    return map(TYPES[type_], stream)


def pipe(stream: Iterable[Element], *args):
    iter_ = zip(tee(stream, len(args)), args)
    iter__ = starmap(parse_stream, iter_)

    return chain.from_iterable(iter__)


def _dt_lt(strict, value):
    try:
        return datetime.strptime(value[:19], TIME_FORMAT) < datetime.now()
    except ValueError as e:
        if strict:
            raise e
        else:
            return True


def _dt_gt(strict, value):
    try:
        return datetime.strptime(value[:19], TIME_FORMAT) > datetime.now()
    except ValueError as e:
        if strict:
            raise e
        else:
            return True


OPS = {'s': select,
       'fa': filter_attribute,
       'fv': filter_value,
       'a': apply,
       'p': pipe}

TYPES = {}

MAGICS = {'<%d': _dt_lt,
         '>%d': _dt_gt}

FILTERS = {}
