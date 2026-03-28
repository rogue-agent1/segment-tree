#!/usr/bin/env python3
"""Segment tree for range sum/min/max queries with point updates."""
import sys

class SegTree:
    def __init__(self, data, op='sum'):
        self.n = len(data)
        self.op = op
        self.fn = {'sum': lambda a,b: a+b, 'min': min, 'max': max}[op]
        self.identity = {'sum': 0, 'min': float('inf'), 'max': float('-inf')}[op]
        self.tree = [self.identity] * (2 * self.n)
        for i in range(self.n): self.tree[self.n + i] = data[i]
        for i in range(self.n - 1, 0, -1): self.tree[i] = self.fn(self.tree[2*i], self.tree[2*i+1])
    def update(self, i, val):
        i += self.n; self.tree[i] = val
        while i > 1: i //= 2; self.tree[i] = self.fn(self.tree[2*i], self.tree[2*i+1])
    def query(self, l, r):
        res = self.identity; l += self.n; r += self.n + 1
        while l < r:
            if l & 1: res = self.fn(res, self.tree[l]); l += 1
            if r & 1: r -= 1; res = self.fn(res, self.tree[r])
            l //= 2; r //= 2
        return res

if __name__ == '__main__':
    if '--demo' in sys.argv:
        data = [1, 3, 5, 7, 9, 11]
        for op in ('sum', 'min', 'max'):
            st = SegTree(data, op)
            print(f"{op}([1..5]={data}): range(1,4)={st.query(1,4)}")
    else:
        data = list(map(int, sys.argv[1].split(','))) if len(sys.argv) > 1 else [1,2,3,4,5]
        op = sys.argv[2] if len(sys.argv) > 2 else 'sum'
        st = SegTree(data, op)
        print(f"SegTree ({op}) data={data}. Commands: query <l> <r>, update <i> <val>, quit")
        while True:
            try: line = input('> ').split()
            except EOFError: break
            if not line: continue
            if line[0] == 'quit': break
            elif line[0] == 'query': print(st.query(int(line[1]), int(line[2])))
            elif line[0] == 'update': st.update(int(line[1]), int(line[2])); print("OK")
