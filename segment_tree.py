#!/usr/bin/env python3
"""segment_tree - Range query data structure."""
import sys, argparse, json

class SegmentTree:
    def __init__(self, data, op=min, identity=float("inf")):
        self.n = len(data)
        self.op = op
        self.identity = identity
        self.tree = [identity] * (4 * self.n)
        if self.n > 0:
            self._build(data, 1, 0, self.n - 1)
    def _build(self, data, node, start, end):
        if start == end:
            self.tree[node] = data[start]
        else:
            mid = (start + end) // 2
            self._build(data, 2*node, start, mid)
            self._build(data, 2*node+1, mid+1, end)
            self.tree[node] = self.op(self.tree[2*node], self.tree[2*node+1])
    def query(self, l, r):
        return self._query(1, 0, self.n-1, l, r)
    def _query(self, node, start, end, l, r):
        if r < start or end < l:
            return self.identity
        if l <= start and end <= r:
            return self.tree[node]
        mid = (start + end) // 2
        return self.op(self._query(2*node, start, mid, l, r), self._query(2*node+1, mid+1, end, l, r))
    def update(self, idx, val):
        self._update(1, 0, self.n-1, idx, val)
    def _update(self, node, start, end, idx, val):
        if start == end:
            self.tree[node] = val
        else:
            mid = (start + end) // 2
            if idx <= mid:
                self._update(2*node, start, mid, idx, val)
            else:
                self._update(2*node+1, mid+1, end, idx, val)
            self.tree[node] = self.op(self.tree[2*node], self.tree[2*node+1])

def main():
    p = argparse.ArgumentParser(description="Segment tree CLI")
    p.add_argument("values", nargs="+", type=float)
    p.add_argument("--query", nargs=2, type=int, metavar=("L","R"))
    p.add_argument("--op", choices=["min","max","sum"], default="min")
    args = p.parse_args()
    ops = {"min": (min, float("inf")), "max": (max, float("-inf")), "sum": (lambda a,b: a+b, 0)}
    op, ident = ops[args.op]
    st = SegmentTree(args.values, op, ident)
    result = {"size": st.n, "op": args.op}
    if args.query:
        result["query"] = {"l": args.query[0], "r": args.query[1], "result": st.query(args.query[0], args.query[1])}
    print(json.dumps(result, indent=2))

if __name__ == "__main__":
    main()
