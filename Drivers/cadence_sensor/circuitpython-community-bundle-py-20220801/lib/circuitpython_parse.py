"""Parse (absolute and relative) URLs, tweaked to work with CircuitPython
==========================================================================================

urlparse module is based upon the following RFC specifications.

RFC 3986 (STD66): "Uniform Resource Identifiers" by T. Berners-Lee, R. Fielding
and L.  Masinter, January 2005.

RFC 2732 : "Format for Literal IPv6 Addresses in URL's by R.Hinden, B.Carpenter
and L.Masinter, December 1999.

RFC 2396:  "Uniform Resource Identifiers (URI)": Generic Syntax by T.
Berners-Lee, R. Fielding, and L. Masinter, August 1998.

RFC 2368: "The mailto URL scheme", by P.Hoffman , L Masinter, J. Zawinski, July 1998.

RFC 1808: "Relative Uniform Resource Locators", by R. Fielding, UC Irvine, June
1995.

RFC 1738: "Uniform Resource Locators (URL)" by T. Berners-Lee, L. Masinter, M.
McCahill, December 1994

RFC 3986 is considered the current standard and any future changes to
urlparse module should conform with it.  The urlparse module is
currently not entirely compliant with this RFC due to defacto
scenarios for parsing, and for backward compatibility purposes, some
parsing quirks from older RFCs are retained. The testcases in
test_urlparse.py provides a good indicator of parsing behavior.
"""

import sys
from collections import namedtuple

# pylint: disable=C0115
# pylint: disable=C0116

__all__ = [
    "urlparse",
    "urlunparse",
    "urljoin",
    "urldefrag",
    "urlsplit",
    "urlunsplit",
    "urlencode",
    "parse_qs",
    "parse_qsl",
    "quote",
    "quote_plus",
    "quote_from_bytes",
    "unquote",
    "unquote_plus",
    "unquote_to_bytes",
    "DefragResult",
    "ParseResult",
    "SplitResult",
    "DefragResultBytes",
    "ParseResultBytes",
    "SplitResultBytes",
]

# A classification of schemes.
# The empty string classifies URLs with no scheme specified,
# being the default value returned by “urlsplit” and “urlparse”.

USES_RELATIVE = [
    "",
    "ftp",
    "http",
    "gopher",
    "nntp",
    "imap",
    "wais",
    "file",
    "https",
    "shttp",
    "mms",
    "prospero",
    "rtsp",
    "rtspu",
    "sftp",
    "svn",
    "svn+ssh",
    "ws",
    "wss",
]

USES_NETLOC = [
    "",
    "ftp",
    "http",
    "gopher",
    "nntp",
    "telnet",
    "imap",
    "wais",
    "file",
    "mms",
    "https",
    "shttp",
    "snews",
    "prospero",
    "rtsp",
    "rtspu",
    "rsync",
    "svn",
    "svn+ssh",
    "sftp",
    "nfs",
    "git",
    "git+ssh",
    "ws",
    "wss",
]

USES_PARAMS = ["", "ftp", "hdl", "prospero", "http", "imap", "https", "shttp", "rtsp", "rtspu", "sip", "sips", "mms", "sftp", "tel"]

# These are not actually used anymore, but should stay for backwards
# compatibility.  (They are undocumented, but have a public-looking name.)

NON_HIERARCHICAL = ["gopher", "hdl", "mailto", "news", "telnet", "wais", "imap", "snews", "sip", "sips"]

USES_QUERY = ["", "http", "wais", "imap", "https", "shttp", "mms", "gopher", "rtsp", "rtspu", "sip", "sips"]

USES_FRAGMENT = ["", "ftp", "hdl", "http", "gopher", "news", "nntp", "wais", "https", "shttp", "snews", "file", "prospero"]

# Characters valid in scheme names
SCHEME_CHARS = "abcdefghijklmnopqrstuvwxyz" "ABCDEFGHIJKLMNOPQRSTUVWXYZ" "0123456789" "+-."

MAX_CACHE_SIZE = 20
PARSE_CACHE = {}


def clear_cache():
    """Clear the parse cache and the quoters cache."""
    PARSE_CACHE.clear()
    SAFE_QUOTERS.clear()


# Helpers for bytes handling
# For 3.2, we deliberately require applications that
# handle improperly quoted URLs to do their own
# decoding and encoding. If valid use cases are
# presented, we may relax this by using latin-1
# decoding internally for 3.3
IMPLICIT_ENCODING = "ascii"
IMPLICIT_ERRORS = "strict"


def _noop(obj):
    return obj


def _encode_result(obj, encoding=IMPLICIT_ENCODING, errors=IMPLICIT_ERRORS):
    return obj.encode(encoding, errors)


def _decode_args(args, encoding=IMPLICIT_ENCODING, errors=IMPLICIT_ERRORS):
    return tuple(x.decode(encoding, errors) if x else "" for x in args)


def _coerce_args(*args):
    # Invokes decode if necessary to create str args
    # and returns the coerced inputs along with
    # an appropriate result coercion function
    #   - noop for str inputs
    #   - encoding function otherwise
    str_input = isinstance(args[0], str)
    for arg in args[1:]:
        # We special-case the empty string to support the
        # "scheme=''" default argument to some functions
        if arg and isinstance(arg, str) != str_input:
            raise TypeError("Cannot mix str and non-str arguments")
    if str_input:
        return args + (_noop,)
    return _decode_args(args) + (_encode_result,)


# Result objects are more helpful than simple tuples
class _ResultMixinStr:
    """Standard approach to encoding parsed results from str to bytes"""

    __slots__ = ()

    def encode(self, encoding="ascii", errors="strict"):
        # pylint: disable=E1101,E1133
        return self._encoded_counterpart(*(x.encode(encoding, errors) for x in self))


class _ResultMixinBytes:
    """Standard approach to decoding parsed results from bytes to str"""

    __slots__ = ()

    def decode(self, encoding="ascii", errors="strict"):
        # pylint: disable=E1101,E1133
        return self._decoded_counterpart(*(x.decode(encoding, errors) for x in self))


class _NetlocResultMixinBase:
    """Shared methods for the parsed result objects containing a netloc element"""

    __slots__ = ()

    @property
    def username(self):
        # pylint: disable=E1101
        return self._userinfo[0]

    @property
    def password(self):
        # pylint: disable=E1101
        return self._userinfo[1]

    @property
    def hostname(self):
        # pylint: disable=E1101
        hostname = self._hostinfo[0]
        if not hostname:
            return None
        # Scoped IPv6 address may have zone info, which must not be lowercased
        # like http://[fe80::822a:a8ff:fe49:470c%tESt]:1234/keys
        separator = "%" if isinstance(hostname, str) else b"%"
        hostname, percent, zone = hostname.partition(separator)
        return hostname.lower() + percent + zone

    @property
    def port(self):
        # pylint: disable=E1101
        port = self._hostinfo[1]
        if port is not None:
            try:
                port = int(port, 10)
            except ValueError:
                message = "Port could not be cast to integer value as {port}".format(port=port)
                raise ValueError(message) from None

            # pylint: disable=C0325
            if not (0 <= port <= 65535):
                raise ValueError("Port out of range 0-65535")
        return port


class _NetlocResultMixinStr(_NetlocResultMixinBase, _ResultMixinStr):
    __slots__ = ()

    @property
    def _userinfo(self):
        # pylint: disable=E1101
        netloc = self.netloc
        userinfo, have_info, _ = netloc.rpartition("@")
        if have_info:
            username, have_password, password = userinfo.partition(":")
            if not have_password:
                password = None
        else:
            username = password = None
        return username, password

    @property
    def _hostinfo(self):
        # pylint: disable=E1101
        netloc = self.netloc
        _, _, hostinfo = netloc.rpartition("@")
        _, have_open_br, bracketed = hostinfo.partition("[")
        if have_open_br:
            hostname, _, port = bracketed.partition("]")
            _, _, port = port.partition(":")
        else:
            hostname, _, port = hostinfo.partition(":")
        if not port:
            port = None
        return hostname, port


class _NetlocResultMixinBytes(_NetlocResultMixinBase, _ResultMixinBytes):
    __slots__ = ()

    @property
    def _userinfo(self):
        # pylint: disable=E1101
        netloc = self.netloc
        userinfo, have_info, _ = netloc.rpartition(b"@")
        if have_info:
            username, have_password, password = userinfo.partition(b":")
            if not have_password:
                password = None
        else:
            username = password = None
        return username, password

    @property
    def _hostinfo(self):
        # pylint: disable=E1101
        netloc = self.netloc
        _, _, hostinfo = netloc.rpartition(b"@")
        _, have_open_br, bracketed = hostinfo.partition(b"[")
        if have_open_br:
            hostname, _, port = bracketed.partition(b"]")
            _, _, port = port.partition(b":")
        else:
            hostname, _, port = hostinfo.partition(b":")
        if not port:
            port = None
        return hostname, port


_DefragResultBase = namedtuple("DefragResult", "url fragment")
_SplitResultBase = namedtuple("SplitResult", "scheme netloc path query fragment")
_ParseResultBase = namedtuple("ParseResult", "scheme netloc path params query fragment")

# For backwards compatibility, alias _NetlocResultMixinStr
# ResultBase is no longer part of the documented API, but it is
# retained since deprecating it isn't worth the hassle
ResultBase = _NetlocResultMixinStr

# Structured result objects for string data
# pylint: disable=C0115
class DefragResult(_DefragResultBase, _ResultMixinStr):
    __slots__ = ()

    def geturl(self):
        if self.fragment:
            return self.url + "#" + self.fragment

        return self.url


# pylint: disable=C0115
class SplitResult(_SplitResultBase, _NetlocResultMixinStr):
    __slots__ = ()

    def geturl(self):
        return urlunsplit(self)


# pylint: disable=C0115
class ParseResult(_ParseResultBase, _NetlocResultMixinStr):
    __slots__ = ()

    def geturl(self):
        return urlunparse(self)


# Structured result objects for bytes data
# pylint: disable=C0115
class DefragResultBytes(_DefragResultBase, _ResultMixinBytes):
    __slots__ = ()

    def geturl(self):
        if self.fragment:
            return self.url + b"#" + self.fragment

        return self.url


# pylint: disable=C0115
class SplitResultBytes(_SplitResultBase, _NetlocResultMixinBytes):
    __slots__ = ()

    def geturl(self):
        return urlunsplit(self)


# pylint: disable=C0115
class ParseResultBytes(_ParseResultBase, _NetlocResultMixinBytes):
    __slots__ = ()

    def geturl(self):
        return urlunparse(self)


# Set up the encode/decode result pairs
def _fix_result_transcoding():
    _result_pairs = (
        (DefragResult, DefragResultBytes),
        (SplitResult, SplitResultBytes),
        (ParseResult, ParseResultBytes),
    )
    for _decoded, _encoded in _result_pairs:
        # pylint: disable=W0212
        _decoded._encoded_counterpart = _encoded
        _encoded._decoded_counterpart = _decoded


_fix_result_transcoding()
del _fix_result_transcoding


def urlparse(url, scheme="", allow_fragments=True):
    """Parse a URL into 6 components:
    <scheme>://<netloc>/<path>;<params>?<query>#<fragment>

    The result is a named 6-tuple with fields corresponding to the
    above. It is either a ParseResult or ParseResultBytes object,
    depending on the type of the url parameter.

    The username, password, hostname, and port sub-components of netloc
    can also be accessed as attributes of the returned object.

    The scheme argument provides the default value of the scheme
    component when no scheme is found in url.

    If allow_fragments is False, no attempt is made to separate the
    fragment component from the previous component, which can be either
    path or query.

    Note that % escapes are not expanded.
    """
    url, scheme, _coerce_result = _coerce_args(url, scheme)
    splitresult = urlsplit(url, scheme, allow_fragments)
    scheme, netloc, url, query, fragment = splitresult
    if scheme in USES_PARAMS and ";" in url:
        url, params = _splitparams(url)
    else:
        params = ""
    result = ParseResult(scheme, netloc, url, params, query, fragment)
    return _coerce_result(result)


def _splitparams(url):
    if "/" in url:
        i = url.find(";", url.rfind("/"))
        if i < 0:
            return url, ""
    else:
        i = url.find(";")
    return url[:i], url[i + 1 :]


def _splitnetloc(url, start=0):
    delim = len(url)  # position of end of domain part of url, default is end
    for char in "/?#":  # look for delimiters; the order is NOT important
        wdelim = url.find(char, start)  # find first of this delim
        if wdelim >= 0:  # if found
            delim = min(delim, wdelim)  # use earliest delim position
    return url[start:delim], url[delim:]  # return (domain, rest)


def isascii(string):
    for char in string:
        if ord(char) > 0x7F:
            return False
    return True


def _checknetloc(netloc):
    if not netloc or isascii(netloc):
        return
    # looking for characters like \u2100 that expand to 'a/c'
    # IDNA uses NFKC equivalence, so normalize for this check
    n = netloc.replace("@", "")  # ignore characters already included
    n = n.replace(":", "")  # but not the surrounding text
    n = n.replace("#", "")
    n = n.replace("?", "")
    netloc2 = n
    if n == netloc2:
        return
    for char in "/?#@:":
        if char in netloc2:
            raise ValueError("netloc '" + netloc + "' contains invalid " + "characters under NFKC normalization")


def urlsplit(url, scheme="", allow_fragments=True):
    """Parse a URL into 5 components:
    <scheme>://<netloc>/<path>?<query>#<fragment>

    The result is a named 5-tuple with fields corresponding to the
    above. It is either a SplitResult or SplitResultBytes object,
    depending on the type of the url parameter.

    The username, password, hostname, and port sub-components of netloc
    can also be accessed as attributes of the returned object.

    The scheme argument provides the default value of the scheme
    component when no scheme is found in url.

    If allow_fragments is False, no attempt is made to separate the
    fragment component from the previous component, which can be either
    path or query.

    Note that % escapes are not expanded.
    """

    url, scheme, _coerce_result = _coerce_args(url, scheme)
    allow_fragments = bool(allow_fragments)
    key = url, scheme, allow_fragments, type(url), type(scheme)
    cached = PARSE_CACHE.get(key, None)
    if cached:
        return _coerce_result(cached)
    if len(PARSE_CACHE) >= MAX_CACHE_SIZE:  # avoid runaway growth
        clear_cache()
    netloc = query = fragment = ""
    i = url.find(":")
    if i > 0:
        for char in url[:i]:
            if char not in SCHEME_CHARS:
                break
        else:
            scheme, url = url[:i].lower(), url[i + 1 :]

    if url[:2] == "//":
        netloc, url = _splitnetloc(url, 2)
        if ("[" in netloc and "]" not in netloc) or ("]" in netloc and "[" not in netloc):
            raise ValueError("Invalid IPv6 URL")
    if allow_fragments and "#" in url:
        url, fragment = url.split("#", 1)
    if "?" in url:
        url, query = url.split("?", 1)
    _checknetloc(netloc)
    val = SplitResult(scheme, netloc, url, query, fragment)
    PARSE_CACHE[key] = val
    return _coerce_result(val)


def urlunparse(components):
    """Put a parsed URL back together again.  This may result in a
    slightly different, but equivalent URL, if the URL that was parsed
    originally had redundant delimiters, e.g. a ? with an empty query
    (the draft states that these are equivalent)."""
    scheme, netloc, url, params, query, fragment, _coerce_result = _coerce_args(*components)
    if params:
        url = "%s;%s" % (url, params)
    return _coerce_result(urlunsplit((scheme, netloc, url, query, fragment)))


def urlunsplit(components):
    """Combine the elements of a tuple as returned by urlsplit() into a
    complete URL as a string. The data argument can be any five-item iterable.
    This may result in a slightly different, but equivalent URL, if the URL that
    was parsed originally had unnecessary delimiters (for example, a ? with an
    empty query; the RFC states that these are equivalent)."""
    scheme, netloc, url, query, fragment, _coerce_result = _coerce_args(*components)
    if netloc or (scheme and scheme in USES_NETLOC and url[:2] != "//"):
        if url and url[:1] != "/":
            url = "/" + url
        url = "//" + (netloc or "") + url
    if scheme:
        url = scheme + ":" + url
    if query:
        url = url + "?" + query
    if fragment:
        url = url + "#" + fragment
    return _coerce_result(url)


def urljoin(base, url, allow_fragments=True):
    """Join a base URL and a possibly relative URL to form an absolute
    interpretation of the latter."""
    if not base:
        return url
    if not url:
        return base

    base, url, _coerce_result = _coerce_args(base, url)
    bscheme, bnetloc, bpath, bparams, bquery, _ = urlparse(base, "", allow_fragments)
    scheme, netloc, path, params, query, fragment = urlparse(url, bscheme, allow_fragments)

    if scheme != bscheme or scheme not in USES_RELATIVE:
        return _coerce_result(url)
    if scheme in USES_NETLOC:
        if netloc:
            return _coerce_result(urlunparse((scheme, netloc, path, params, query, fragment)))
        netloc = bnetloc

    if not path and not params:
        path = bpath
        params = bparams
        if not query:
            query = bquery
        return _coerce_result(urlunparse((scheme, netloc, path, params, query, fragment)))

    base_parts = bpath.split("/")
    if base_parts[-1] != "":
        # the last item is not a directory, so will not be taken into account
        # in resolving the relative path
        del base_parts[-1]

    # for rfc3986, ignore all base path should the first character be root.
    if path[:1] == "/":
        segments = path.split("/")
    else:
        segments = base_parts + path.split("/")
        # filter out elements that would cause redundant slashes on re-joining
        # the resolved_path
        segments[1:-1] = filter(None, segments[1:-1])

    resolved_path = []

    for seg in segments:
        if seg == "..":
            try:
                resolved_path.pop()
            except IndexError:
                # ignore any .. segments that would otherwise cause an IndexError
                # when popped from resolved_path if resolving for rfc3986
                pass
        elif seg == ".":
            continue
        else:
            resolved_path.append(seg)

    if segments[-1] in (".", ".."):
        # do some post-processing here. if the last segment was a relative dir,
        # then we need to append the trailing '/'
        resolved_path.append("")

    return _coerce_result(urlunparse((scheme, netloc, "/".join(resolved_path) or "/", params, query, fragment)))


def urldefrag(url):
    """Removes any existing fragment from URL.

    Returns a tuple of the defragmented URL and the fragment.  If
    the URL contained no fragments, the second element is the
    empty string.
    """
    url, _coerce_result = _coerce_args(url)
    if "#" in url:
        scheme, netloc, url_val, params, query, frag = urlparse(url)
        defrag = urlunparse((scheme, netloc, url_val, params, query, ""))
    else:
        frag = ""
        defrag = url
    return _coerce_result(DefragResult(defrag, frag))


HEX_DIG = "0123456789ABCDEFabcdef"
HEX_TO_BYTE = None


def unquote_to_bytes(string):
    """unquote_to_bytes('abc%20def') -> b'abc def'."""
    # Note: strings are encoded as UTF-8. This is only an issue if it contains
    # unescaped non-ASCII characters, which URIs should not.
    if not string:
        # Is it a string-like object?
        # pylint: disable=W0104
        string.split
        return b""
    if isinstance(string, str):
        string = string.encode("utf-8")
    bits = string.split(b"%")
    if len(bits) == 1:
        return string
    res = [bits[0]]
    append = res.append
    # Delay the initialization of the table to not waste memory
    # if the function is never called
    # pylint: disable=W0603
    global HEX_TO_BYTE
    if HEX_TO_BYTE is None:
        HEX_TO_BYTE = {(a + b).encode(): bytes.fromhex(a + b) for a in HEX_DIG for b in HEX_DIG}
    for item in bits[1:]:
        try:
            append(HEX_TO_BYTE[item[:2]])
            append(item[2:])
        except KeyError:
            append(b"%")
            append(item)
    return b"".join(res)


def unquote(string, encoding="utf-8", errors="replace"):
    """Replace %xx escapes by their single-character equivalent. The optional
    encoding and errors parameters specify how to decode percent-encoded
    sequences into Unicode characters, as accepted by the bytes.decode()
    method.
    By default, percent-encoded sequences are decoded with UTF-8, and invalid
    sequences are replaced by a placeholder character.

    unquote('abc%20def') -> 'abc def'.
    """
    if isinstance(string, bytes):
        return unquote_to_bytes(string).decode(encoding, errors)
    if "%" not in string:
        # pylint: disable=W0104
        string.split
        return string
    if encoding is None:
        encoding = "utf-8"
    if errors is None:
        errors = "replace"

    current_string = ""
    str_pos = 0

    while str_pos < len(string):
        char = string[str_pos]

        if char == "%":
            part = char + string[str_pos + 1] + string[str_pos + 2]
            decoded_part = unquote_to_bytes(part).decode(encoding, errors)
            current_string = current_string + decoded_part
            str_pos = str_pos + 3
        else:
            current_string = current_string + char
            str_pos = str_pos + 1

    return current_string


# pylint: disable=C0103
def parse_qs(qs, keep_blank_values=False, strict_parsing=False, encoding="utf-8", errors="replace", max_num_fields=None):
    """Parse a query given as a string argument.

        Arguments:

        qs: percent-encoded query string to be parsed

        keep_blank_values: flag indicating whether blank values in
            percent-encoded queries should be treated as blank strings.
            A true value indicates that blanks should be retained as
            blank strings.  The default false value indicates that
            blank values are to be ignored and treated as if they were
            not included.

        strict_parsing: flag indicating what to do with parsing errors.
            If false (the default), errors are silently ignored.
            If true, errors raise a ValueError exception.

        encoding and errors: specify how to decode percent-encoded sequences
            into Unicode characters, as accepted by the bytes.decode() method.

        max_num_fields: int. If set, then throws a ValueError if there
            are more than n fields read by parse_qsl().

        Returns a dictionary.
    """
    parsed_result = {}
    pairs = parse_qsl(qs, keep_blank_values, strict_parsing, encoding=encoding, errors=errors, max_num_fields=max_num_fields)
    for name, value in pairs:
        if name in parsed_result:
            parsed_result[name].append(value)
        else:
            parsed_result[name] = [value]
    return parsed_result


# pylint: disable=C0103
def parse_qsl(qs, keep_blank_values=False, strict_parsing=False, encoding="utf-8", errors="replace", max_num_fields=None):
    """Parse a query given as a string argument.

        Arguments:

        qs: percent-encoded query string to be parsed

        keep_blank_values: flag indicating whether blank values in
            percent-encoded queries should be treated as blank strings.
            A true value indicates that blanks should be retained as blank
            strings.  The default false value indicates that blank values
            are to be ignored and treated as if they were  not included.

        strict_parsing: flag indicating what to do with parsing errors. If
            false (the default), errors are silently ignored. If true,
            errors raise a ValueError exception.

        encoding and errors: specify how to decode percent-encoded sequences
            into Unicode characters, as accepted by the bytes.decode() method.

        max_num_fields: int. If set, then throws a ValueError
            if there are more than n fields read by parse_qsl().

        Returns a list, as G-d intended.
    """
    qs, _coerce_result = _coerce_args(qs)

    # If max_num_fields is defined then check that the number of fields
    # is less than max_num_fields. This prevents a memory exhaustion DOS
    # attack via post bodies with many fields.
    if max_num_fields is not None:
        num_fields = 1 + qs.count("&") + qs.count(";")
        if max_num_fields < num_fields:
            raise ValueError("Max number of fields exceeded")

    pairs = [s2 for s1 in qs.split("&") for s2 in s1.split(";")]
    r = []
    for name_value in pairs:
        if not name_value and not strict_parsing:
            continue
        split_name_value = name_value.split("=", 1)
        if len(split_name_value) != 2:
            if strict_parsing:
                raise ValueError("bad query field: %r" % (name_value,))
            # Handle case of a control-name with no equal sign
            if keep_blank_values:
                split_name_value.append("")
            else:
                continue
        # pylint: disable=C1801
        if len(split_name_value[1]) or keep_blank_values:
            name = split_name_value[0].replace("+", " ")
            name = unquote(name, encoding=encoding, errors=errors)
            name = _coerce_result(name)
            value = split_name_value[1].replace("+", " ")
            value = unquote(value, encoding=encoding, errors=errors)
            value = _coerce_result(value)
            r.append((name, value))
    return r


def unquote_plus(string, encoding="utf-8", errors="replace"):
    """Like unquote(), but also replace plus signs by spaces, as required for
    unquoting HTML form values.

    unquote_plus('%7e/abc+def') -> '~/abc def'
    """
    string = string.replace("+", " ")
    return unquote(string, encoding, errors)


_ALWAYS_SAFE = frozenset(b"ABCDEFGHIJKLMNOPQRSTUVWXYZ" b"abcdefghijklmnopqrstuvwxyz" b"0123456789" b"_.-~")
_ALWAYS_SAFE_BYTES = bytes(_ALWAYS_SAFE)
SAFE_QUOTERS = {}


# pylint: disable=C0103
class defaultdict:
    """
    Default Dict Implementation.

    Defaultdcit that returns the key if the key is not found in dictionnary (see
    unswap in karma-lib):
    >>> d = defaultdict(default=lambda key: key)
    >>> d['foo'] = 'bar'
    >>> d['foo']
    'bar'
    >>> d['baz']
    'baz'
    DefaultDict that returns an empty string if the key is not found (see
    prefix in karma-lib for typical usage):
    >>> d = defaultdict(default=lambda key: '')
    >>> d['foo'] = 'bar'
    >>> d['foo']
    'bar'
    >>> d['baz']
    ''
    Representation of a default dict:
    >>> defaultdict([('foo', 'bar')])
    defaultdict(None, {'foo': 'bar'})
    """

    @staticmethod
    # pylint: disable=W0613
    def __new__(cls, default_factory=None, **kwargs):
        # Some code (e.g. urllib.urlparse) expects that basic defaultdict
        # functionality will be available to subclasses without them
        # calling __init__().
        self = super(defaultdict, cls).__new__(cls)
        # pylint: disable=C0103
        self.d = {}
        return self

    def __init__(self, default_factory=None, **kwargs):
        self.d = kwargs
        self.default_factory = default_factory

    def __getitem__(self, key):
        try:
            return self.d[key]
        except KeyError:
            val = self.__missing__(key)
            self.d[key] = val
            return val

    def __setitem__(self, key, val):
        self.d[key] = val

    def __delitem__(self, key):
        del self.d[key]

    def __contains__(self, key):
        return key in self.d

    def __missing__(self, key):
        if self.default_factory is None:
            raise KeyError(key)
        return self.default_factory()


class Quoter(defaultdict):
    """A mapping from bytes (in range(0,256)) to strings.

    String values are percent-encoded byte values, unless the key < 128, and
    in the "safe" set (either the specified safe set, or default set).
    """

    # Keeps a cache internally, using defaultdict, for efficiency (lookups
    # of cached keys don't call Python code at all).
    def __init__(self, safe):
        """safe: bytes object."""
        super(Quoter, self).__init__()
        self.safe = _ALWAYS_SAFE.union(safe)

    def __missing__(self, b):
        # Handle a cache miss. Store quoted string in cache and return.
        res = chr(b) if b in self.safe else "%{:02X}".format(b)
        self[b] = res
        return res


def quote(string, safe="/", encoding=None, errors=None):
    """quote('abc def') -> 'abc%20def'

    Each part of a URL, e.g. the path info, the query, etc., has a
    different set of reserved characters that must be quoted. The
    quote function offers a cautious (not minimal) way to quote a
    string for most of these parts.

    The quote function %-escapes all characters that are neither in the
    unreserved chars ("always safe") nor the additional chars set via the
    safe arg.

    The default for the safe arg is '/'. The character is reserved, but in
    typical usage the quote function is being called on a path where the
    existing slash characters are to be preserved.

    Python 3.7 updates from using RFC 2396 to RFC 3986 to quote URL strings.
    Now, "~" is included in the set of unreserved characters.

    string and safe may be either str or bytes objects. encoding and errors
    must not be specified if string is a bytes object.

    The optional encoding and errors parameters specify how to deal with
    non-ASCII characters, as accepted by the str.encode method.
    By default, encoding='utf-8' (characters are encoded with UTF-8), and
    errors='strict' (unsupported characters raise a UnicodeEncodeError).
    """
    if isinstance(string, str):
        if not string:
            return string
        if encoding is None:
            encoding = "utf-8"
        if errors is None:
            errors = "strict"
        string = string.encode(encoding, errors)
    else:
        if encoding is not None:
            raise TypeError("quote() doesn't support 'encoding' for bytes")
        if errors is not None:
            raise TypeError("quote() doesn't support 'errors' for bytes")
    return quote_from_bytes(string, safe)


def quote_plus(string, safe="", encoding=None, errors=None):
    """Like quote(), but also replace ' ' with '+', as required for quoting
    HTML form values. Plus signs in the original string are escaped unless
    they are included in safe. It also does not have safe default to '/'.
    """
    # Check if ' ' in string, where string may either be a str or bytes.  If
    # there are no spaces, the regular quote will produce the right answer.
    if (isinstance(string, str) and " " not in string) or (isinstance(string, bytes) and b" " not in string):
        return quote(string, safe, encoding, errors)
    if isinstance(safe, str):
        space = " "
    else:
        space = b" "
    string = quote(string, safe + space, encoding, errors)
    return string.replace(" ", "+")


def quote_from_bytes(bytes_val, safe="/"):
    """Like quote(), but accepts a bytes object rather than a str, and does
    not perform string-to-bytes encoding.  It always returns an ASCII string.
    quote_from_bytes(b'abc def\x3f') -> 'abc%20def%3f'
    """
    if not isinstance(bytes_val, (bytes, bytearray)):
        raise TypeError("quote_from_bytes() expected bytes")
    if not bytes_val:
        return ""
    if isinstance(safe, str):
        # Normalize 'safe' by converting to bytes and removing non-ASCII chars
        safe = safe.encode("ascii", "ignore")
    else:
        safe = bytes([char for char in safe if char < 128])
    if not bytes_val.rstrip(_ALWAYS_SAFE_BYTES + safe):
        return bytes_val.decode()
    try:
        quoter = SAFE_QUOTERS[safe]
    except KeyError:
        SAFE_QUOTERS[safe] = quoter = Quoter(safe).__getitem__
    return "".join([quoter(char) for char in bytes_val])


def urlencode(query, doseq=False, safe="", encoding=None, errors=None, quote_via=quote_plus):
    """Encode a dict or sequence of two-element tuples into a URL query string.

    If any values in the query arg are sequences and doseq is true, each
    sequence element is converted to a separate parameter.

    If the query arg is a sequence of two-element tuples, the order of the
    parameters in the output will match the order of parameters in the
    input.

    The components of a query arg may each be either a string or a bytes type.

    The safe, encoding, and errors parameters are passed down to the function
    specified by quote_via (encoding and errors only if a component is a str).
    """

    if hasattr(query, "items"):
        query = query.items()
    else:
        # It's a bother at times that strings and string-like objects are
        # sequences.
        try:
            # non-sequence items should not work with len()
            # non-empty strings will fail this
            # pylint: disable=C1801
            if len(query) and not isinstance(query[0], tuple):
                raise TypeError
            # Zero-length sequences of all types will get here and succeed,
            # but that's a minor nit.  Since the original implementation
            # allowed empty dicts that type of behavior probably should be
            # preserved for consistency
        except TypeError:
            _, _, traceback = sys.exc_info()
            raise TypeError("not a valid non-string sequence " "or mapping object").with_traceback(traceback)

    lst = []
    if not doseq:
        for key, val in query:
            if isinstance(key, bytes):
                key = quote_via(key, safe)
            else:
                key = quote_via(str(key), safe, encoding, errors)

            if isinstance(val, bytes):
                val = quote_via(val, safe)
            else:
                val = quote_via(str(val), safe, encoding, errors)
            lst.append(key + "=" + val)
    else:
        for key, val in query:
            if isinstance(key, bytes):
                key = quote_via(key, safe)
            else:
                key = quote_via(str(key), safe, encoding, errors)

            if isinstance(val, bytes):
                val = quote_via(val, safe)
                lst.append(key + "=" + val)
            elif isinstance(val, str):
                val = quote_via(val, safe, encoding, errors)
                lst.append(key + "=" + val)
            else:
                try:
                    # Is this a sufficient test for sequence-ness?
                    _ = len(val)
                except TypeError:
                    # not a sequence
                    val = quote_via(str(val), safe, encoding, errors)
                    lst.append(key + "=" + val)
                else:
                    # loop over the sequence
                    for elt in val:
                        if isinstance(elt, bytes):
                            elt = quote_via(elt, safe)
                        else:
                            elt = quote_via(str(elt), safe, encoding, errors)
                        lst.append(key + "=" + elt)
    return "&".join(lst)


def unwrap(url):
    """Transform a string like '<URL:scheme://host/path>' into 'scheme://host/path'.

    The string is returned unchanged if it's not a wrapped URL.
    """
    url = str(url).strip()
    if url[:1] == "<" and url[-1:] == ">":
        url = url[1:-1].strip()
    if url[:4] == "URL:":
        url = url[4:].strip()
    return url
