# https://claude.ai/chat/b6ef1e65-bf7d-4a3d-a2f6-b55a85dc329e
import numpy as np
import matplotlib.pyplot as plt
import string

class HashNode:
    def __init__(self, word, count=1):
        self.word = word
        self.count = count
        self.next = None

class WordCountHash:
    def __init__(self, size):
        self.size = size
        self.table = [None] * size
        self.num_items = 0
        
    def hash_function(self, word):
        """Multiplication method hash function."""
        hash_value = 0
        multiplier = 2654435769  
        
        for char in word:
            hash_value = ((hash_value * multiplier) + ord(char)) & 0xFFFFFFFF
            
        return hash_value % self.size
    
    def insert(self, word, value=1):
        index = self.hash_function(word)
        
        current = self.table[index]
        while current is not None:
            if current.word == word:
                current.count = value
                return
            current = current.next
            
        new_node = HashNode(word, value)
        new_node.next = self.table[index]
        self.table[index] = new_node
        self.num_items += 1
    
    def delete(self, word):
        index = self.hash_function(word)
        current = self.table[index]
        prev = None
        
        while current is not None:
            if current.word == word:
                if prev is None:
                    self.table[index] = current.next
                else:
                    prev.next = current.next
                self.num_items -= 1
                return True
            prev = current
            current = current.next
        return False
    
    def increase(self, word):
        """Increase the count of a word by 1."""
        index = self.hash_function(word)
        current = self.table[index]
        
        while current is not None:
            if current.word == word:
                current.count += 1
                return True
            current = current.next
        return False
    
    def find(self, word):
        """Find the count of a word."""
        index = self.hash_function(word)
        current = self.table[index]
        
        while current is not None:
            if current.word == word:
                return current.count
            current = current.next
        return 0
    
    def list_all_keys(self):
        """Return list of all words and their counts."""
        result = []
        for i in range(self.size):
            current = self.table[i]
            while current is not None:
                result.append((current.word, current.count))
                current = current.next
        return sorted(result)  

    def get_collision_stats(self):
        """Return list of chain lengths for each bucket."""
        chain_lengths = []
        for i in range(self.size):
            length = 0
            current = self.table[i]
            while current is not None:
                length += 1
                current = current.next
            chain_lengths.append(length)
        return chain_lengths

def process_text_file(input_file, output_file, table_size=1000):
    """Process input text file and write word counts to output file."""
    # Create hash table
    word_hash = WordCountHash(table_size)
    
    try:
        #  try ISO-8859-1 encoding 
        with open(input_file, 'r', encoding='ISO-8859-1') as f:
            text = f.read().lower()
            # Remove punctuation and split into words
            translator = str.maketrans('', '', string.punctuation)
            text = text.translate(translator)
            words = [word for word in text.split() if word]
            
            # Insert each word
            for word in words:
                if word_hash.find(word) > 0:
                    word_hash.increase(word)
                else:
                    word_hash.insert(word)
    
        # Write results to output file
        with open(output_file, 'w', encoding='utf-8') as f:
            for word, count in word_hash.list_all_keys():
                f.write(f"{word}: {count}\n")
        
        return word_hash
    
    except Exception as e:
        print(f"Error processing file: {e}")
        return None

def analyze_hash_distribution(hash_table):
    """Analyze and visualize the hash distribution."""
    if hash_table is None:
        print("No hash table to analyze")
        return
        
    chain_lengths = hash_table.get_collision_stats()
    
    # Calculate statistics
    n = hash_table.num_items
    m = hash_table.size
    alpha = n / m
    actual_mean = np.mean(chain_lengths)
    actual_variance = np.var(chain_lengths)
    
    # Get longest 10% of chains
    sorted_lengths = sorted(chain_lengths, reverse=True)
    longest_10_percent = sorted_lengths[:max(1, int(0.1 * m))]
    
    print(f"\nHash Table Analysis:")
    print(f"Table size (m): {m}")
    print(f"Total items (n): {n}")
    print(f"Load factor (α = n/m): {alpha:.2f}")
    print(f"Average chain length: {actual_mean:.2f}")
    print(f"Variance in chain lengths: {actual_variance:.2f}")
    
    print("\nLongest 10% of chains:")
    for length in longest_10_percent:
        print(f"  Chain length: {length}")
    
    # Create histogram
    plt.figure(figsize=(10, 6))
    plt.hist(chain_lengths, bins=range(max(chain_lengths) + 2), align='left', rwidth=0.8)
    plt.title('Distribution of Chain Lengths')
    plt.xlabel('Chain Length')
    plt.ylabel('Number of Buckets')
    plt.show()

# Example usage
if __name__ == "__main__":
    # Process Alice in Wonderland with different table sizes
    for size in [30, 300, 1000]:
        print(f"\nAnalyzing with table size {size}:")
        hash_table = process_text_file('alice_in_wonderland.txt', f'word_counts_{size}.txt', size)
        analyze_hash_distribution(hash_table)
        
        if hash_table:
            # Demonstrate operations with a few words
            test_words = ["alice", "rabbit", "queen"]
            print("\nSample word counts:")
            for word in test_words:
                count = hash_table.find(word)
                print(f"'{word}': {count}")
