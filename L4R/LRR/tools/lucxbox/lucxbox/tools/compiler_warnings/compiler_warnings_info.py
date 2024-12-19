import datetime
import sys

try:
    import git
except ImportError:
    git = False

def get_date():
    return datetime.datetime.now()

def get_call():
    return " ".join(sys.argv[:])

def get_commit():
    if git:
        repo = git.Repo(search_parent_directories=True)
        return repo.head.object.hexsha
    else:
        return "NA"

def get_branch():
    if git:
        repo = git.Repo(search_parent_directories=True)
        try:
            branch_name = repo.active_branch.name
        except TypeError:
            branch_name = "NA"
        return branch_name
    else:
        return "NA"

def get_dirty():
    if git:
        repo = git.Repo(search_parent_directories=True)
        if repo.is_dirty():
            return "true"
        else:
            return "false"
    else:
        return "NA"
