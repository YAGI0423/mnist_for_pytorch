class Node:
    def __init__(self, state, value, parent, branches):
        self.state = state
        self.value = value
        self.total_visit = 1

        self.parent = parent
        self.childrens = {}
        self.branches = {
            key: {
                "pior": value,
                "visit": 0,
                "total_value": 0.
            } for key, value in branches.items()
        }
