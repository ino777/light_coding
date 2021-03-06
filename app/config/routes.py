'''
ページ遷移を管理

Router オブジェクトに相対パスを登録し、前ページ・次ページ・子ページを取得できる
Flask だと上記管理ができなそうなので実装
'''



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
    
    def get_brothers(self):
        if self.parent is None:
            return []
        return self.parent.children
    
    def previous(self, depth):
        if depth < 0:
            return None
        parent = self.parent
        if parent is None:
            return None
        brothers = parent.children
        index = brothers.index(self)
        previous_index = index - 1
        if previous_index >= 0:
            return brothers[previous_index]
        previous_parent = parent.previous(depth-1)
        if previous_parent is None:
            return None
        if previous_parent.is_leaf():
            return previous_parent
        return previous_parent.children[-1]
    
    def next(self, depth):
        if depth < 0:
            return None
        parent = self.parent
        if parent is None:
            return None
        brothers = parent.children
        index = brothers.index(self)
        next_index = index + 1
        if next_index < len(brothers):
            return brothers[next_index]
        next_parent = parent.next(depth-1)
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
        self.names = {}
    
    def register(self, path, name=''):
        values = re.split(r'[/\\]', path)
        tail = self.root
        for value in values:
            if not value:
                continue
            child = tail.match_children(value)
            if not child:
                child = Node(value)
                tail.add_child(child)
            tail = child
        self.names[self.get_path_from_leaf(tail)] = name
    
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
        return None
    
    def get_tail(self, path):
        if not self.valid_path(path):
            raise ValueError('invalid path:', path)
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

    def previous_path(self, path, depth=0):
        if not self.valid_path(path):
            raise ValueError('invalid path:', path)
        tail = self.get_tail(path)
        previous_leaf = tail.previous(depth)
        p_path = self.get_path_from_leaf(previous_leaf)
        if not p_path:
            return (None,)*2
        return p_path, self.names[p_path]

    def next_path(self, path, depth=0):
        if not self.valid_path(path):
            raise ValueError('invalid path:', path)
        tail = self.get_tail(path)
        next_leaf = tail.next(depth)
        n_path = self.get_path_from_leaf(next_leaf)
        if not n_path:
            return (None,)*2
        return n_path, self.names[n_path]
    
    def parent(self, path):
        if not self.valid_path(path):
            raise ValueError('invalid path', path)
        tail = self.get_tail(path)
        return tail.parent
    
    def children(self, path):
        if not self.valid_path(path):
            raise ValueError('invalid path:', path)
        tail = self.get_tail(path)
        return tail.children
    
    def brother_paths(self, path):
        if not self.valid_path(path):
            raise ValueError('invalid path:', path)
        tail = self.get_tail(path)
        return [(self.get_path_from_leaf(brother), self.names[self.get_path_from_leaf(brother)]) for brother in tail.get_brothers()]
    
    def _children_recursive(self, tail, paths):
        if tail.is_leaf():
            return (self.get_path_from_leaf(tail), self.names[self.get_path_from_leaf(tail)])

        children_paths = []
        for child in tail.children:
            children_paths.append(self._children_recursive(child, paths))

        if not None in children_paths:
            paths.append([
                (self.get_path_from_leaf(tail), self.names[self.get_path_from_leaf(tail)]),
                children_paths
            ])

    def children_recursive(self, path):
        if not self.valid_path(path):
            raise ValueError('invalid path:', path)
        tail = self.get_tail(path)

        paths = []
        self._children_recursive(tail, paths)
        return paths

    def get_chain(self, path, depth):
        if not self.valid_path(path):
            raise ValueError('invalid path:', path)
        tail = self.get_tail(path)
        chain = [(self.get_path_from_leaf(tail), self.names[self.get_path_from_leaf(tail)])]
        for _ in range(depth):
            tail = tail.parent
            if tail is None:
                raise ValueError('invalid depth:', depth)
            chain.append((self.get_path_from_leaf(tail), self.names[self.get_path_from_leaf(tail)]))
        chain.reverse()
        return chain


router = Router.get_instance()
router.register('/lesson', 'レッスン')

router.register('/lesson/python', 'Python Lesson')


router.register('/lesson/python/basics', '基礎編')
router.register('/lesson/python/basics/variable', '変数')
router.register('/lesson/python/basics/boolean', '真偽値')
router.register('/lesson/python/basics/none', 'None')
router.register('/lesson/python/basics/string', '文字列')
router.register('/lesson/python/basics/datastructure1', 'データ構造１（リスト型）')
router.register('/lesson/python/basics/datastructure2', 'データ構造２（タプル型）')
router.register('/lesson/python/basics/datastructure3', 'データ構造３（辞書型）')
router.register('/lesson/python/basics/datastructure4', 'データ構造４（集合型）')
router.register('/lesson/python/basics/flowcontrol1', 'if 文')
router.register('/lesson/python/basics/flowcontrol2', 'while 文')
router.register('/lesson/python/basics/flowcontrol3', 'for 文')
router.register('/lesson/python/basics/comprehension', '内包表記')
router.register('/lesson/python/basics/function', '関数')
router.register('/lesson/python/basics/argument', '引数')
router.register('/lesson/python/basics/lambda', 'ラムダ式')
router.register('/lesson/python/basics/closure', 'クロージャ')
router.register('/lesson/python/basics/decorator', 'デコレータ')
router.register('/lesson/python/basics/exception', '例外処理')

router.register('/lesson/python/class', 'クラスとメソッド')
router.register('/lesson/python/class/class', 'クラス')
router.register('/lesson/python/class/methods', 'メソッド')
router.register('/lesson/python/class/inheritance', '継承')
router.register('/lesson/python/class/property', 'プロパティ')
router.register('/lesson/python/class/abstract', '抽象クラス')