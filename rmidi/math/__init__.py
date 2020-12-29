from . import functions
from . import sequences
from . import generators

function   = dict([(val, getattr(functions, val)) for val in dir(functions)])
sequence  = dict([(val, getattr(sequences, val)) for val in dir(sequences)])
generator = dict([(val, getattr(generators, val)) for val in dir(generators)])