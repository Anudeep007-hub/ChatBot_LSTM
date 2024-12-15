class TrieNode:
    def __init__(self):
        self.children = {}
        self.is_end_of_word = False

class Trie:
    def __init__(self):
        self.root = TrieNode()

    def insert(self, word):
        node = self.root
        for char in word:
            if char not in node.children:
                node.children[char] = TrieNode()
            node = node.children[char]
        node.is_end_of_word = True

    def search_prefix(self, prefix):
        node = self.root
        for char in prefix:
            if char not in node.children:
                return []
            node = node.children[char]
        return self._collect_words_from_node(node, prefix)

    def _collect_words_from_node(self, node, prefix):
        suggestions = []
        if node.is_end_of_word:
            suggestions.append(prefix)
        for char, child_node in node.children.items():
            suggestions.extend(self._collect_words_from_node(child_node, prefix + char))
        return suggestions
