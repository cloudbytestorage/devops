#!/usr/bin/env python
#title           :DriverScript.py
#description     :Driver/Engine where the actual execution starts.
#author          :Sudarshan D
#date            :20160504
#version         :1
#usage           :python DriverScript.py
#notes           :
#python_version  :2.7
#==============================================================================

import types, os, yaml, sys, datetime, importlib, yamlordereddictloader, traceback
from ES_1.constants import Constants as const
from FCM.utils.ResultUtils import ResultUtilities as Rutils
from GUIConfig import GuiConfig as Gconst

# ---
script_dir = os.sep.join(os.path.realpath(__file__).split(os.sep)[:-1])
import_path = os.path.realpath(os.path.join(script_dir, '../'))
sys.path.append(import_path)
# --
os.environ['PYTHONPATH'] = import_path

def getTestSet(testsetloc, testtype):
    execution_list = []
    commented_list = []
    result = {}
    print testsetloc
    try:
        my_dictionary = yaml.load(open(testsetloc), Loader=yamlordereddictloader.Loader)
        for key in my_dictionary[testtype].keys():
            if my_dictionary[testtype][key] == "execute":
                execution_list.append(key)
            else:
                commented_list.append(key)

    except IOError, (errno, strerror):
        print "I/O error(%s): %s" % (errno, strerror)
    except:
        print("Unexpected error:", sys.exc_info()[0])
        raise
    finally:
        result['execution_list'] = execution_list
        result['commented_list'] = commented_list
        result['execution_count'] = len(execution_list)
        result['commented_count'] = len(commented_list)
        return result
# </editor-fold>

def main():
    try:
        summaryreportpath = Rutils.createSummaryReport(const.dict['sol_name'])
        result_summary =[]
        tc_exe_details = []
        testsetloc = const.dict['testsetloc']
        testtype = const.dict['testtype']
        test_cases_details = getTestSet(testsetloc, testtype)
        for tcName in test_cases_details['execution_list']:
            print "Executing: ",tcName
            # /SCM/TestScripts/tc1 not tc1.py
            tc_abspath = const.scmpath + os.path.sep + 'TestScripts'+ os.path.sep+ tcName
            tcexecution_start_time = datetime.datetime.now()
            filename = tc_abspath+'.py'
            if not os.path.exists(filename):
                raise Exception('ERROR: {} does not exist'.format(filename))
            try:
                def is_test_function(module, attr):
                    return (attr == 'main') and isinstance(getattr(module, attr), types.FunctionType)

                sys.path.append(os.path.join(const.scmpath, 'TestScripts'))
                t = importlib.import_module(tcName)
                test_funcs = sorted([attr for attr in dir(t) if is_test_function(t, attr)])

                for test_func in test_funcs:
                    ts_list_totaldetails = getattr(t, test_func)()

                tcexecution_end_time = datetime.datetime.now()
                tc_execution_time = Rutils.timeDifference(tcexecution_start_time, tcexecution_end_time)
                # appending the test-set summary to tc.html file.
                # final_tc_result will have pass/fail status of tc.
                tcresult_fileabspath = Rutils.generate_tslist_summary(tcName, ts_list_totaldetails)

                final_tc_result = tcresult_fileabspath.split("&&")[0]
                tc_result_file = (tcresult_fileabspath.split("&&")[1]).split(os.path.sep)[len((tcresult_fileabspath.split("&&")[1]).split(os.path.sep)) - 1]

                # Format should be storyID||tcName||executionTime||status||link
                tc_exe_detail = "US123" + "&&" + tcName + "&&" + str(tc_execution_time) + "&&" +final_tc_result + "&&"+ tc_result_file
                tc_exe_details.append(tc_exe_detail)

                # result_summary will have the list of pass/fail status of all the testcases.
                result_summary.append(tcName+":"+final_tc_result)
                final_result_txt_file = open(summaryreportpath+os.path.sep+"result_summary.txt", 'a')
                final_result_txt_file.write(tcName+":"+final_tc_result+"\n")
                final_result_txt_file.close()
            except Exception as ex:
                "$$$$$$ Exception in testcase:" + tcName +":"+format(ex)+"$$$$$$$$"

    except IOError as e:
        print >> sys.stderr, traceback.format_exc(), "$$$$$Exception occurred in main$$$$$"
        traceback.print_exc()

    finally:
        tcs_result_summary = Rutils.generate_tclist_summary(tc_exe_details, summaryreportpath)
        Rutils.endSummaryReport()

if __name__ == '__main__':
     main()