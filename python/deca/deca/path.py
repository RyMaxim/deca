import os

class UniPath():

    @staticmethod
    def abspath(path):
        return __class__.unify(os.path.abspath(path))
    
    @staticmethod
    def basename(path):
        return os.path.basename(path)

    @staticmethod
    def commonpath(paths):
        try:
            return __class__.unify(os.path.commonpath(paths))
        except:
            return str()

    @staticmethod
    def commonprefix(paths):
        paths = [__class__.unify(path) for path in paths]
        if len(paths) > 0:
            result = paths.pop(0)
            for path in paths:
                i = 0
                while len(result) > i and len(path) > i and result[i] == path[i]:
                    i += 1
                result = result[:i]
            return result
        return str()

    @staticmethod
    def dirname(path):
        return __class__.unify(os.path.dirname(path))

    @staticmethod
    def exists(path):
        return os.path.exists(path)
    
    @staticmethod
    def expanduser(path):
        return os.path.expanduser(path)

    @staticmethod
    def isdir(path):
        return os.path.isdir(path)

    @staticmethod
    def isfile(path):
        return os.path.isfile(path)

    @staticmethod
    def join(path, *paths):
        return __class__.unify(os.path.join(path, *paths))

    @staticmethod
    def normpath(path):
        return __class__.unify(os.path.normpath(path))

    @staticmethod
    def split(path):
        head, tail = os.path.split(path)
        return __class__.unify(head), __class__.unify(tail)

    @staticmethod
    def splitext(path):
        root, ext = os.path.splitext(path)
        return __class__.unify(root), ext

    @staticmethod
    def unify(path):
        if isinstance(path, bytes):
            sep = b'\\'
            extsep = b'/'
        else:
            sep = '\\'
            extsep = '/'
        return path.replace(sep, extsep)
    
