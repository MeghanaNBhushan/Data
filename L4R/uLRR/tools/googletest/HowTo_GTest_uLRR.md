# Integration of GoogleTest in uLRR

This section gives an overview how unit tests may be integrated into our project. The usage of GoogleTest framework is described in the [GoogleTest User´s Guide](https://google.github.io/googletest/).

## Folder Structure
In this approach it is assumed that the sources of the unit under test are structured in the following way:
```bash
.
`-- compname
    |-- doc
    |-- inc
    |   `-- examplefunc.hpp
    |-- src
    |   `-- examplefunc.cpp
    `-- test
        `-- test_examplefunc.cpp
```
> **NOTE**: This structure applies for application components/nodes under `/software/application/`


## Creation of Unit Tests
In your component/node, create for every source file (*.cpp) one test file with the prefix `test_` and the name of the source file (`test_`_\<sourcename\>_`.
cpp`) in the `test` folder of the component/node. 

As a starting point you may check the example component with the corresponding simple GoogleTest `software\application\compname\test\test_examplefunc.cpp`.

Basic concepts on GoogleTest are described in the [Googletest Primer](https://google.github.io/googletest/primer.html). And how good unit tests are written is described in [Unit Tests, How to Write Testable Code and Why it Matters](https://www.toptal.com/qa/how-to-write-testable-code-and-why-it-matters).


## Generation of Build Environment

* Add your unit test source files into root `CMakeLists.txt`
```cmake
add_executable(ad_radar_sensor_unit_tests  
	# Other already existing source files
	software/application/yourcompname/test/test_sourcename.cpp
)

target_include_directories(ad_radar_sensor_unit_tests
	PRIVATE
  		  # Other already existing header files
          software/application/yourcompname/inc/
)
```
> **NOTE**: In the current approach we just generate one executable. Later we will extend the script and possibilities. 

* Create build folder in project root folder
```bash
$ mkdir build
```

* Generate CMake environment for your building environment in previous created folder.

### Windows
```bash
$ cd build/
$ cmake ../ -G "MinGW Makefiles"
-- The C compiler identification is GNU 8.1.0
-- The CXX compiler identification is GNU 8.1.0
-- Check for working C compiler: C:/TCC/Tools/mingw64/8.1.0_WIN64/bin/gcc.exe
-- Check for working C compiler: C:/TCC/Tools/mingw64/8.1.0_WIN64/bin/gcc.exe - works
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Detecting C compile features
-- Detecting C compile features - done
-- Check for working CXX compiler: C:/TCC/Tools/mingw64/8.1.0_WIN64/bin/g++.exe
-- Check for working CXX compiler: C:/TCC/Tools/mingw64/8.1.0_WIN64/bin/g++.exe - works
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Found Python: C:/TCC/Tools/python3/3.7.4-29_WIN64/python.exe (found version "3.7.4") found components: Interpreter
-- Configuring done
-- Generating done
-- Build files have been written to: C:/ATR/uLRR/ad_radar_sensor/build
```

### OSD
```bash
$ cd build/
$ cmake ../
-- The C compiler identification is GNU 9.4.0
-- The CXX compiler identification is GNU 9.4.0
-- Check for working C compiler: /usr/bin/cc
-- Check for working C compiler: /usr/bin/cc -- works
-- Detecting C compiler ABI info
-- Detecting C compiler ABI info - done
-- Detecting C compile features
-- Detecting C compile features - done
-- Check for working CXX compiler: /usr/bin/c++
-- Check for working CXX compiler: /usr/bin/c++ -- works
-- Detecting CXX compiler ABI info
-- Detecting CXX compiler ABI info - done
-- Detecting CXX compile features
-- Detecting CXX compile features - done
-- Found Python: /usr/bin/python3.8 (found version "3.8.10") found components: Interpreter 
-- Looking for pthread.h
-- Looking for pthread.h - found
-- Performing Test CMAKE_HAVE_LIBC_PTHREAD
-- Performing Test CMAKE_HAVE_LIBC_PTHREAD - Failed
-- Looking for pthread_create in pthreads
-- Looking for pthread_create in pthreads - not found
-- Looking for pthread_create in pthread
-- Looking for pthread_create in pthread - found
-- Found Threads: TRUE  
-- Configuring done
-- Generating done
-- Build files have been written to: /media/bad2lr/big_hdd/uLRR/ad_radar_sensor/build
```


## Compilation and Execution

* Compile your unit tests

### Windows

```bash
$ make
Scanning dependencies of target gtest
[  9%] Building CXX object software/googletest/googletest/CMakeFiles/gtest.dir/src/gtest-all.cc.obj
[ 18%] Linking CXX static library ..\..\..\lib\libgtest.a
[ 18%] Built target gtest
Scanning dependencies of target gtest_main
[ 27%] Building CXX object software/googletest/googletest/CMakeFiles/gtest_main.dir/src/gtest_main.cc.obj
[ 36%] Linking CXX static library ..\..\..\lib\libgtest_main.a
[ 36%] Built target gtest_main
Scanning dependencies of target ad_radar_sensor_unit_tests
[ 45%] Building CXX object CMakeFiles/ad_radar_sensor_unit_tests.dir/software/application/compname/src/examplefunc.cpp.obj
[ 54%] Building CXX object CMakeFiles/ad_radar_sensor_unit_tests.dir/software/application/compname/test/test_examplefunc.cpp.obj
[ 63%] Linking CXX executable ad_radar_sensor_unit_tests.exe
[ 63%] Built target ad_radar_sensor_unit_tests
Scanning dependencies of target gmock
[ 72%] Building CXX object software/googletest/googlemock/CMakeFiles/gmock.dir/src/gmock-all.cc.obj
[ 81%] Linking CXX static library ..\..\..\lib\libgmock.a
[ 81%] Built target gmock
Scanning dependencies of target gmock_main
[ 90%] Building CXX object software/googletest/googlemock/CMakeFiles/gmock_main.dir/src/gmock_main.cc.obj
[100%] Linking CXX static library ..\..\..\lib\libgmock_main.a
[100%] Built target gmock_main
```

### OSD
```bash
$ make
Scanning dependencies of target gtest
[  9%] Building CXX object software/googletest/googletest/CMakeFiles/gtest.dir/src/gtest-all.cc.o
[ 18%] Linking CXX static library ../../../lib/libgtest.a
[ 18%] Built target gtest
Scanning dependencies of target gtest_main
[ 27%] Building CXX object software/googletest/googletest/CMakeFiles/gtest_main.dir/src/gtest_main.cc.o
[ 36%] Linking CXX static library ../../../lib/libgtest_main.a
[ 36%] Built target gtest_main
Scanning dependencies of target ad_radar_sensor_unit_tests
[ 45%] Building CXX object CMakeFiles/ad_radar_sensor_unit_tests.dir/software/application/compname/src/examplefunc.cpp.o
[ 54%] Building CXX object CMakeFiles/ad_radar_sensor_unit_tests.dir/software/application/compname/test/test_examplefunc.cpp.o
[ 63%] Linking CXX executable ad_radar_sensor_unit_tests
[ 63%] Built target ad_radar_sensor_unit_tests
Scanning dependencies of target gmock
[ 72%] Building CXX object software/googletest/googlemock/CMakeFiles/gmock.dir/src/gmock-all.cc.o
[ 81%] Linking CXX static library ../../../lib/libgmock.a
[ 81%] Built target gmock
Scanning dependencies of target gmock_main
[ 90%] Building CXX object software/googletest/googlemock/CMakeFiles/gmock_main.dir/src/gmock_main.cc.o
[100%] Linking CXX static library ../../../lib/libgmock_main.a
[100%] Built target gmock_main
```

* Execute your unit tests

### Windows

```bash
$ ./ad_radar_sensor_unit_tests.exe 
Running main() from C:\ATR\uLRR\ad_radar_sensor\software\googletest\googletest\src\gtest_main.cc
[==========] Running 1 test from 1 test suite.
[----------] lobal test environment set-up.
[----------] 1 test from TestSuiteSomeExampleClass
[ RUN      ] TestSuiteSomeExampleClass.TestInputValues
[       OK ] TestSuiteSomeExampleClass.TestInputValues (0 ms)
[----------] 1 test from TestSuiteSomeExampleClass (10 ms total)

[----------] Global test environment tear-down
[==========] 1 test from 1 test suite ran. (33 ms total)
[  PASSED  ] 1 test.
```

### OSD

```bash
$ ./ad_radar_sensor_unit_tests 
Running main() from /media/bad2lr/big_hdd/uLRR/ad_radar_sensor/software/googletest/googletest/src/gtest_main.cc
[==========] Running 1 test from 1 test suite.
[----------] Global test environment set-up.
[----------] 1 test from TestSuiteSomeExampleClass
[ RUN      ] TestSuiteSomeExampleClass.TestInputValues
[       OK ] TestSuiteSomeExampleClass.TestInputValues (0 ms)
[----------] 1 test from TestSuiteSomeExampleClass (1 ms total)
[----------] Global test environment tear-down
[==========] 1 test from 1 test suite ran. (1 ms total)
[  PASSED  ] 1 test.
```