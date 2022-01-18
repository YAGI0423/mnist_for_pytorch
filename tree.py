class Node:
    def __init__(self, state, value, parent, branches):
        self.state = state
        self.value = value
        self.total_visit = 1

        self.parent = parent
        self.childrens = {}
        self.branches = branches
