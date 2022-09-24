import numpy as np
from colour import Color
MAX_OFFSET = 7

class String:
    def __init__(self, nodes=15, center=25, color=Color('green').rgb):
        self.nodes = []
        self.color = color
        self.center = center
        for i in range(nodes):
            if i == 0:
                self.nodes.append(StringNode(center, 0, fixed=True))
            elif i == nodes-1:
                self.nodes.append(StringNode(center, 15, fixed=True))
            else:
                self.nodes.append(StringNode(center, i))


    def draw(self, ctx, color):
        ctx.move_to(self.nodes[0].x, self.nodes[0].y)
        nmax = self.center
        nmin = self.center
        for node in self.nodes:
            ctx.line_to(node.x, node.y)
            if node.x > nmax:
                nmax = node.x
            if node.x < nmin:
                nmin = node.x
        br = max(abs(self.center-nmax), abs(self.center-nmin))
        r,g,b = color
        ctx.set_source_rgba(r,g,b, br/9.0)
        ctx.set_line_width(.1)
        ctx.stroke()

    def update(self, data, idx=7):
        oldnodes = self.nodes.copy()
        for i in range(len(self.nodes)):
            if i == idx:
                self.nodes[i].update(data, oldnodes, i)
            else:
                self.nodes[i].update(0, oldnodes, i)

class StringNode:
    def __init__(self, x, y,fixed=False, mass=.35, k=9, dt=0.1):
        self.x = x
        self.y = y
        self.m = mass
        self.k = k  # spring constant
        self.dt = dt
        self.v = 0
        self.a = 0
        self.fixed = fixed
        self.center = x
        self.sq_mk = np.sqrt(self.m*self.k) # sqrt(mass*spring), expensive calc that never changes


    def calc_spring_force(self, other):
        dist = other.x - self.x
        spring = self.k * (dist)
        damp = 0.3*self.sq_mk*self.v
        return spring - damp

    def update(self, data, nodes, i):
        fx = 0
        if self.fixed:
            return
        # calculate the spring force from neighboring nodes
        fx1 = self.calc_spring_force(nodes[i-1])
        fx2 = 0
        if i < len(nodes)-1:
            fx2 = self.calc_spring_force(nodes[i+1])
        fx = fx1 + fx2
        f_data = -data if self.center <17 else data
        self.a = (fx+f_data) / (self.m)
        self.v += self.a * self.dt
        self.x += self.v * self.dt
        self.x = max(self.center-MAX_OFFSET, min(self.center+MAX_OFFSET, self.x))
