#!/usr/bin/env python3
"""Segment Tree - Range queries and updates with lazy propagation."""
import sys

class SegTree:
    def __init__(self, data, op=lambda a,b: a+b, identity=0):
        self.n = len(data); self.op = op; self.e = identity
        self.tree = [identity] * (4 * self.n); self.lazy = [0] * (4 * self.n)
        self._build(data, 1, 0, self.n - 1)
    def _build(self, data, node, lo, hi):
        if lo == hi: self.tree[node] = data[lo]; return
        mid = (lo + hi) // 2
        self._build(data, 2*node, lo, mid); self._build(data, 2*node+1, mid+1, hi)
        self.tree[node] = self.op(self.tree[2*node], self.tree[2*node+1])
    def _push(self, node, lo, hi):
        if self.lazy[node]:
            mid = (lo + hi) // 2
            self._apply(2*node, lo, mid, self.lazy[node])
            self._apply(2*node+1, mid+1, hi, self.lazy[node])
            self.lazy[node] = 0
    def _apply(self, node, lo, hi, val):
        self.tree[node] += val * (hi - lo + 1); self.lazy[node] += val
    def update_range(self, l, r, val): self._update(1, 0, self.n-1, l, r, val)
    def _update(self, node, lo, hi, l, r, val):
        if r < lo or hi < l: return
        if l <= lo and hi <= r: self._apply(node, lo, hi, val); return
        self._push(node, lo, hi); mid = (lo + hi) // 2
        self._update(2*node, lo, mid, l, r, val); self._update(2*node+1, mid+1, hi, l, r, val)
        self.tree[node] = self.op(self.tree[2*node], self.tree[2*node+1])
    def query(self, l, r): return self._query(1, 0, self.n-1, l, r)
    def _query(self, node, lo, hi, l, r):
        if r < lo or hi < l: return self.e
        if l <= lo and hi <= r: return self.tree[node]
        self._push(node, lo, hi); mid = (lo + hi) // 2
        return self.op(self._query(2*node, lo, mid, l, r), self._query(2*node+1, mid+1, hi, l, r))

def main():
    arr = [1, 3, 5, 7, 9, 11]
    st = SegTree(arr)
    print(f"=== Segment Tree ===\nArray: {arr}\n")
    print(f"  sum[0..5] = {st.query(0, 5)}")
    print(f"  sum[1..3] = {st.query(1, 3)}")
    st.update_range(1, 3, 10)
    print(f"  After range_add [1..3] += 10:")
    print(f"  sum[0..5] = {st.query(0, 5)}")
    print(f"  sum[1..3] = {st.query(1, 3)}")

if __name__ == "__main__":
    main()
