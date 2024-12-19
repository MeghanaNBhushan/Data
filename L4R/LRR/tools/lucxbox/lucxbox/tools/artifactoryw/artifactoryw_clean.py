import sys
import os
import requests

sys.path.append(os.path.join(os.path.dirname(__file__), "../../.."))

from lucxbox.lib import lucxlog
from lucxbox.tools.artifactoryw.aql import items_in_repo_created_before, items_in_repo_downloaded_before

LOGGER = lucxlog.get_logger()


def clean(args):
    artifactory_url = args.artifactory_url
    artifactory_repository = args.artifactory_repository
    aql_domain_field = args.domain_field
    retention_period = args.retention_period
    dry_run = args.dry_run
    patterns = {'include_path_pattern': args.include_path_pattern}
    excludes = args.exclude_list
    session = _login(args.username, args.password)

    items_to_delete = fetch_items_from_artifactory(
        artifactory_url, artifactory_repository, aql_domain_field, retention_period, session, patterns)

    for item in items_to_delete:
        item_full_name = '/'.join((item['repo'], item['path'], item['name']))
        if excludes and item_full_name in excludes:
            LOGGER.info('%sSKIP   %s.', 'DRY-RUN | ' if dry_run else '', '/'.join((artifactory_url, item_full_name)))
        else:
            delete_item(artifactory_url, item['repo'], item['path'], item['name'], session, dry_run)


def fetch_items_from_artifactory(artifactory_url, repository, aql_domain_field, retention_period, session, patterns):
    artifactory_aql_query = {
        'c': items_in_repo_created_before(repository, retention_period, patterns),
        'dl': items_in_repo_downloaded_before(repository, retention_period, patterns)
    }[aql_domain_field]

    with session.post(artifactory_url + '/api/search/aql', data=artifactory_aql_query, stream=True) as response:
        response.raise_for_status()
        artifactory_items = response.json()
        return artifactory_items['results']


def delete_item(url, repo, path, name, session, dry_run=False):
    item = '/'.join((url, repo, path, name))
    if not dry_run:
        LOGGER.info('DELETE %s.', item)
        with session.delete(item, stream=True) as response:
            response.raise_for_status()
    else:
        LOGGER.info('DRY-RUN | DELETE %s.', item)


def _login(username, password):
    session = requests.Session()
    session.auth = username, password
    return session
