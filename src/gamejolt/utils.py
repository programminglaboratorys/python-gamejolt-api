class AttrDict(dict):
    def __getattr__(self, attr):
        try:
            return self[attr]
        except KeyError:
            raise AttributeError(attr) from None

    def __setattr__(self, attr, value):
        self[attr] = value

    def __delattr__(self, attr):
        try:
            del self[attr]
        except KeyError:
            raise AttributeError(attr) from None

    def __dir__(self):
        return list(self) + dir(type(self))
    
    def __repr__(self):
        return f"AttrDict({dict.__repr__(self)})"