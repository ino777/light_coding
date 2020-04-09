import re

class Singleton(object):
    _instance = None

    def __init__(self):
        raise NotImplementedError('not allowed')

    @classmethod
    def get_instance(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = cls(*args, **kwargs)
        return cls._instance


class Node(object):
    def __init__(self, value, parent=None, children=None):
        self.value = value
        self.parent = parent
        if children is None:
            self.children = []
    
    def is_leaf(self):
        return self.children == []
    
    def previous(self):
        parent = self.parent
        if parent is None:
            return None
        brothers = parent.children
        index = brothers.index(self)
        previous_index = index - 1
        if previous_index >= 0:
            return brothers[previous_index]
        previous_parent = parent.previous()
        if previous_parent is None:
            return None
        if previous_parent.is_leaf():
            return previous_parent
        return previous_parent.children[-1]
    
    def next(self):
        parent = self.parent
        if parent is None:
            return None
        brothers = parent.children
        index = brothers.index(self)
        next_index = index + 1
        if next_index < len(brothers):
            return brothers[next_index]
        next_parent = parent.next()
        if next_parent is None:
            return None
        if next_parent.is_leaf():
            return next_parent
        return next_parent.children[0]
    
    def add_child(self, node):
        self.children.append(node)
        node.parent = self
    
    def match_children(self, value):
        for child in self.children:
            if value == child.value:
                return child
        return None

class Router(Singleton):
    def __init__(self, root=''):
        self.root = Node(root)
        self.routes = []
    
    def register(self, path):
        values = re.split(r'[/\\]', path)
        tail = self.root
        for value in values:
            if not value:
                continue
            child = tail.match_children(value)
            if not child:
                child = Node(value)
                tail.add_child(child)
                self.routes.append(child)
            tail = child
    
    def valid_path(self, path):
        values = re.split(r'[/\\]', path)
        tail = self.root
        for value in values:
            if not value:
                continue
            child = tail.match_children(value)
            if not child:
                return False
            tail = child
        return True
    
    def get_path(self, *args):
        path = '/' + '/'.join(args)
        if self.valid_path(path):
            return path
        return ''
    
    def get_tail(self, path):
        if not self.valid_path(path):
            raise ValueError('invalid path: ' + path)
        values = re.split(r'[/\\]', path)
        tail = self.root
        for value in values:
            if not value:
                continue
            child = tail.match_children(value)
            if child.is_leaf():
                return child
            tail = child
        return tail

    def get_path_from_leaf(self, leaf, limit=20):
        if leaf is None:
            return ''
        path = leaf.value
        for _ in range(limit):
            leaf = leaf.parent
            if leaf is None:
                break
            path = leaf.value + '/' + path
        return path

    def previous_path(self, path):
        if not self.valid_path(path):
            raise ValueError('invalid path: ' + path)
        tail = self.get_tail(path)
        previous_leaf = tail.previous()
        return self.get_path_from_leaf(previous_leaf)

    def next_path(self, path):
        if not self.valid_path(path):
            raise ValueError('invalid path: ' + path)
        tail = self.get_tail(path)
        next_leaf = tail.next()
        return self.get_path_from_leaf(next_leaf)



router = Router.get_instance()
router.register('/python/list')
router.register('/python/basics/1')
router.register('/python/basics/2')