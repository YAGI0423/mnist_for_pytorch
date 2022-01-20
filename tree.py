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

    def get_expected_value(self, branch_idx):
        #Branch별 방문에 대한 평균 기댓값
        branch = self.branches[branch_idx]
        if branch['visit'] == 0: return 0.;
        return branch['total_value'] / branch['visit']

    def get_prior(self, branch_idx):
        #후보 수의 사전확률
        return self.branches[branch_idx]['pior']

    def get_visit(self, branch_idx):
        #Branch 방문 횟수
        if branch_idx in self.branches:
            return self.branches[branch_idx]['visit']
        return 0
