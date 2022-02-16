from queue import PriorityQueue


class PrioritizedItem:

    def __init__(self, cost: float, item: any):
        self.cost = cost
        self.item = item

    def __eq__(self, other):
        return self.cost == other.cost

    def __lt__(self, other):
        return self.cost < other.cost


class KLPriorityQueue:

    def __init__(self):
        self.q = PriorityQueue()

    def empty(self):
        return self.q.empty()

    def get(self) -> any:
        p_item = self.q.get()
        return p_item.item

    def put(self, cost: float, item: any):
        p_item = PrioritizedItem(cost, item)
        self.q.put(p_item)

