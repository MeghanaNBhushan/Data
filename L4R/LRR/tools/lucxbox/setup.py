import os
from setuptools import setup, find_packages

HERE = os.path.abspath(os.path.dirname(__file__))

__pkginfo__ = {}
with open(os.path.join(HERE, "lucxbox", "__pkginfo__.py")) as f:
    # pylint: disable=W0122
    exec(f.read(), __pkginfo__)

with open(os.path.join(HERE, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

setup(
    name='lucxbox',
    version=__pkginfo__["VERSION"],
    description='LUCxBox - A collection of common used tools and scripts in XC',
    long_description=LONG_DESCRIPTION,
    long_description_content_type='text/markdown',
    url='https://sourcecode.socialcoding.bosch.com/projects/LUCX/repos/lucxbox/',
    author='',
    author_email='procclucxcore@bosch.com',
    license='Bosch Internal Open Source License v4',
    classifiers=[
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Development Status :: 4 - Beta',
        'Operating System :: OS Independent',
    ],
    keywords='',
    include_package_data=True,
    packages=find_packages(exclude=['docs', 'envs', 'jenkins']),
    python_requires='>=3.5',
    install_requires=[
        'atomicwrites>=1.3.0',
        'colorama>=0.3.9',
        'jsonschema',
        'more_itertools>=4.3',
        'pygments>=2.2.0',
        'requests>=2.19',
        'tqdm>=4.26',
        'xlsxwriter>=1.0.5',
    ],
    extras_require={
        'dev': [
            'PyInstaller>=3.4',
            'pylint>=1.8',
            'pytest>=3.8',
            'pytest-cov>=2.6',
            'pytest-mock>=1.10',
            'wheel>=0.33',
        ],
    },
    entry_points={
        'console_scripts': [
            'artifactory_cache = lucxbox.tools.artifactory_cache.artifactory_cache:main',
            'artifactoryw = lucxbox.tools.artifactoryw.artifactoryw:main',
            'batcodecheckw = lucxbox.tools.batcodecheckw.batcodecheckw:main',
            'cantataw = lucxbox.tools.cantataw.cantataw:main',
            'cashew = lucxbox.tools.cashew.cashew:main',
            'cppcheckw = lucxbox.tools.cppcheckw.cppcheckw:main',
            'compiler_warnings = lucxbox.tools.compiler_warnings.compiler_warnings:main',
            'copyright_checker = lucxbox.tools.copyright_checker.copyright_checker:main',
            'coverityw = lucxbox.tools.coverityw.coverityw:main',
            'cpp_macro_reader = lucxbox.tools.cpp_macro_reader.cpp_macro_reader:main',
            'dauerlaufw = lucxbox.tools.dauerlaufw.dauerlaufw:main',
            'flux_checker = lucxbox.tools.flux_checker.flux_checker:main',
            'git_lfs_check = lucxbox.tools.git_lfs_check.git_lfs_check:main',
            'git_reference_repo = lucxbox.tools.git_reference_repo.git_reference_repo:main',
            'mspdbsrv_wrapper = lucxbox.tools.mspdbsrv_wrapper.mspdbsrv_wrapper:main',
            'qacw = lucxbox.tools.qacw.qacw:main',
            'retryw = lucxbox.tools.retryw.retryw:main',
            'tccw = lucxbox.tools.tccw.tccw:main',
        ]
    },
)
