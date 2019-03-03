from search_st import suffixtree

S = 'Mississippi'
st = suffixtree(S, show = False)
print('tree done')
match = st.find_positions('iss')

print(match)
