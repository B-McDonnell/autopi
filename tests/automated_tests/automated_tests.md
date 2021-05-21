# Instructions

Each subfolder under the current folder will be searched for python files of the form `*_test.py`. Each such file will be treated as containing unit tests as expected by the 'unittest' framework. These have the following form:

```
import unittest

class REPLACEWITHGROUPTESTNAME(unittest.TestCase):
    def TESTFUNCTION(self):
        ... # test code
    def MOARTEST(self):
        ... # test code

class REPLACEWITHGROUPTESTNAME2(unittest.TestCase):
    ... # more tests like above

... # more classes
```

Each function will be executed exactly as expected for 'unittest'. If you want to know how to do something test-wise, look up documentation for 'unittest'. Group tests into different `*_test.py` files as you think makes logical sense, group into classes as makes logical sense. Keep tests for particular scripts in the same folder. If you want input files/configuration files/etc., feel free to add subdirectories or other files to a folder as you wish. As long as you do not want a file to be treated as a test, don't name it like one. 

The current working directory will be the test's folder. So, to access the corresponding script:
`python3 ../../../src/scripts/SCRIPT`

No execution order for test files or tests in a file is guaranteed.

Test folders should be named with the stem of the script name. That is, 'CSM_getip.py' test folder should be named 'CSM_getip'. Non-compliance will be punished severely...
