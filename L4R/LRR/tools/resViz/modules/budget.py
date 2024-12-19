# =============================================================================
#  C O P Y R I G H T
# -----------------------------------------------------------------------------
#  @copyright (c) 2021 by Robert Bosch GmbH. All rights reserved.
#
#  The reproduction, distribution and utilization of this file as
#  well as the communication of its contents to others without express
#  authorization is prohibited. Offenders will be held liable for the
#  payment of damages. All rights reserved in the event of the grant
#  of a patent, utility model or design.
# =============================================================================
#  P R O J E C T   I N F O R M A T I O N
# -----------------------------------------------------------------------------
#  Projectname            : resViz (Mapfile based memory resource analysis)
# =============================================================================
#  F I L E   I N F O R M A T I O N
# -----------------------------------------------------------------------------
#  @brief : budget 'data type' providing appropriate minimal set function to
#           handle bugdet (and also memory_consumption) values consistently
# =============================================================================

import copy
import sys


class BudgetError(Exception):
    def __init__(self, msg):
        super().__init__()
        self._msg = msg

    def __str__(self):
        return self._msg


class Budget:
    _available_resources = ["RAM", "ROM"]
    _p_resources_finalized = False

    @classmethod
    def set_available_resources(cls, resources):
        if not cls._p_resources_finalized:
            cls._available_resources = resources
            cls._p_resources_finalized = True
        else:
            raise BudgetError("not allowed to modify resource list once it is used")

    @classmethod
    def get_available_resources(cls):
        cls._p_resources_finalized = True
        return cls._available_resources

    def __init__(self):
        Budget._p_resources_finalized = True
        self._resource_budget = {}
        for resource in self._available_resources:
            self._resource_budget[resource] = 0

    def __getitem__(self, resource):
        return self._resource_budget[resource]

    def __setitem__(self, resource, value):
        self._resource_budget[resource] = value

    def keys(self):
        return self._resource_budget.keys()

    def __add__(self, other):
        result = copy.deepcopy(self)
        result += other
        return result

    def __iadd__(self, other):
        try:
            for resource in self.keys():
                self[resource] += other[resource]
        except KeyError as exc:
            raise BudgetError("unknown resource {0}".format(exc))
        return self

    def __sub__(self, other):
        result = copy.deepcopy(self)
        result -= other
        return result

    def __isub__(self, other):
        try:
            for resource in self.keys():
                self[resource] -= other[resource]
        except KeyError as exc:
            raise BudgetError("unknown resource {0}".format(exc))
        return self

    def __gt__(self, ref):
        result = []
        for resource in self._available_resources:
            if self[resource] > ref[resource]:
                result.append(resource)
        return result

    def __str__(self):
        return "BUDGET {0} :: {1}".format(id(self), self._resource_budget)


def testmain():
    Budget.set_available_resources(["HOLLA", "BOLLA", "JUHU"])
    b_1 = Budget()
    print("{0}".format(b_1))
    b_1[list(b_1.keys())[0]] = 13
    print("{0}".format(b_1))
    b_1[list(b_1.keys())[0]] += 25
    b_2 = Budget()
    b_2[list(b_2.keys())[1]] = 99
    b_2[list(b_2.keys())[1]] += 1
    print("b_1 {0}".format(b_1))
    print("b_2 {0}".format(b_2))
    b_3 = b_1 + b_2
    print("b_3 = b_1 + b_2 {0}".format(b_3))
    b_1 += b_2
    print("b_1 += b_2 {0}".format(b_1))
    print("b3 - resource {0} value {1}".format(list(b_3.keys())[0], b_3[list(b_3.keys())[0]]))
    print("{0} > {1} -> {2}".format(b_1, b_2, b_1 > b_2))
    print("{0} > {1} -> {2}".format(b_2, b_1, b_2 > b_1))
    b_1 -= b_2
    print("b_1 -= b_2 {0}".format(b_1))
    b_4 = b_3 - b_2
    print("b_4 = b_3 - b_2 {0}".format(b_4))
    sys.exit(0)


if __name__ == "__main__":
    testmain()
