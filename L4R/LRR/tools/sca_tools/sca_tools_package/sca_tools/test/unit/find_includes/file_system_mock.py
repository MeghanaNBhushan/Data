""" Module that create mocked files on filesystem """
import os
from unittest import mock

REPO_PATH = os.path.join('path', 'to', 'repo')
DC_FW_INTERFACES_REL_PATH = os.path.join('dc_fw', 'inc', 'dc_interfaces')
DC_INTERFACES_PATH = os.path.join(REPO_PATH, DC_FW_INTERFACES_REL_PATH)
DC_FW_SRC_REL_PATH = os.path.join('dc_fw', 'src')
DC_FW_SRC_PATH = os.path.join(REPO_PATH, DC_FW_SRC_REL_PATH)
DC_FW_SIT_SRC_REL_PATH = os.path.join(DC_FW_SRC_REL_PATH, 'sit')
DC_FW_SRC_SIT_PATH = os.path.join(REPO_PATH, DC_FW_SIT_SRC_REL_PATH)

# Set up the following mock file system structure:
#
#       dc_fw/inc/dc_interfaces/
#       +-- foo/
#           +-- data/
#               +-- d.hpp
#           +-- a.hpp
#       dc_fw/src/sit/
#       +-- a.cpp
#       +-- b.hpp
#       +-- c.hpp
#       +-- c.cpp

REPO_RELATIVE_FILE_PATHS = dict()
REPO_RELATIVE_FILE_PATHS['a.hpp'] = os.path.join('dc_fw', 'inc',
                                                 'dc_interfaces', 'foo',
                                                 'a.hpp')
REPO_RELATIVE_FILE_PATHS['a.inl'] = os.path.join('dc_fw', 'inc',
                                                 'dc_interfaces', 'foo',
                                                 'a.inl')
REPO_RELATIVE_FILE_PATHS['d.hpp'] = os.path.join('dc_fw', 'inc',
                                                 'dc_interfaces', 'foo',
                                                 'data', 'd.hpp')
REPO_RELATIVE_FILE_PATHS['a.cpp'] = os.path.join('dc_fw', 'src', 'sit',
                                                 'a.cpp')
REPO_RELATIVE_FILE_PATHS['b.hpp'] = os.path.join('dc_fw', 'src', 'sit',
                                                 'b.hpp')
REPO_RELATIVE_FILE_PATHS['c.hpp'] = os.path.join('dc_fw', 'src', 'sit',
                                                 'c.hpp')
REPO_RELATIVE_FILE_PATHS['c.cpp'] = os.path.join('dc_fw', 'src', 'sit',
                                                 'c.cpp')
REPO_RELATIVE_FILE_PATHS['e.cpp'] = os.path.join('dc_fw', 'src', 'sit',
                                                 'e.cpp')
REPO_RELATIVE_FILE_PATHS['e.hpp'] = os.path.join('dc_fw', 'inc',
                                                 'dc_interfaces', 'foo',
                                                 'e.hpp')

DC_INTERFACES_WALK_MOCK = [(DC_INTERFACES_PATH, ['foo'], []),
                           (os.path.join(DC_INTERFACES_PATH, 'foo'), ['data'],
                            ['a.hpp', 'a.inl', 'e.hpp']),
                           (os.path.join(DC_INTERFACES_PATH, 'foo',
                                         'data'), [], ['d.hpp'])]

DC_FW_SRC_WALK_MOCK = [(DC_FW_SRC_PATH, ['sit'], []),
                       (os.path.join(DC_FW_SRC_PATH, 'sit'), [],
                        ['a.cpp', 'b.hpp', 'c.hpp', 'c.cpp', 'e.cpp'])]


def my_mocked_os_walk(path):
    """ Function my_moked_os_walk() """
    if 'dc_interfaces' in path:
        return_value = DC_INTERFACES_WALK_MOCK
    elif os.path.join('dc_fw', 'src') in path:
        return_value = DC_FW_SRC_WALK_MOCK
    else:
        return_value = []
    return return_value


# with the following file include structure:
#       a.cpp -> a.hpp, b.hpp, c.hpp
#       a.hpp -> d.hpp
#       c.hpp -> b.hpp
#       c.cpp -> c.hpp

DIRECT_INCLUDERS_OF = dict()
DIRECT_INCLUDERS_OF['a.hpp'] = {'a.cpp'}
DIRECT_INCLUDERS_OF['a.cpp'] = {}
DIRECT_INCLUDERS_OF['a.inl'] = {'e.cpp'}
DIRECT_INCLUDERS_OF['b.hpp'] = {'a.cpp', 'c.hpp'}
DIRECT_INCLUDERS_OF['c.hpp'] = {'a.cpp', 'c.cpp'}
DIRECT_INCLUDERS_OF['c.cpp'] = {}
DIRECT_INCLUDERS_OF['d.hpp'] = {'a.hpp'}
DIRECT_INCLUDERS_OF['e.hpp'] = {'a.inl'}
DIRECT_INCLUDERS_OF['e.cpp'] = {}

INDIRECT_CPP_INCLUDERS_OF = dict()
INDIRECT_CPP_INCLUDERS_OF['a.hpp'] = {'a.cpp'}
INDIRECT_CPP_INCLUDERS_OF['b.hpp'] = {'a.cpp', 'c.cpp'}
INDIRECT_CPP_INCLUDERS_OF['c.hpp'] = {'a.cpp', 'c.cpp'}
INDIRECT_CPP_INCLUDERS_OF['d.hpp'] = {'a.cpp'}
INDIRECT_CPP_INCLUDERS_OF['e.hpp'] = {'a.inl', 'e.cpp'}

FILE_CONTENT = dict()
FILE_CONTENT['a.cpp'] = """
#include "dc_interfaces/foo/a.hpp"

#include "sit/b.hpp"
#include "sit/c.hpp"

void S::foo()
{
    m_i = 42;
}
"""

FILE_CONTENT['a.inl'] = """
#include "dc_interfaces/foo/e.hpp"

void S::foo2()
{
    m_i = 42;
}
"""

FILE_CONTENT['a.hpp'] = """
#include "data/d.hpp"

struct S
{
    int m_i;
    void foo();
};
"""

FILE_CONTENT['b.hpp'] = """
class B {};
"""

FILE_CONTENT['c.hpp'] = """

#include "b.hpp"
"""

FILE_CONTENT['c.cpp'] = """
#include "c.hpp"

int g_x = 123;
"""

FILE_CONTENT['d.hpp'] = """
class D {};
"""

FILE_CONTENT['e.cpp'] = """
#include "dc_interfaces/foo/a.inl"

void S::foo()
{
    m_i = 42;
}
"""

FILE_CONTENT['e.hpp'] = """
class E {};
"""


def my_mocked_open(path, *_args, **_kwargs):
    """ Function my_mocked_open() """
    file_name = os.path.basename(path)
    if file_name in FILE_CONTENT:
        mocked_file_content = [
            line + '\n' for line in FILE_CONTENT[file_name].split('\n')
        ]
        magic_mock = mock.MagicMock()

        class FileMock:
            """ Class FileMock """
            @classmethod
            def readlines(cls):
                """ Method readlines """
                return mocked_file_content

            def __str__(self):
                return self.__class__.__name__

        magic_mock.__enter__ = lambda x: FileMock()
        return_value = magic_mock
    else:
        return_value = mock.MagicMock()
    return return_value
