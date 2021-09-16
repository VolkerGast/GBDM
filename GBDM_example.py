from GBDM import *
from graph_tool import draw

# initialize empty Proposition Graph
PG = PropositionGraph()

# define participants
I = {1,2}

# initialize empty Common Ground
CG = CommonGround(PG, I)

# initialize Discourse
D = Discourse([CG])

# add referent 'princess'
p = D.add_referent('PRINCESS')

# add referent 'forest'
f = D.add_referent('FOREST')

# add event 'princess went into forest'
D.add_event('Narr', 'WENT_INTO', [p,f])

# draw graph
D.CommonGrounds[0].PropositionGraph.draw_graph('CG0')
D.CommonGrounds[1].PropositionGraph.draw_graph('CG1')
D.CommonGrounds[2].PropositionGraph.draw_graph('CG2')
D.CommonGrounds[3].PropositionGraph.draw_graph('CG3')
