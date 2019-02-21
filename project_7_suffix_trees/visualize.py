from graphviz import Digraph

dot = Digraph(comment='Suffix tree')

dot.node('A', 'King Arthur')
dot.node('B', 'Sir Bedevere the Wise')
dot.node('L', 'Sir Lancelot the Brave')

dot.edges(['AB', 'AL'])
dot.edge('B', 'L', label = 'john', constraint='false')

print(dot.source)

dot.render('test-output/round-table.gv', view=True)



