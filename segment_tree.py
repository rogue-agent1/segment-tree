#!/usr/bin/env python3
"""Segment tree for range queries. Zero dependencies."""

class SegmentTree:
    def __init__(self, data, op=None, identity=0):
        self.n = len(data)
        self.op = op or (lambda a, b: a + b)
        self.identity = identity
        self.tree = [identity] * (4 * self.n)
        if self.n > 0:
            self._build(data, 1, 0, self.n - 1)

    def _build(self, data, node, start, end):
        if start == end:
            self.tree[node] = data[start]
            return
        mid = (start + end) // 2
        self._build(data, 2*node, start, mid)
        self._build(data, 2*node+1, mid+1, end)
        self.tree[node] = self.op(self.tree[2*node], self.tree[2*node+1])

    def update(self, idx, value, node=1, start=0, end=None):
        if end is None: end = self.n - 1
        if start == end:
            self.tree[node] = value
            return
        mid = (start + end) // 2
        if idx <= mid: self.update(idx, value, 2*node, start, mid)
        else: self.update(idx, value, 2*node+1, mid+1, end)
        self.tree[node] = self.op(self.tree[2*node], self.tree[2*node+1])

    def query(self, l, r, node=1, start=0, end=None):
        if end is None: end = self.n - 1
        if r < start or end < l: return self.identity
        if l <= start and end <= r: return self.tree[node]
        mid = (start + end) // 2
        return self.op(self.query(l, r, 2*node, start, mid),
                       self.query(l, r, 2*node+1, mid+1, end))

if __name__ == "__main__":
    st = SegmentTree([1, 3, 5, 7, 9, 11])
    print(f"Sum [1,3] = {st.query(1,3)}")
    st.update(2, 10)
    print(f"Sum [1,3] after update = {st.query(1,3)}")
