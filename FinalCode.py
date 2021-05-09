################################################################################
################################################################################
################################################################################
# GET_NESTING_DEPTH
################################################################################
################################################################################
################################################################################
def get_nesting_depth(s: str):
  '''
  Here's my logic. I loop through ever character in str. If it's ')', then I check if the stack is empty. If it is, I return -1. If it isn't, I pop from the stack. If the character was '(', then I push '(' onto the stack. Whenever I push or pop an element, I add or subtrack one from curr_len, which represents the current length of the stack. Whenever I push an element, I check if curr_len > max_len, in which case I say max_len = curr_len, because we've reached a new maximum size of the stack. The maximum size of the stack is the maximum nesting depth. Once I make it through str, I check if there's anything left in the stack (meaning it doesn't balance, so I should return -1). If nothing is left, then we just return max_len
  '''
  my_stack = Stack()
  curr_len = 0
  max_len = 0
  for i in range(len(str)):
    this_char = str[i]
    if this_char == '(':
      my_stack.push(this_char)
      curr_len += 1
      if curr_len > max_len:
        max_len = curr_len
    elif this_char == ')':
      if my_stack.empty():
        return -1
      else:
        my_stack.pop()
        curr_len -= 1
  if my_stack.empty():
    return max_len
  return -1              

class Stack:
    def __init__(self):
        self.data = []

    def push(self, val):
        self.data.append(val)

    def pop(self):
        assert not self.empty()
        val = self.data[-1]
        del self.data[-1]
        return val

    def peek(self):
        assert not self.empty()
        return self.data[-1]

    def empty(self):
        return self.data == []

    def __len__(self):
        return len(self.data)

    def __bool__(self):
        return not self.empty()

    def __repr__(self):
        return self.data.__repr__()

    def __str__(self):
        return self.__repr__()

################################################################################
################################################################################
################################################################################
# AVL-TREE
################################################################################
################################################################################
################################################################################
class AVLTree:
    class Node:
        def __init__(self, val, left=None, right=None):
            self.val = val
            self.left = left
            self.right = right

        def rotate_right(self):
            n = self.left
            self.val, n.val = n.val, self.val
            self.left, n.left, self.right, n.right = n.left, n.right, n, self.right

        def rotate_left(self):
            n = self.right
            self.val, n.val = n.val, self.val
            self.left, n.left, self.right, n.right = n, self.left, n.right, n.left

        def __repr__(self):
            return str(self.val)

        def __str__(self):
            return self.__repr__()

        @staticmethod
        def height(n):
            if not n:
                return 0
            else:
                return max(1+AVLTree.Node.height(n.left), 1+AVLTree.Node.height(n.right))

    def __init__(self):
        self.size = 0
        self.root = None

    @staticmethod
    def rebalance(t):
        if AVLTree.Node.height(t.left) > AVLTree.Node.height(t.right):
            if AVLTree.Node.height(t.left.left) >= AVLTree.Node.height(t.left.right):
                t.rotate_right()
            else:
                t.left.rotate_left()
                t.rotate_right()
        else:
            if AVLTree.Node.height(t.right.right) >= AVLTree.Node.height(t.right.left):
                t.rotate_left()
            else:
                t.right.rotate_right()
                t.rotate_left()

    def min(self):
        ########################################
        # BEGIN SOLUTION
        ########################################
        if not self:
          return None
        this_node = self
        while self.left:
          this_node = self.left
        return this_node.val  
        ########################################
        # END SOLUTION
        ########################################

    def max(self):
        ########################################
        # BEGIN SOLUTION
        ########################################
        if not self:
          return None
        this_node = self
        while self.right:
          this_node = self.right
        return this_node.val  
        ########################################
        # END SOLUTION
        ########################################

    def next(self,v):
        ########################################
        # BEGIN SOLUTION
        ########################################
        if not self:
          return None
        '''
        Here's the logic I'm using:
        we locate the element. If it has a right child, then the smallest element larger than it is going to be the smallest element in that subtree. If it doesn't have a right child, then the smallest element larger than this node is going to be one of its ancestors. When we start at the top, we can either move to the left path or the right. If we move to the right, then the child is bigger than the parent, but if we move to the left, the parent is bigger than the child. As we traverse down the tree, the last time we set this_el = this_el.left, the original this_el is the node which is the element with the smallest value bigger than v. So as I try to locate v, I'll keep track of target_el in the this_el.val > v part. That's O(1), done at most log n times, so O(log n). Then, if there is a right child for v, we can replace target_el with v's right child, and do the while self.left self = self.left loop. Either way, we end up returning target_el.val
        '''
        this_el = self # O(1)
        exists = False # O(1)
        target_el = None # O(1)
        while this_el and not exists: # O(log n)
          if this_el.val == v:
            exists = True
          elif this_el.val > v:
            target_el = this_el
            this_el = this_el.left
          elif this_el.val < v:
            this_el = this_el.right
        if not exists: # O(1)
          return None
        if this_el.right: # O(1)
          target_el = this_el.right
          while target_el.left: # O(log n)
            target_el = target_el.left
        if target_el:
          return target_el.val
        return None       
        # Total is O(log n)
        ########################################
        # END SOLUTION
        ########################################

    def add(self, val):
        assert(val not in self)
        def add_rec(node):
            if not node:
                return AVLTree.Node(val)
            elif val < node.val:
                node.left = add_rec(node.left)
            else:
                node.right = add_rec(node.right)
            if abs(AVLTree.Node.height(node.left) - AVLTree.Node.height(node.right)) >= 2:
                AVLTree.rebalance(node)
            return node
        self.root = add_rec(self.root)
        self.size += 1

    def __delitem__(self, val):
        assert(val in self)
        def delitem_rec(node):
            to_fix = [node]

            if val < node.val:
                node.left = delitem_rec(node.left)
            elif val > node.val:
                node.right = delitem_rec(node.right)
            else:
                if not node.left and not node.right:
                    return None
                elif node.left and not node.right:
                    return node.left
                elif node.right and not node.left:
                    return node.right
                else:
                    t = node.left
                    if not t.right:
                        node.val = t.val
                        node.left = t.left
                    else:
                        to_fix.append(t)
                        n = t
                        while n.right.right:
                            n = n.right
                            to_fix.append(n)
                        t = n.right
                        n.right = t.left
                        node.val = t.val
            while to_fix:
                n = to_fix.pop()
                if abs(AVLTree.Node.height(n.left) - AVLTree.Node.height(n.right)) >= 2:
                    AVLTree.rebalance(n)
            return node

        self.root = delitem_rec(self.root)
        self.size -= 1

    def __contains__(self, val):
        def contains_rec(node):
            if not node:
                return False
            elif val < node.val:
                return contains_rec(node.left)
            elif val > node.val:
                return contains_rec(node.right)
            else:
                return True
        return contains_rec(self.root)

    def __len__(self):
        return self.size

    def __iter__(self):
        def iter_rec(node):
            if node:
                yield from iter_rec(node.left)
                yield node.val
                yield from iter_rec(node.right)
        yield from iter_rec(self.root)

    def pprint(self, width=64):
        """Attempts to pretty-print this tree's contents."""
        height = self.height()
        nodes  = [(self.root, 0)]
        prev_level = 0
        repr_str = ''
        while nodes:
            n,level = nodes.pop(0)
            if prev_level != level:
                prev_level = level
                repr_str += '\n'
            if not n:
                if level < height-1:
                    nodes.extend([(None, level+1), (None, level+1)])
                repr_str += '{val:^{width}}'.format(val='-', width=width//2**level)
            elif n:
                if n.left or level < height-1:
                    nodes.append((n.left, level+1))
                if n.right or level < height-1:
                    nodes.append((n.right, level+1))
                repr_str += '{val:^{width}}'.format(val=n.val, width=width//2**level)
        print(repr_str)

    def height(self):
        """Returns the height of the longest branch of the tree."""
        def height_rec(t):
            if not t:
                return 0
            else:
                return max(1+height_rec(t.left), 1+height_rec(t.right))
        return height_rec(self.root)

################################################################################
################################################################################
################################################################################
# AVL-tree sort
################################################################################
################################################################################
################################################################################
def avl_sort(l):
  '''
  My plan is:
  1: O(1)-  Create an empty AVL tree
  2: O(n)- loop through l
  3: O(log n)- add ever element in l to my AVL tree
  ** Note: because step 3 occurs inside step 2, the overall Big-O so far is O(n log n)
  4: O(n) or O(n log n)- Create a list of the elements yielded by the iterator function
  5: O(1)- return the list
  Total: O(n) + O(2) + O(2 n log n) = O(n log n)
  '''
  my_tree = AVLTree()
  for i in range(len(l)):
    this_el = l[i]
    my_tree.add(this_el)
  my_iter = my_tree.__iter__()
  lst = list(my_iter)
  return lst
