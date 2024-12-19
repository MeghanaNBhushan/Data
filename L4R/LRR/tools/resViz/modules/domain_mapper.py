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
#  @brief : map symbols based on regex matching or string comparison of the symbol
#           attributes as name, namespace, object file, library to a domain
# =============================================================================

import sys
import re


class DomainMapperError(Exception):
    def __init__(self, msg):
        super().__init__()
        self._msg = msg

    def __str__(self):
        return self._msg


class SymbolMapper:
    def __init__(self, domain, category, mapper_string):
        """create 'mapper' object to configure
        mapper_string as regex for regex match if mapper_string contains a '*'
        else as a string for string (equal) comparison
        if there is a '(' the mapper expects qualified names for matching
        """
        self._domain = domain
        self._category = category
        self._raw_string = mapper_string
        self._p_string_mapper = True
        self._p_qualified = "(" in mapper_string
        if "*" in mapper_string:
            self._mapper = re.compile(re.escape(mapper_string).replace("\\*", ".*"))
            self._p_string_mapper = False
        self._match_count = 0

    def __call__(self, m_name, qualified_name_list):
        """apply the mapping object and return it itself if matching
        return the object eases tracking of ambiguous mappings
        """
        result = None
        name_list = [m_name]
        if self._p_qualified:
            name_list = qualified_name_list
        if self._p_string_mapper:
            for name in name_list:
                if name == self._raw_string:
                    result = self
                    break
        else:
            for name in name_list:
                if self._mapper.match(name):
                    result = self
                    break
        if result is not None:
            self._match_count += 1
        return result

    def get_domain(self):
        return self._domain

    def get_mapper_category(self):
        return self._category

    def get_mapper_string(self):
        return self._raw_string

    def get_match_string(self):
        if self._p_string_mapper:
            return "STR: " + self._raw_string
        else:
            return "PAT: " + re.escape(self._raw_string).replace("\\*", ".*")

    def p_used_mapper(self):
        return self._match_count > 0

    def log_format(self):
        return "domain: {0} -- {1}: {2}".format(self._domain, self._category, self._raw_string)

    def __str__(self):
        return "SymbolMapper: {0} category: {1} domain: {2}\n\tqualified: {3} regex:  {4} matches: {5}".format(
            self._raw_string,
            self._category,
            self._domain,
            int(self._p_qualified),
            int(not self._p_string_mapper),
            self._match_count,
        )


class DomainMapper:
    """some kind of container to collect domain mapping configuration"""

    def __init__(self, mapper_categories):
        self._mapper_categories = mapper_categories
        self._mapper_definitons = {}
        for mapper in self._mapper_categories:
            self._mapper_definitons[mapper] = []

    def add_mapper_defintion(self, domain, category, mapper_string):
        self._mapper_definitons[category].append(SymbolMapper(domain, category, mapper_string))

    def __call__(self, category, name, qualified_name_list):
        """apply all mapping configuration of category a return a list of successful matches"""
        result = []
        for mapper in self._mapper_definitons[category]:
            match = mapper(name, qualified_name_list)
            if match:
                result.append(match)
        return result

    def get_unused_mapper(self):
        """collect all mapping configurations which did not match so far"""
        result = {}
        for mapper_category in self._mapper_categories:
            result[mapper_category] = []
            for mapper_def in self._mapper_definitons[mapper_category]:
                if not mapper_def.p_used_mapper():
                    result[mapper_category].append(mapper_def)
        return result

    def __str__(self):
        domain_mapper_category_str = []
        for mapper_category in self._mapper_categories:
            domain_mapper_category_str.append(
                "######## {0}\n{1}".format(
                    mapper_category,
                    "\n".join([str(x) for x in self._mapper_definitons[mapper_category]]),
                )
            )
        return "{0}".format("\n".join(domain_mapper_category_str))


def testmain():
    domain_mapper = DomainMapper(["dies", "jenes"])
    domain_mapper.add_mapper_defintion("d1", "dies", "holla")
    domain_mapper.add_mapper_defintion("d2", "dies", "holla*")
    domain_mapper.add_mapper_defintion("d3", "jenes", "crammes*uuuu")
    domain_mapper.add_mapper_defintion("d4", "jenes", "happel(uuuu*)")
    print("DOMAIN_MAPPER .... \n{0}".format(domain_mapper))
    map_test_data = [
        ("dies", "haha", ["holla1"]),
        ("dies", "holla", ["holla1"]),
        ("dies", "holla1", ["holla1"]),
        ("jenes", "", ["happel(uuuutest3)"]),
        ("jenes", "", []),
        ("jenes", "crammes*uuuu", []),
    ]
    for test_tupel in map_test_data:
        map_result = domain_mapper(test_tupel[0], test_tupel[1], test_tupel[2])
        print(
            "TEST ... domain_mapper('{0}','{1}','{2}') --> {3}".format(
                test_tupel[0],
                test_tupel[1],
                test_tupel[2],
                [(x.get_domain(), x.get_match_string()) for x in map_result],
            )
        )
    try:
        domain_mapper.add_mapper_defintion("d3", "nix", "crammes*uuuu")
    except KeyError as exc:
        print("Expected Key error ... {0}".format(exc))
    sys.exit(0)


if __name__ == "__main__":
    testmain()
