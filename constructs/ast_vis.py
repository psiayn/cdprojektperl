from typing import List
from collections import defaultdict
from constructs.ast import Node
import constructs.ast as ast
import pydot


def get_node_name(node: Node, cache: defaultdict):
    return f"{node.name}_{cache[node.name]}"


def get_node_label(node: Node, cache: defaultdict):
    return f"{node.name}\n{node.data}"


def _recur_draw(graph: pydot.Graph, cache: defaultdict, node: Node, rank: int = 0):
    # cache[node.name] += 1

    node_name = get_node_name(node, cache)
    # graph.add_node(pydot.Node(node_name, label=node_name, color="blue"))

    children: List[pydot.Node] = []

    for child in node.children:
        cache[child.name] += 1

        child_name = get_node_name(child, cache)
        child_label = get_node_label(child, cache)

        fillcolor = "turquoise"
        color = "red"

        if isinstance(child, ast.List):
            fillcolor = "gray"
            color = "black"

        elif isinstance(child, ast.Foreach):
            fillcolor = "coral"
            color = "blue"

        elif isinstance(child, ast.Use):
            fillcolor = "yellow1"
            color = "yellow4"

        elif isinstance(child, ast.Decleration):
            fillcolor = "lightpink"
            color = "red"

        elif isinstance(child, ast.Until):
            fillcolor = "palegreen"
            color = "blue"

        elif isinstance(child, ast.Literal):
            fillcolor = "thistle"
            color = "purple"

        elif isinstance(child, ast.BinOP):
            fillcolor = "lightyellow"
            color = "orange"

        elif isinstance(child, ast.Print):
            fillcolor = "lightblue"
            color = "navy"

        child_node = pydot.Node(
            child_name,
            label=child_label,
            group=node_name,
            fillcolor=fillcolor,
            color=color,
        )
        graph.add_node(child_node)
        children.append(child_node)

        graph.add_edge(pydot.Edge(node_name, child_name, weight=1.5))

        _recur_draw(graph, cache, child, rank + 1)

def draw_AST(ast: Node):
    graph = pydot.Dot(
        "AST",
        graph_type="digraph",
        nodesep=1.0,
        ranksep=1.0,
        splines="ortho",
        overlap=False,
    )
    cache = defaultdict(lambda: 0)

    node_name = get_node_name(ast, cache)
    graph.add_node(pydot.Node(node_name, label="START", fillcolor="white"))

    _recur_draw(graph, cache, ast)

    graph.write("ast.dot")
    graph.write("ast.png", format="png")

    return graph
