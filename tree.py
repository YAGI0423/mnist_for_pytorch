class Node:
    def __init__(self, state, value, idx, parent, branches):
        self.state = state
        self.value = value
        self.total_visit = 1

        self.idx = idx
        self.parent = parent
        self.childrens = {}
        self.branches = {
            key: {
                "pior": value,
                "visit": 0,
                "total_value": 0.
            } for key, value in branches.items()
        }

    def has_child(self, branch_idx):
        return branch_idx in self.childrens

    def get_branches_keys(self):
        #return has branch keys
        return self.branches.keys()

    def get_expected_value(self, branch_idx):
        #Branch별 방문에 대한 평균 기댓값(Q)
        branch = self.branches[branch_idx]
        if branch['visit'] == 0: return 0.;
        return branch['total_value'] / branch['visit']

    def get_prior(self, branch_idx):
        #후보 수의 사전확률(P)
        return self.branches[branch_idx]['pior']

    def get_visit(self, branch_idx):
        #Branch 방문 횟수(n)
        return self.branches[branch_idx]['visit']

    def record_visit(self, branch_idx, value):
        self.total_visit += 1
        self.branches[branch_idx]['visit'] += 1
        self.branches[branch_idx]['total_value'] += value
