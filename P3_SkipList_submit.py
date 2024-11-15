import random

class Node:
    def __init__(self, key, level):
        self.key = key
        self.forward = [None] * (level + 1)

class SkipList:
    def __init__(self, max_level=4, p=0.5):
        self.max_level = max_level
        self.p = p
        self.header = Node(float('-inf'), max_level)
        self.level = 0

    def random_level(self):
        level = 0
        # random level p=0.5
        while random.random() < self.p and level < self.max_level:
            level += 1
        return level

    def insert(self, key):
        update = [None] * (self.max_level + 1)
        current = self.header

        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        new_level = self.random_level()

        if new_level > self.level:
            for i in range(self.level + 1, new_level + 1):
                update[i] = self.header
            self.level = new_level

        # Create new node
        new_node = Node(key, new_level)

        # Insert node by updating references
        for i in range(new_level + 1):
            new_node.forward[i] = update[i].forward[i]
            update[i].forward[i] = new_node

        print(f"Inserted {key}")

    def delete(self, key):
        update = [None] * (self.max_level + 1)
        current = self.header

        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]
            update[i] = current

        current = current.forward[0]

        if current and current.key == key:
            for i in range(self.level + 1):
                if update[i].forward[i] != current:
                    break
                update[i].forward[i] = current.forward[i]

            while self.level > 0 and self.header.forward[self.level] is None:
                self.level -= 1
            print(f"Deleted {key}")
        else:
            print(f"Key {key} not found")

    def search(self, key):
        current = self.header

        for i in range(self.level, -1, -1):
            while current.forward[i] and current.forward[i].key < key:
                current = current.forward[i]

        current = current.forward[0]

        if current and current.key == key:
            print(f"Found key {key}")
            return True
        print(f"Key {key} not found")
        return False


    def display_detailed(self):
        print("\nDetailed Skip List Structure:")
        for level in range(self.level, -1, -1):
            print(f"Level {level}: ", end="")
            node = self.header
            while node:
                print(f"({node.key})->", end="")
                node = node.forward[level]
            print("None")
# Testing

def test_detailed_structure():
    sl = SkipList()
    test_values = [3, 6, 7, 9, 12, 15, 18, 21]
    print("\nTesting detailed structure visualization:")
    
    for value in test_values:
        sl.insert(value)
        print(f"\nAfter inserting {value}:")
        sl.display_detailed()
    
    for value in [7, 15, 9]:
        sl.delete(value)
        print(f"\nAfter deleting {value}:")
        sl.display_detailed()

# def test_search_functionality():
#     # Set seed for reproducible random levels
#     random.seed(42)
    
#     # Create skip list and insert values
#     sl = SkipList(max_level=3)
#     test_values = [3, 6, 7, 9, 12, 15, 18, 21]
    
#     print("\nBuilding skip list structure:")
#     for value in test_values:
#         sl.insert(value)
    
#     # Display initial structure
#     print("\nInitial skip list structure:")
#     sl.display_detailed()
    
#     # Test search operations
#     print("\nSearch operations:")
#     print("-" * 20)
    
#     # Test existing values
#     sl.search(7)   # Should find
#     sl.search(15)  # Should find
#     sl.search(21)  # Should find
    
#     # Test non-existing values
#     sl.search(4)   # Should not find
#     sl.search(10)  # Should not find
#     sl.search(25)  # Should not find

if __name__ == "__main__":

    test_detailed_structure()
    # test_search_functionality()