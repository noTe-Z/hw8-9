class Node:
    def __init__(self, key):
        self.key = key
        self.left = None
        self.right = None
        self.parent = None
        self.color = "RED" 
        
class RedBlackTree:
    def __init__(self):
        self.NIL = Node(None)  
        self.NIL.color = "BLACK"
        self.root = self.NIL
        
    def height(self, node=None):
        """Calculate the height"""
        if node is None:
            node = self.root
            
        if node == self.NIL:
            return 0
            
        left_height = self.height(node.left)
        right_height = self.height(node.right)
        
        return max(left_height, right_height) + 1

    
    def left_rotate(self, x):
        """maintain red-black properties"""
        y = x.right
        x.right = y.left
        
        if y.left != self.NIL:
            y.left.parent = x
            
        y.parent = x.parent
        
        if x.parent == self.NIL:
            self.root = y
        elif x == x.parent.left:
            x.parent.left = y
        else:
            x.parent.right = y
            
        y.left = x
        x.parent = y
        
    def right_rotate(self, y):
        x = y.left
        y.left = x.right
        
        if x.right != self.NIL:
            x.right.parent = y
            
        x.parent = y.parent
        
        if y.parent == self.NIL:
            self.root = x
        elif y == y.parent.right:
            y.parent.right = x
        else:
            y.parent.left = x
            
        x.right = y
        y.parent = x
        
    def insert(self, key):
        """Insert + maintain red-black properties"""
        node = Node(key)
        node.left = self.NIL
        node.right = self.NIL
        
        y = self.NIL
        x = self.root
        
        while x != self.NIL:
            y = x
            if node.key < x.key:
                x = x.left
            else:
                x = x.right
                
        node.parent = y
        
        if y == self.NIL:
            self.root = node
        elif node.key < y.key:
            y.left = node
        else:
            y.right = node
        
        # fix
        self.insert_fixup(node)
        print(f"Current tree height after insertion: {self.height()}")
        
    def insert_fixup(self, z):
        """Fix red-black properties"""
        while z.parent.color == "RED":
            if z.parent == z.parent.parent.left:
                y = z.parent.parent.right
                
                if y.color == "RED":
                    z.parent.color = "BLACK"
                    y.color = "BLACK"
                    z.parent.parent.color = "RED"
                    z = z.parent.parent
                else:
                    if z == z.parent.right:
                        z = z.parent
                        self.left_rotate(z)
                    z.parent.color = "BLACK"
                    z.parent.parent.color = "RED"
                    self.right_rotate(z.parent.parent)
            else:
                y = z.parent.parent.left
                
                if y.color == "RED":
                    z.parent.color = "BLACK"
                    y.color = "BLACK"
                    z.parent.parent.color = "RED"
                    z = z.parent.parent
                else:
                    if z == z.parent.left:
                        z = z.parent
                        self.right_rotate(z)
                    z.parent.color = "BLACK"
                    z.parent.parent.color = "RED"
                    self.left_rotate(z.parent.parent)
                    
        self.root.color = "BLACK"
        
    def search(self, key):
        """Search for a key"""
        result = self._search_recursive(self.root, key)
        print(f"Current tree height: {self.height()}")
        return result != self.NIL
    
    def _search_recursive(self, node, key):
        if node == self.NIL or key == node.key:
            return node
        
        if key < node.key:
            return self._search_recursive(node.left, key)
        return self._search_recursive(node.right, key)
    
    def minimum(self, node):
        """Find the minimum key"""
        while node.left != self.NIL:
            node = node.left
        return node
    
    def maximum(self, node):
        """Find the maximum key"""
        while node.right != self.NIL:
            node = node.right
        return node
    
    def successor(self, x):
        """Find the next larger key"""
        if x.right != self.NIL:
            return self.minimum(x.right)
            
        y = x.parent
        while y != self.NIL and x == y.right:
            x = y
            y = y.parent
        return y
    
    def predecessor(self, x):
        """Find the next smaller key """
        if x.left != self.NIL:
            return self.maximum(x.left)
            
        y = x.parent
        while y != self.NIL and x == y.left:
            x = y
            y = y.parent
        return y
    
    def inorder_traversal(self, node, result):
        """Helper function for sorting"""
        if node != self.NIL:
            self.inorder_traversal(node.left, result)
            result.append(node.key)
            self.inorder_traversal(node.right, result)
    
    def sort(self):
        """Return sorted list of all keys"""
        result = []
        self.inorder_traversal(self.root, result)
        print(f"Current tree height: {self.height()}")
        return result
    
    def delete(self, key):
        """Delete a node with given key without RB fixup"""
        # Find the node to delete
        z = self._search_recursive(self.root, key)
        if z == self.NIL:
            print(f"Key {key} not found in tree")
            return

        # Case z has at most one child
        if z.left == self.NIL or z.right == self.NIL:
            y = z  # y will be removed
        else:
            # Case z has two children
            y = self.successor(z)  # y will be removed
        
        if y.left != self.NIL:
            x = y.left
        else:
            x = y.right


        x.parent = y.parent

        if y.parent == self.NIL:
            self.root = x
        elif y == y.parent.left:
            y.parent.left = x
        else:
            y.parent.right = x

        if y != z:
            z.key = y.key

        print(f"Deleted {key} from tree")
        print(f"Current tree height after deletion: {self.height()}")
    
def print_tree(self, node=None, level=0, prefix="Root: "):
    """Print the tree structure"""
    if node is None:
        node = self.root
        
    if node == self.NIL:
        return
        
    print("  " * level + prefix + str(node.key) + " (" + node.color + ")")
    if node.left:
        self.print_tree(node.left, level + 1, "L--- ")
    if node.right:
        self.print_tree(node.right, level + 1, "R--- ")

RedBlackTree.print_tree = print_tree

def main():

    rbtree = RedBlackTree()
    
    # Read initial numbers from file that contain space-seperated numbers
    with open('input.txt', 'r') as file:
        numbers = [int(num) for num in file.read().split()]
        print("Initial numbers from file:", numbers)
        
        # Build tree with initial numbers
        for num in numbers:
            rbtree.insert(num)
        
    # Interactive command loop
    print("\nAvailable commands:")
    print("- insert x")
    print("- search x")
    print("- sort")
    print("- min")
    print("- max")
    print("- successor x")
    print("- predecessor x")
    print("- exit (end program)")
    print("- delete x")
    
    while True:
        command = input("\nEnter command: ").strip().lower()
        
        if command == "exit":
            break
            
        elif command == "sort":
            sorted_nums = rbtree.sort()
            print("Sorted numbers:", sorted_nums)
            
        elif command.startswith("insert "):
            num = int(command.split()[1])
            rbtree.insert(num)
            print(f"Inserted {num}")
                
        elif command.startswith("search "):
            num = int(command.split()[1])
            found = rbtree.search(num)
            print(f"Number {num} {'found' if found else 'not found'}")
            
        elif command == "min":
            min_node = rbtree.minimum(rbtree.root)
            print(f"Minimum value: {min_node.key}")
            
        elif command == "max":
            max_node = rbtree.maximum(rbtree.root)
            print(f"Maximum value: {max_node.key}")
            
        elif command.startswith("successor "):
            num = int(command.split()[1])
            node = rbtree._search_recursive(rbtree.root, num)
            if node != rbtree.NIL:
                succ = rbtree.successor(node)
                if succ != rbtree.NIL:
                    print(f"Successor of {num}: {succ.key}")
                else:
                    print(f"No successor found for {num}")
            else:
                print(f"Number {num} not found")
        
        elif command.startswith("delete "):
            num = int(command.split()[1])
            rbtree.delete(num)
            print(f"Current tree structure:")
            rbtree.print_tree()
                
        elif command.startswith("predecessor "):
            num = int(command.split()[1])
            node = rbtree._search_recursive(rbtree.root, num)
            if node != rbtree.NIL:
                pred = rbtree.predecessor(node)
                if pred != rbtree.NIL:
                    print(f"Predecessor of {num}: {pred.key}")
                else:
                    print(f"No predecessor found for {num}")
            else:
                print(f"Number {num} not found")
        elif command == "print":
            rbtree.print_tree()
                
        else:
            print("Invalid command")

if __name__ == "__main__":
    main()



