FROM rb-dtr.de.bosch.com/library/python:3.7.0a3-stretch

## Install dependencies:
# git-lfs for git_lfs_check
RUN curl -o /tmp/git-lfs_2.5.2_amd64.deb \
        https://rb-artifactory.bosch.com/artifactory/list/tcc-deb-local/tools/git-lfs/git-lfs_2.5.2_amd64.deb \
    && dpkg -i /tmp/git-lfs_2.5.2_amd64.deb \
    && rm -f /tmp/git-lfs_2.5.2_amd64.deb

## Install bitbucket_tools package
COPY ./ /tmp/lucxbox/

RUN python3 -m pip install -r /tmp/lucxbox/requirements.txt --proxy=rb-proxy-de.bosch.com:8080
RUN cd /tmp/lucxbox \
    && python3 setup.py install \
    && rm -rf /tmp/lucxbox
