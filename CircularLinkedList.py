class Node:
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node


class CircularLinkedList:
    def __init__(self):
        self.head = Node()

    def addnode(self, data):
        new_node = Node(data)
        if self.head.data is None:
            self.head = new_node
            self.head.next_node = self.head
        carrier = self.head
        while carrier.next_node is not self.head:
            carrier = carrier.next_node
        carrier.next_node = new_node
        new_node.next_node = self.head
        print("******************Node ADDED*******************")

    def addhead(self,data):
        if self.head.data is None:
            print("Create a LinkedList First")
        else:
            carrier = self.head
            new_node = Node(data)
            while carrier.next_node is not self.head:
                carrier = carrier.next_node
            carrier.next_node = new_node
            new_node.next_node = self.head
            self.head = new_node
            print("**************HEAD ADDED*****************")

    def delete_head(self):
        if self.head.data is None:
            print("Create a LinkedList First")
        else:
            carrier = self.head
            while carrier.next_node is not self.head:
                carrier = carrier.next_node
            self.head = self.head.next_node
            carrier.next_node = self.head
            print("****************HEAD DELETED****************")

    def add_target_node(self, target, data):
        if self.head.data is None:
            print("Create a LinkedList First")
        else:
            index=1
            new_node = Node(data)
            prev = Node()
            carrier = self.head
            while index != target:
                prev = carrier
                carrier = carrier.next_node
                index = index + 1
            prev.next_node = new_node
            new_node.next_node = carrier

    def del_target_node(self,target):
        if self.head.data is None:
            print("Create a LinkedList First")
        else:
            index=1
            prev = Node()
            carrier = self.head
            while index != target:
                prev = carrier
                carrier = carrier.next_node
                index = index + 1
            prev.next_node = carrier.next_node

    def show_list(self):
        if self.head.data is None:
            print("Create a LinkedList First")
        else:
            node_id = 1
            carrier = self.head
            while carrier.next_node is not self.head:
                print(carrier.data)
                carrier = carrier.next_node
                node_id += 1
            print(carrier.data)


if __name__ == '__main__':
    noder = CircularLinkedList()
    noder.addnode(1)
    noder.addnode(2)
    noder.addnode(3)
    noder.addnode(4)
    noder.addnode(5)
    noder.addnode(6)
    noder.addnode(7)
    noder.del_target_node(4)
    noder.show_list()
