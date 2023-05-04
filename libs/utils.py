from importlib import import_module

__all__ = ( 'importer', )


def importer(mod, cls):
    module = import_module(mod)

    if not cls:
        return module

    return getattr(module, cls)
