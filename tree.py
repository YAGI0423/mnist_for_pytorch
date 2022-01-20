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

    def get_branches_keys(self):
        return self.branches.keys()

    def expected_value(self, move):
        branch = self.branches[move]
        if branch['visit'] == 0: return 0.;
        return branch['total_value'] / branch['visit']
