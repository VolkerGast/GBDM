from itertools import product
from graph_tool.all import *
from copy import deepcopy


class PropositionGraph:
    def __init__(self, G=Graph(directed=True)):
        self.graph = G
        self.PropositionSet = [n for n in self.graph.vertices() if
                               self.node_type[n] == 'event']
        
        self.graph.v_type = self.graph.new_vertex_property('string')
        self.graph.vertex_properties['v_type'] = self.graph.v_type

        self.graph.v_label = self.graph.new_vertex_property('string')
        self.graph.vertex_properties['v_label'] = self.graph.v_label

        self.graph.v_act = self.graph.new_vertex_property('double')
        self.graph.vertex_properties['v_act'] = self.graph.v_act

        self.graph.v_rat = self.graph.new_vertex_property('double')
        self.graph.vertex_properties['v_rat'] = self.graph.v_rat

        self.graph.v_com = self.graph.new_vertex_property('object')
        self.graph.vertex_properties['v_com'] = self.graph.v_com

        self.graph.v_shape = self.graph.new_vertex_property('string')
        self.graph.vertex_properties['v_shape'] = self.graph.v_shape

        self.graph.e_arg = self.graph.new_edge_property('string')
        self.graph.edge_properties['e_arg'] = self.graph.e_arg

        self.graph.e_relation = self.graph.new_edge_property('string')
        self.graph.edge_properties['e_relation'] = self.graph.e_relation

    def draw_graph(self, g_name):
        for v in self.graph.vertices():
            lab = self.graph.vertex_properties['v_label'][v]
            lab = lab + '\nAct: ' + str(self.graph.vertex_properties['v_act'][v])
            if self.graph.vertex_properties['v_type'][v] == 'event':
                lab = lab + '\nRat: ' + str(self.graph.vertex_properties['v_rat'][v])
                lab = lab + '\nCom: ' + str(self.graph.vertex_properties['v_com'][v])
            self.graph.vertex_properties['v_label'][v] = lab
        graphviz_draw(self.graph,
                      size = (20, 20),
                      ratio = 'compress',
                      overlap = False,
                      splines = True,
                      vcmap = default_cm,
                      vprops = {"label": self.graph.vertex_properties['v_label'],
                                "fontsize":12,
                                "fontcolor": "black",
                                "shape": self.graph.vertex_properties['v_shape'],
                                "fillcolor": "gray", 
                                "width": 2,
                                "height": 2,
                                "fixedsize": True},
                      eprops = {"label": self.graph.edge_properties['e_arg'],
                                "fontsize": 15,
                                "labeldistance": 20,
                                "labelangle": 0,
                                "penwidth": 2},
                      output = g_name + '.png',
                      fork = True)


class InformationModel:
    def __init__(self, PG:PropositionGraph):
        self.PropositionGraph = PG
        self.EpistemicMap = EpistemicMap(PG.PropositionSet)


class EpistemicMap:
    def __init__(self, P):
        self.Map = {n: None for n in P}


class CommonGround:
    def __init__(self, PG, I):
        self.Participants = I
        self.PropositionGraph = PG


class ActivationMap:
    def __init__(self, PG:PropositionGraph):
        self.Map = {n: None for n in PG.PropositionSet}


class CommitmentMap:
    def __init__(self, PG, I):
        self.Map = {(n,d): 0.5 for n,d in product(PG, I)}


class Discourse:
    def __init__(self, CGs):
        self.CommonGrounds = CGs
        self.Participants =  set(p for CG in CGs for p in CG.Participants)
        self.Stages = [i for i,CG in enumerate(self.CommonGrounds)]
        self.InformationMatrix = [InformationState(self.Participants)
                                  for s in self.Stages]    

    def add_referent(self, label):
        CG = deepcopy(self.CommonGrounds[-1])
        PG = CG.PropositionGraph
        G = PG.graph
        v = G.add_vertex()
        G.vertex_properties['v_type'][v] = 'entity'
        G.vertex_properties['v_shape'][v] = 'circle'
        G.vertex_properties['v_label'][v] = label
        G.vertex_properties['v_act'][v] = 1
        for n in [nd for nd in G.vertices() if nd != v]:
            G.vertex_properties['v_act'][n] -= 0.1
        self.CommonGrounds.append(CG)
        return(v)

    def add_event(self, spk, label, arguments):
        CG = deepcopy(self.CommonGrounds[-1])
        PG = CG.PropositionGraph
        G = PG.graph
        v = G.add_vertex()
        G.vertex_properties['v_type'][v] = 'event'
        G.vertex_properties['v_shape'][v] = 'square'
        G.vertex_properties['v_label'][v] = label
        G.vertex_properties['v_act'][v] = 1
        G.vertex_properties['v_rat'][v] = 0
        G.vertex_properties['v_com'][v] = {spk: 1.0}
        for i,arg in enumerate(arguments):
            e = G.add_edge(v, arg)
            G.edge_properties['e_arg'][e] = 'arg: ' + str(i+1)
        self.CommonGrounds.append(CG)
        return(v)

    def add_edge(self, src, trg, arg_no):
        CG = deepcopy(self.CommonGrounds[-1])
        PG = CG.PropositionGraph
        G = PG.graph
        e = G.add_edge(src, trg)
        G.edge_properties['e_arg'][e] = arg_no
        self.CommonGrounds.append(CG)
        

class InformationState:
    def __init__(self, I:set, G=PropositionGraph()):
        self.State = [InformationModel(G) for d in I]


class InformationMatrix:
    def __init__(self, S:list):
        self.Matrix = [InformationState() for s in S]


