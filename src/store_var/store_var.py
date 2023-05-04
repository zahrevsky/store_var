from abc import ABC, abstractmethod
from typing import Union, SupportsIndex, Callable, List
import pickle


class _Trackable(ABC):
    __slots__ = ()

    onchange_triggers: List[Callable]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.onchange_triggers = []

    def onchange_notify(self):
        pass

    def onchange(self, handler=None):
        if handler is None:
            self.onchange_notify()
        else:
            if handler in self.onchange_triggers:
                raise AttributeError('This @onchange trigger is already set')
            self.onchange_triggers.append(handler)
            return handler

    @abstractmethod
    def _notify_add_one(self, key: int, added):
        pass

    @abstractmethod
    def _notify_remove_one(self, key: int, to_remove):
        pass

    @abstractmethod
    def _notify_add(self, key: Union[SupportsIndex, slice], added):
        pass

    @abstractmethod
    def _notify_remove(self, key: Union[SupportsIndex, slice], to_remove):
        pass

    def _notify_post_remove(self):
        self.onchange()


class _TrackableList(_Trackable, list):
    __slots__ = ('onchange_triggers',)

    def _notify_add(self, key: Union[SupportsIndex, slice], added: Union[tuple, list]):
        length = len(self)
        if isinstance(key, slice):
            for index, value in zip(range(key.start or 0, key.stop or length, key.step or 1), added):
                if index < 0:
                    index += length
                self._notify_add_one(index, value)
        else:
            index = key.__index__()
            if index < 0:
                index += length
            self._notify_add_one(index, added[0])
        if added:
            self.onchange()

    def _notify_remove(self, key: Union[SupportsIndex, slice], to_remove: Union[tuple, list]):
        if isinstance(key, slice):
            for index, value in reversed(list(
                zip(range(key.start or 0, key.stop or len(self), key.step or 1), to_remove)
            )):
                if index < 0:
                    index += len(self)
                self._notify_remove_one(index, value)
        else:
            index = key.__index__()
            if index < 0:
                index += len(self)
            self._notify_remove_one(index, to_remove[0])

    def append(self, __object):
        super().append(__object)

        self._notify_add(-1, (self[-1], ))

    def clear(self):
        length = len(self)
        self._notify_remove(slice(0, length), self)
        super().clear()
        if length:
            self._notify_post_remove()

    def extend(self, __iterable):
        length = len(self)
        super().extend(__iterable)
        self._notify_add(slice(length, len(self)), self[length:len(self)])

    def insert(self, __index, __object):
        index = __index.__index__()
        super().insert(index, __object)
        self._notify_add(index, (self[index], ))

    def pop(self, __index=None):
        if __index is None:
            index = len(self) - 1
        else:
            index = __index.__index__()

        self._notify_remove(index, (self[index], ))
        result = super().pop(__index or -1)
        self._notify_post_remove()
        return result

    def remove(self, __value):
        self._notify_remove(self.index(__value), (__value, ))
        super().remove(__value)
        self._notify_post_remove()

    def copy(self):
        result = type(self)(super().copy())
        result.onchange_triggers = self.onchange_triggers.copy()
        return result

    def reverse(self):
        raise AttributeError('Not implemented yet!')

    def sort(self, *, key=..., reverse=...):
        raise AttributeError('Not implemented yet!')

    def __delitem__(self, key):
        to_remove = self[key]
        if not isinstance(to_remove, (tuple, list)):
            to_remove = (to_remove,)

        self._notify_remove(key, to_remove)
        super().__delitem__(key)
        if to_remove:
            self._notify_post_remove()

    def __iadd__(self, other):
        self.extend(other)
        return self

    def __imul__(self, n):
        length = len(self)
        n = n.__index__()
        if n <= 0:
            self._notify_remove(slice(0, length), self)
        super().__imul__(n)
        if n <= 0:
            if length:
                self._notify_post_remove()
        else:
            self._notify_add(slice(length, len(self)), self[length:len(self)])
        return self

    def __setitem__(self, key, value):
        to_remove = self[key]
        if not isinstance(to_remove, (tuple, list)):
            to_remove = (to_remove,)

        self._notify_remove(key, to_remove)
        super().__setitem__(key, value)
        # TODO: prevent doubling calls of onchange_notify
        if to_remove:
            self._notify_post_remove()

        added = value
        if not isinstance(added, (tuple, list)):
            added = (added,)
        self._notify_add(key, added)

    def __repr__(self):
        return f'{type(self).__name__}({super().__repr__()})'


class stored(_TrackableList):
    def __init__(self, path, iterable=None):
        self._path = str(path)
        if iterable is None:
            super().__init__(self._load())
        else:
            super().__init__(iterable)
            self._store()

    def _store(self):
        with open(self._path, 'wb') as file:
            pickle.dump(list(self), file)

    def _load(self):
        with open(self._path, 'rb') as file:
            data = file.read()
            if len(data) == 0:
                return []
            return pickle.loads(data)

    def _notify_add_one(self, key, value):
        self._store()

    def _notify_post_remove(self):
        super()._notify_post_remove()
        self._store()


__all__ = ['stored']