
class Pipelines:
    def __init__(self, pipelines, pre_nodes, post_nodes, post_success_nodes, post_fail_nodes):
        self.pipelines = pipelines
        self.pre_nodes = pre_nodes
        self.post_nodes = post_nodes
        self.post_success_nodes = post_success_nodes
        self.post_fail_nodes = post_fail_nodes


class Pipeline:
    def __init__(self, nodes):
        self.nodes = nodes


class Node:
    def __init__(self, execution_order, stages, post_stages, post_success_stages, post_fail_stages):
        self.execution_order = execution_order
        self.stages = stages
        self.post_stages = post_stages
        self.post_success_stages = post_success_stages
        self.post_fail_stages = post_fail_stages


class Stage:
    def __init__(self, name, execution_order, steps, post_steps, post_success_steps, post_fail_steps):
        self.name = name
        self.execution_order = execution_order
        self.steps = steps
        self.post_steps = post_steps
        self.post_success_steps = post_success_steps
        self.post_fail_steps = post_fail_steps
