# -*- coding: utf-8 -*-
"""
Created on Mon Jan 13 18:17:15 2014

@author: takluyver
"""
from inspect import signature, Parameter
from functools import wraps

def callback_prototype(prototype):
    protosig = signature(prototype)
    positional, keyword = [], []
    for name, param in protosig.parameters.items():
        if param.kind in (Parameter.VAR_POSITIONAL, Parameter.VAR_KEYWORD):
            raise TypeError("*args/**kwargs not supported in prototypes")

        if (param.default is not Parameter.empty) \
            or (param.kind == Parameter.KEYWORD_ONLY):
            keyword.append(name)
        else:
            positional.append(name)
        
    kwargs = dict.fromkeys(keyword)
    def adapt(callback):
        sig = signature(callback)
        try:
            # XXX: callback can have extra optional parameters - OK?
            sig.bind(*positional, **kwargs)
            return callback
        except TypeError:
            pass
        
        # Match up arguments
        unmatched_pos = positional[:]
        unmatched_kw = kwargs.copy()
        unrecognised = []
        # TODO: unrecognised parameters with default values - OK?
        for name, param in sig.parameters.items():
            print(name, param.kind)
            if param.kind == Parameter.POSITIONAL_ONLY:
                if len(unmatched_pos) > 0:
                    unmatched_pos.pop(0)
                else:
                    unrecognised.append(name)
            elif param.kind == Parameter.POSITIONAL_OR_KEYWORD:
                if len(unmatched_pos) > 0:
                    unmatched_pos.pop(0)
                elif name in unmatched_kw:
                    unmatched_kw.pop(name)
                else:
                    unrecognised.append(name)
            elif param.kind == Parameter.VAR_POSITIONAL:
                unmatched_pos = []
            elif param.kind == Parameter.KEYWORD_ONLY:
                if name in unmatched_kw:
                    unmatched_kw.pop(name)
                else:
                    unrecognised.append(name)
            else:  # VAR_KEYWORD
                unmatched_kw = {}
        
            print(unmatched_pos, unmatched_kw, unrecognised)
        
        if unrecognised:
            raise TypeError("Function {!r} had unmatched arguments: {}".format(callback, unrecognised))

        cut_positional = len(unmatched_pos)

        @wraps(callback)
        def adapted(*args, **kwargs):
#            print(args, kwargs)
            if cut_positional:
                args = args[:-cut_positional]
            for name in unmatched_kw:
                # XXX: Could name not be in kwargs?
                kwargs.pop(name)
#            print(args, kwargs, unmatched_pos, cut_positional, unmatched_kw)
            return callback(*args, **kwargs)
        
        return adapted

    return adapt