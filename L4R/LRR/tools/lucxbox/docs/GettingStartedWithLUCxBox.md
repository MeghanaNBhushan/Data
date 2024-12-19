# Getting Started

-----------------------

1. [Directory Structure](#directory-structure)
2. [Using library functions](#library)
2. [Using functions from a different tool](#reuse)
3. [Creating Unit Tests](#creating-unit-tests)

-----------------------

## <a name="directory-structure">Directory Structure</a>

* `root/`
    * `docs/` -> used for documentation
    * `jenkins/` -> jenkins test config folder
    * `lucxbox` -> project folder containing the source code
        * `lib/` -> place for code shared across different scripts
            * `test/` -> Unittests for the lib
        * `tools/` -> folder for the tools
            * `template_script/` -> Example script
                * `test/` -> Unittests for the script

-----------------------

## <a name="library">Using library functions</a>

To include LUCx-specific library functions, import the respective modules in your Python script as follows:

```python
from lucxbox.lib import lucxlog, lucxargs
```

-----------------------

## <a name="reuse">Using functions from a different tool</a>

To include functions from different LUCxBox tools, simply import the respective tool, e.g.:

```python
from lucxbox.tools.tccw import tccw

tccw.tcc_wrapper.execute()
```
-----------------------

## <a name="creating-unit-tests">Creating Unit Tests</a>

You get some primary benefits from unit testing, with a majority of the value going to the first:

- Guides your design to be loosely coupled and well fleshed out. If doing test driven development, it limits the code you write to only what is needed and 
helps you to evolve that code in small steps.
- Provides fast automated regression for refactors and small changes to the code.
- Unit testing also gives you living documentation about how small pieces of the system work.

### Writing Unit Tests with LUCxBox

Unit tests have to be placed in a `test` folder in the tool's directory. The tests can then be executed with (from the root of the repo):

`python lucxbox_steps.py --test`

There is some help in the top level README how to set up a proper python environment in the "How to use it" section.
A simple unit test will look like this:

```python
""" Test for a python project """

import unittest
import lucxbox.tools.template_script.template_script as template_script  # (1)


class TestStringMethods(unittest.TestCase):

    def test_upper(self):
        string = "foo"
        result = template_script.upper(string)  # (2)
        self.assertEqual("FOO", result)


if __name__ == "__main__":
    unittest.main()
```

It is also possible to write tests using pytest:

```python
import lucxbox.tools.template_script.template_script as template_script  # (1)


def test_upper():
    string = "foo"
    result = template_script.upper(string)  # (2)
    assert "FOO" == result
```

1. Import your python script.
2. Just write test functions by using your functions.