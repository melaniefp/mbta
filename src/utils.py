import functools

def cache(func):
    """Keep a cache of previous function calls"""
    @functools.wraps(func)
    def wrapper_cache(*args, **kwargs):
        cache_key = args + tuple(kwargs.items())
        if cache_key not in wrapper_cache.cache:
            wrapper_cache.cache[cache_key] = func(*args, **kwargs)
        return wrapper_cache.cache[cache_key]
    wrapper_cache.cache = dict()
    return wrapper_cache

def cached_property(fun):
    """A memoize decorator for class properties."""
    @functools.wraps(fun)
    def get(self):
        try:
            return self._cache[fun]
        except AttributeError:
            self._cache = {}
        except KeyError:
            pass
        ret = self._cache[fun] = fun(self)
        return ret
    return property(get)

def get_id_tuple(f, args, kwargs, mark=object()):
    """ 
    Some quick'n'dirty way to generate a unique key for an specific call.
    """
    l = [id(f)]
    for arg in args:
        l.append(id(arg))
    l.append(id(mark))
    for k, v in kwargs:
        l.append(k)
        l.append(id(v))
    return tuple(l)

def memoize(f):
    """ 
    Some basic memoizer
    """
    _memoized = {}
    def memoized(*args, **kwargs):
        key = get_id_tuple(f, args, kwargs)
        if key not in _memoized:
            _memoized[key] = f(*args, **kwargs)
        import pdb; pdb.set_trace()
        return _memoized[key]
    return memoized

class Memoize:

    def __init__(self, fn):
        self.fn = fn
        self.memo = {}

    def __call__(self, *args):
        if args not in self.memo:
            self.memo[args] = self.fn(*args)
        return self.memo[args]
