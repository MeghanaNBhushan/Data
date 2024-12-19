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
#  @brief : parse domain configuration and provide domain mapper as part of it
# =============================================================================

import sys
from budget import Budget


class DomainConfigError(Exception):
    def __init__(self, msg):
        super().__init__()
        self._msg = msg

    def __str__(self):
        return self._msg


class DomainConfig:
    """straight forward internal representation of the
    resViz application specific domain configuration
    """

    def __init__(self, name):
        self._name = name
        self._budget = Budget()
        self._mapper_config = {}
        self._p_inialized = False

    def parse_config(self, config_data, mapper_list):
        if self._p_inialized:
            raise DomainConfigError("domain {0} already configured")
        try:
            for res in Budget.get_available_resources():
                self._budget[res] = config_data[res]
        except KeyError as key_exc:
            raise DomainConfigError("missing domain budget configuration item {0}".format(key_exc))
        if "name" in config_data:
            self._name = config_data["name"]
        for mapper_name in mapper_list:
            if mapper_name in config_data:
                self._mapper_config[mapper_name] = config_data[mapper_name].copy()
            else:
                self._mapper_config[mapper_name] = []
        self._p_inialized = True

    def get_mapper_config(self, category):
        return self._mapper_config[category]

    def __str__(self):
        'Domain "{0}"\nBudget\n'.format(self._name)
        budget_data = []
        for res in Budget.get_available_resources():
            budget_data.append("\t{0}: {1}\n".format(res, self._budget[res]))
        mapper_data = []
        for mapping in self._mapper_config.keys():
            if self._mapper_config[mapping]:
                mapper_data.append(
                    "\t{0}:\n\t\t{1}\n".format(mapping, "\n\t\t".join(self._mapper_config[mapping]))
                )
        return 'Domain "{0}"\nBudget\n{1}\nDomainMapping:\n{2}'.format(
            self._name, "".join(budget_data), "".join(mapper_data)
        )

    def get_name(self):
        return self._name

    def get_budget(self):
        return self._budget

    def get_domain_mapping(self):
        return self._mapper_config


def testmain():
    Budget.set_available_resources(["ram", "rom"])
    domain_1 = DomainConfig("malsehn")
    dcf = {
        "name": "holla",
        "ram": 13,
        "rom": 39,
        "nase": ["crammens", "dingens"],
        "vase": ["auch", "das"],
        "iiii": ["uuuu"],
    }
    domain_1.parse_config(dcf, ["nase", "vase", "ddd"])
    print("{0}".format(domain_1))
    domain_2 = DomainConfig("juüü")
    domain_2.parse_config(dcf, [])
    print("{0}".format(domain_2))
    try:
        domain_2.parse_config(dcf, [])
    except DomainConfigError:
        print("expected Exception ...")
    sys.exit(0)


if __name__ == "__main__":
    testmain()
