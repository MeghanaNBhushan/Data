import pkgutil

from lucxbox import tools


def toolnames():
    path = tools.__path__
    prefix = tools.__name__ + '.'
    return (name.partition(prefix)[2] for module_loader, name, ispkg
            in pkgutil.iter_modules(path=path, prefix=prefix))
