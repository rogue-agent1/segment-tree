#!/usr/bin/env python3
"""segment_tree - Segment tree with lazy propagation."""
import sys
class SegTree:
    def __init__(s,data):
        s.n=len(data);s.tree=[0]*(4*s.n);s.lazy=[0]*(4*s.n);s._build(data,1,0,s.n-1)
    def _build(s,d,v,l,r):
        if l==r:s.tree[v]=d[l];return
        m=(l+r)//2;s._build(d,2*v,l,m);s._build(d,2*v+1,m+1,r);s.tree[v]=s.tree[2*v]+s.tree[2*v+1]
    def _push(s,v,l,r):
        if s.lazy[v]:
            m=(l+r)//2;s.tree[2*v]+=s.lazy[v]*(m-l+1);s.tree[2*v+1]+=s.lazy[v]*(r-m)
            s.lazy[2*v]+=s.lazy[v];s.lazy[2*v+1]+=s.lazy[v];s.lazy[v]=0
    def update(s,ql,qr,val,v=1,l=0,r=None):
        if r is None:r=s.n-1
        if ql>r or qr<l:return
        if ql<=l and r<=qr:s.tree[v]+=val*(r-l+1);s.lazy[v]+=val;return
        s._push(v,l,r);m=(l+r)//2;s.update(ql,qr,val,2*v,l,m);s.update(ql,qr,val,2*v+1,m+1,r)
        s.tree[v]=s.tree[2*v]+s.tree[2*v+1]
    def query(s,ql,qr,v=1,l=0,r=None):
        if r is None:r=s.n-1
        if ql>r or qr<l:return 0
        if ql<=l and r<=qr:return s.tree[v]
        s._push(v,l,r);m=(l+r)//2;return s.query(ql,qr,2*v,l,m)+s.query(ql,qr,2*v+1,m+1,r)
if __name__=="__main__":
    data=[1,3,5,7,9,11];st=SegTree(data);print(f"Data: {data}")
    print(f"Sum [1,3]: {st.query(1,3)}");st.update(1,3,10);print(f"After +10 on [1,3]:")
    print(f"Sum [1,3]: {st.query(1,3)}");print(f"Sum [0,5]: {st.query(0,5)}")
