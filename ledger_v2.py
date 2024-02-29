from hashlib import sha256


def cryptohash(x):
    return sha256(x.encode()).hexdigest()


class Node:
    def __init__(self, data, prev=None):
        self.data = data
        self.prev = prev
        if prev:
            self.hash = cryptohash(prev.data + prev.hash)
        else:
            self.hash = "000"


class Ledger:
    """A tamper resistant ledger (version 2)."""

    def __init__(self):
        self.tail = Node("genesis")

        # read in the transactions and build the ledger
        with open("transactions.txt", "r") as f:
            for line in f:
                self.tail = Node(line.strip(), self.tail)

    def verify(self):
        """Return whether the ledger verifies and print any issues."""
        node = self.tail
        verifications = []
        while node.prev:
            verifications.append(
                node.hash == cryptohash(node.prev.data + node.prev.hash)
            )
            node = node.prev
        return all(verifications)

    def print(self):
        """Print the ledger entries with hash values indicated."""
        stack = []
        node = self.tail
        while node.prev:
            stack.append(node)
            node = node.prev
        stack.append(node)
        while len(stack) > 0:
            node = stack.pop()
            if node.hash == "000":
                print(f"{node.data:<48} {node.hash[:10]}         verifies:")
            else:
                verifies = node.hash == cryptohash(node.prev.data + node.prev.hash)
                print(f"{node.data:<48} {node.hash[:10]}      {verifies}")


ledger = Ledger()
