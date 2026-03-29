from segment_tree import SegmentTree
data = [1, 3, 5, 7, 9, 11]
st = SegmentTree(data)
assert st.query(0, 5) == 36
assert st.query(1, 3) == 15
assert st.query(0, 0) == 1
st.update(2, 10)
assert st.query(1, 3) == 20
assert st.query(0, 5) == 41
# Min segment tree
st2 = SegmentTree(data, op=min, identity=float("inf"))
assert st2.query(0, 5) == 1
assert st2.query(2, 4) == 5
print("segment_tree tests passed")
