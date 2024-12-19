import os
import subprocess
import xml.etree.ElementTree as ET
import xlsxwriter
import sys

#create build directory
root_dir = os.getcwd() + "../../../"
build_dir="build"
os.makedirs(build_dir, exist_ok=True)
os.chdir(build_dir)

exe_name = "./uLRR_unit_tests"
gtest_output = "ulrr_gtest_output"
subprocess.run(["cmake", ".."])
subprocess.run(["make"])
subprocess.run([exe_name, "--verbose", "--gtest_output=xml:"+gtest_output+".xml"])


tree = ET.parse("./"+gtest_output+".xml")
root = tree.getroot()

workbook = xlsxwriter.Workbook(gtest_output+".xlsx")
worksheet = workbook.add_worksheet('gtest')
worksheet.write('A{}'.format(1), "TEST_SUITES")
worksheet.write('B{}'.format(1), "TEST_CASES")
worksheet.write('C{}'.format(1), "RESULT")
row = 2

failures=0
for test_suite in root.findall('.//testsuite'):
	test_suite_name = test_suite.get('name')
	worksheet.write('A{}'.format(row), test_suite_name)
	for test_case in test_suite.findall('.//testcase'):
		test_name = test_case.get('name')
		worksheet.write('B{}'.format(row), test_name)
		if test_case.find('failure') is not None:
			failures += 1
			worksheet.write('C{}'.format(row), 'FAILED')
			print('Test case failed: ' + test_case.get('name'))
			print(test_case.find('failure').text)
		else:
			worksheet.write('C{}'.format(row), 'PASSED')	
		row += 1
if failures > 0:
	sys.exit(1)
workbook.close()
