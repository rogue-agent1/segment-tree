#!/usr/bin/env python3
"""segment_tree - Segment tree with range queries and lazy propagation."""
import sys

class SegmentTree:
    def __init__(self, data, op=lambda a,b: a+b, identity=0):
        self.n = len(data)
        self.op = op
        self.identity = identity
        self.tree = [identity] * (4 * self.n)
        self.lazy = [0] * (4 * self.n)
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
    
    def _push_down(self, node, start, end):
        if self.lazy[node] != 0:
            mid = (start + end) // 2
            self._apply(2*node, start, mid, self.lazy[node])
            self._apply(2*node+1, mid+1, end, self.lazy[node])
            self.lazy[node] = 0
    
    def _apply(self, node, start, end, val):
        self.tree[node] += val * (end - start + 1)
        self.lazy[node] += val
    
    def update_range(self, l, r, val):
        self._update(1, 0, self.n-1, l, r, val)
    
    def _update(self, node, start, end, l, r, val):
        if r < start or end < l:
            return
        if l <= start and end <= r:
            self._apply(node, start, end, val)
            return
        self._push_down(node, start, end)
        mid = (start + end) // 2
        self._update(2*node, start, mid, l, r, val)
        self._update(2*node+1, mid+1, end, l, r, val)
        self.tree[node] = self.op(self.tree[2*node], self.tree[2*node+1])
    
    def query(self, l, r):
        return self._query(1, 0, self.n-1, l, r)
    
    def _query(self, node, start, end, l, r):
        if r < start or end < l:
            return self.identity
        if l <= start and end <= r:
            return self.tree[node]
        self._push_down(node, start, end)
        mid = (start + end) // 2
        return self.op(self._query(2*node, start, mid, l, r),
                      self._query(2*node+1, mid+1, end, l, r))
    
    def update_point(self, idx, val):
        self._update_point(1, 0, self.n-1, idx, val)
    
    def _update_point(self, node, start, end, idx, val):
        if start == end:
            self.tree[node] = val
            return
        mid = (start + end) // 2
        if idx <= mid:
            self._update_point(2*node, start, mid, idx, val)
        else:
            self._update_point(2*node+1, mid+1, end, idx, val)
        self.tree[node] = self.op(self.tree[2*node], self.tree[2*node+1])

def test():
    data = [1, 3, 5, 7, 9, 11]
    st = SegmentTree(data)
    
    # Range sum
    assert st.query(0, 5) == 36
    assert st.query(1, 3) == 15
    assert st.query(0, 0) == 1
    
    # Point update
    st.update_point(2, 10)  # 5 -> 10
    assert st.query(0, 5) == 41
    assert st.query(2, 2) == 10
    
    # Range update (lazy)
    st.update_range(0, 2, 5)  # add 5 to indices 0-2
    assert st.query(0, 0) == 6   # 1+5
    assert st.query(1, 1) == 8   # 3+5
    assert st.query(2, 2) == 15  # 10+5
    assert st.query(0, 5) == 56  # 41+15
    
    # Min tree
    st_min = SegmentTree(data, op=min, identity=float('inf'))
    assert st_min.query(0, 5) == 1
    assert st_min.query(2, 4) == 5
    
    # Max tree
    st_max = SegmentTree(data, op=max, identity=float('-inf'))
    assert st_max.query(0, 5) == 11
    
    print("All tests passed!")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    else:
        print("Usage: segment_tree.py test")
