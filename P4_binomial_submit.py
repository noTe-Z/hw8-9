class BinomialNode:
    def __init__(self, key):
        self.key = key
        self.degree = 0
        self.parent = None
        self.child = None
        self.sibling = None

class BinomialHeap:
    def __init__(self):
        self.head = None
    
    def _merge_binomial_trees(self, b1, b2):
        """Merge two binomial trees of same degree"""
        if b1.key > b2.key:
            b1, b2 = b2, b1
        
        b2.parent = b1
        b2.sibling = b1.child
        b1.child = b2
        b1.degree += 1
        
        return b1
    
    def _union_binomial_heaps(self, h1, h2):
        """Union of two binomial heaps"""
        if not h1:
            return h2
        if not h2:
            return h1
        
        # Initialize the result heap
        if h1.degree <= h2.degree:
            result = h1
            h1 = h1.sibling
        else:
            result = h2
            h2 = h2.sibling
        
        current = result
        
        # Merge remaining nodes
        while h1 and h2:
            if h1.degree <= h2.degree:
                current.sibling = h1
                h1 = h1.sibling
            else:
                current.sibling = h2
                h2 = h2.sibling
            current = current.sibling
        
        if h1:
            current.sibling = h1
        if h2:
            current.sibling = h2
            
        # Merge trees of same degree
        prev = None
        x = result
        next_x = x.sibling
        
        while next_x:
            if (x.degree != next_x.degree) or \
               (next_x.sibling and next_x.sibling.degree == x.degree):
                prev = x
                x = next_x
            else:
                if x.key <= next_x.key:
                    x.sibling = next_x.sibling
                    self._merge_binomial_trees(x, next_x)
                else:
                    if not prev:
                        result = next_x
                    else:
                        prev.sibling = next_x
                    self._merge_binomial_trees(next_x, x)
                    x = next_x
            next_x = x.sibling
            
        return result
    
    def insert(self, key):
        """Insert a new key """
        new_node = BinomialNode(key)
        if not self.head:
            self.head = new_node
        else:
            temp = BinomialHeap()
            temp.head = new_node
            self.head = self._union_binomial_heaps(self.head, temp.head)
    
    def minimum(self):
        """Find the minimum key """
        if not self.head:
            return float('inf')
        
        min_key = self.head.key
        current = self.head.sibling
        
        while current:
            if current.key < min_key:
                min_key = current.key
            current = current.sibling
            
        return min_key
    
    def extract_min(self):
        """Extract the minimum key"""
        if not self.head:
            return float('inf')
        
        min_node = self.head
        min_prev = None
        current = self.head.sibling
        prev = self.head
        
        # Find minimum node
        while current:
            if current.key < min_node.key:
                min_node = current
                min_prev = prev
            prev = current
            current = current.sibling
        
        # Remove minimum node
        if min_prev:
            min_prev.sibling = min_node.sibling
        else:
            self.head = min_node.sibling
        
        # Reverse the order of min_node's children
        new_head = None
        child = min_node.child
        
        while child:
            next_child = child.sibling
            child.sibling = new_head
            child.parent = None
            new_head = child
            child = next_child
        
        # Create a new heap with reversed children
        if new_head:
            temp = BinomialHeap()
            temp.head = new_head
            self.head = self._union_binomial_heaps(self.head, temp.head)
        
        return min_node.key
    
    def decrease_key(self, node, new_key):
        """Decrease the key value """
        if new_key > node.key:
            return
        
        node.key = new_key
        current = node
        parent = current.parent
        
        while parent and current.key < parent.key:
            current.key, parent.key = parent.key, current.key
            current = parent
            parent = current.parent
    
    def delete(self, node):
        """Delete a node """
        self.decrease_key(node, float('-inf'))
        self.extract_min()
    
    @staticmethod
    def make_heap(keys):
        """Create a binomial heap from a list of keys"""
        heap = BinomialHeap()
        for key in keys:
            heap.insert(key)
        return heap
    
    def display(self):
        """Display the heap structure """
        def display_tree(node, level=0):
            while node:
                print("  " * level + str(node.key))
                if node.child:
                    display_tree(node.child, level + 1)
                node = node.sibling
        
        display_tree(self.head)

# Test 
if __name__ == "__main__":
    # Create heap 
    keys = [10, 1, 6, 12, 25, 18, 8, 14, 29, 11, 17, 38, 27]
    heap = BinomialHeap.make_heap(keys)
    
    print("Initial heap structure:")
    heap.display()
    
    print("\nMinimum key:", heap.minimum())
    
    min_key = heap.extract_min()
    print(f"\nExtracted minimum key: {min_key}")
    print("\nHeap structure after extracting minimum:")
    heap.display()
    
    # Insert a new key
    heap.insert(5)
    print("\nHeap structure after inserting 5:")
    heap.display()