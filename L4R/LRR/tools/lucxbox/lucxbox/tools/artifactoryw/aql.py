"""get_artifactory_aql function returns AQL string which uses to find necessary items in Artifactory:

   items.find({
               "repo":{"$eq":"artifactory-repository-name"},
               "created":{"$before":"5d"}
   }).include("repo","name","path","created")

   AQL - Artifactory Query Language. Its syntax offers a simple way to formulate complex queries that specify any number
   of search criteria, filters, sorting options, and output parameters. AQL is exposed as a RESTful API which uses data
   streaming to provide output data resulting in extremely fast response times and low memory consumption.
   More details are available on https://www.jfrog.com/confluence/display/RTF/Artifactory+Query+Language
"""

from collections import OrderedDict
import json


def items_in_repo_created_before(repository, period, patterns=None, fields=None):
    criteria = OrderedDict()
    criteria['repo'] = {'$eq': repository}
    criteria['created'] = {'$before': period}
    if patterns and 'include_path_pattern' in patterns and patterns['include_path_pattern']:
        criteria['path'] = {'$match': patterns['include_path_pattern']}
    if fields:
        fields = list(OrderedDict.fromkeys(list(fields) + ['created']))
        quoted_fields = ['"{}"'.format(f) for f in fields]
        return 'items.find({}).include({})'.format(json.dumps(criteria), ','.join(quoted_fields))
    else:
        return 'items.find({})'.format(json.dumps(criteria))


def items_in_repo_downloaded_before(repository, period, patterns=None, fields=None):
    criteria = OrderedDict()
    criteria['repo'] = {'$eq': repository}
    criteria['stat.downloaded'] = {'$before': period}
    if patterns and 'include_path_pattern' in patterns and patterns['include_path_pattern']:
        criteria['path'] = {'$match': patterns['include_path_pattern']}
    if fields:
        fields = list(OrderedDict.fromkeys(list(fields) + ['stat.downloaded']))
        quoted_fields = ['"{}"'.format(f) for f in fields]
        return 'items.find({}).include({})'.format(json.dumps(criteria), ','.join(quoted_fields))
    else:
        return 'items.find({})'.format(json.dumps(criteria))
