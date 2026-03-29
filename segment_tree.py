#!/usr/bin/env python3
"""segment_tree - Segment tree for range queries and updates."""
import sys

class SegmentTree:
    def __init__(self, arr, op=min, default=float('inf')):
        self.n = len(arr)
        self.op = op
        self.default = default
        self.tree = [default] * (4 * self.n)
        self._build(arr, 1, 0, self.n - 1)
    def _build(self, arr, node, start, end):
        if start == end:
            self.tree[node] = arr[start]
        else:
            mid = (start + end) // 2
            self._build(arr, 2 * node, start, mid)
            self._build(arr, 2 * node + 1, mid + 1, end)
            self.tree[node] = self.op(self.tree[2 * node], self.tree[2 * node + 1])
    def query(self, l, r):
        return self._query(1, 0, self.n - 1, l, r)
    def _query(self, node, start, end, l, r):
        if r < start or end < l:
            return self.default
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        return self.op(self._query(2 * node, start, mid, l, r),
                       self._query(2 * node + 1, mid + 1, end, l, r))
    def update(self, idx, val):
        self._update(1, 0, self.n - 1, idx, val)
    def _update(self, node, start, end, idx, val):
        if start == end:
            self.tree[node] = val
        else:
            mid = (start + end) // 2
            if idx <= mid:
                self._update(2 * node, start, mid, idx, val)
            else:
                self._update(2 * node + 1, mid + 1, end, idx, val)
            self.tree[node] = self.op(self.tree[2 * node], self.tree[2 * node + 1])

def test():
    arr = [2, 5, 1, 4, 9, 3]
    st = SegmentTree(arr)
    assert st.query(0, 5) == 1
    assert st.query(0, 2) == 1
    assert st.query(3, 5) == 3
    st.update(2, 10)
    assert st.query(0, 2) == 2
    st_sum = SegmentTree(arr, op=lambda a, b: a + b, default=0)
    assert st_sum.query(0, 5) == 24
    assert st_sum.query(1, 3) == 10
    print("OK: segment_tree")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    else:
        print("Usage: segment_tree.py test")
