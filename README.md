# XML LoadExtractTransform

This tool is a generic *iterator* based XML parser that uses a concise syntax to 
express **filters** that can be split, joined and used to apply custom functions to
(sub)elements of the XML document.

The main functions are `parse_file`, `parse_stream` together with the `register_types`
and `register_filters` functions.

## How to use XML_LET

A minimal usage of this package involves creating "types" and "filters" which you then
register using the `register_*` functions.

After that you either parse a file with `parse_file` or an existing `Iterable[Element]`
 with `parse_stream`. Here `Element` is alias for the `xml.dom.minidom.Element` type. 

For example, assuming types and filters have been registered, and letting `root` be
the root `Element` of the document (you can obtain this by parsing the XML with the
`minidom` package), you obtain an `Iterable` containing the parsed, filtered and
transformed subelements specified in your filter by calling:

```python
parse_stream([root], my_filter)
```

where `my_filter` is the identifier for the filter you registered.

You also have the option of registering "MAGIC" conditions. The standard `xml_let`
already provides two "MAGICS" that allows for comparison of XML timestamps.

## How to create types

A `type` in the context of `XML_LET` is any function with signature:

```python
(el: xml.dom.minidom.Element) -> Any
```

You should use this function to make any transformation you want to this element.
The most predominant use-case is to do the final conversion of the XML subelement
you are interested in into an easy to use `Object` of choice. Note that if you want
to further pipe the resulting objects into other filters you need to return a valid
object of type `xml.dom.minidom.Element`. In essence the only composable streams
are streams of this type.

You can create any number of types and then register them with the `register_types`
functions which take a dictionary of `identifier: <function>` pairs.

## How to create filters

A `filter` in `XML_LET` is an object of type `List[str]` where each element is a 
specially encoded string. The encoding follows the following syntax:

```
<op>|<arg1>[|arg2|...|argN]
```

where `op` can be one of the operations defined in `xmllet.builtin.OPS` and `arg_i`
is a generic argument.

Each `op` has different requirements concerning number of arguments allowed. We will
now list the current supported operations.

### Select

```
s|<path>
```

Expects one argument: the dot (.) delimited path to the subelement to be selected. This
operation will return *all* subelements of the current element selection present 
in this path. Note that (as of now) only the last path segment (the actual element
type you want to select) can be non-unique. **In other words the path to the selected
subelements must be unique**. This might change in the future.

### Filter attribute

```
fa|<attribute>|<cond>
```

Expect two arguments: the attribute identifier string (including the namespace if
present) and the conditional value. This will filter the incoming stream of elements
by the referenced attribute and condition. The `cond` argument can, optionally, be 
one of the "MAGIC" conditions. Built-in only less than/greater than comparison to 
the current datetime stamp are implemented via the `<%d` and `>%d` magic conditions.
You can register your own magic commands with `register_magics`.
 
### Filter value

```
fv|<t|f>|<path>|<cond>
```

Expects three arguments.

The first is either `t` or `f` standing for the *boolean*
value whether the filtering should be **strict** or **non-strict**. Strict filtering
implies that the relevant `path` **must** exist else an exception will be raised.
Non-strict filtering allows non-existing subelement paths to bypass the filter. This
is useful in condition where you want to filter only if something *is* present.

The second argument `path` is the subelement path containing the value to be filtered.
This does **not** imply a selection. In this way, you can filter on values of 
subelements and continue parsing other subelements.

Finally `cond`, is the condition to be filtered on. As in the `fa` command you can
pass a "MAGIC" condition.
   
### Apply

```
a|<type_identifier>
```

Expects exactly one argument: the type identifier that has been pre-registered.
This command simply applies the corresponding type creator function to each element
in the stream.
 
### Pipe

```
p|<filter_1>[|<filter_2>|...|<filter_N>]
```

Expects at one or more arguments: each being one filter identifier. This command
provides a generic way to concatenate and fan-out the stream with other filters.
Of course, the filters must have been pre-registered.

## How to create MAGIC conditions

As mentioned before conditions are either equality comparisons to a value or a "MAGIC"
conditional. Built-in `xml_let` provides both `<%d` and `>%d` magics for comparison
of timestamps. You can create your own magic and register it with the 
`register_magics` function.

A "MAGIC" conditional is a function with the following signature:

```python
(strict: bool, value: str) -> bool
``` 

The function should decide if `str` should be filtered **out** by returning a boolean.
Note that this means that a return value of `True` **is filtered**. Only values for
which the return value is `False` remain in the stream.

The *boolean* argument `strict` is a passed in automatically by the calling command
and the magic condition **should** raise an exception if parsing errors occur inside
the function in case `strict` is `True`. Otherwise, **you should ignore the error and
return** `False` (which keeps the element in the stream).
