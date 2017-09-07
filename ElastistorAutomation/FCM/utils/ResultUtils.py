#!/usr/bin/env python

import datetime
import time
import os
import sys
import traceback

from FCM.utils.DateUtils import DateUtilities as Dutils
from FCM.utils.FileUtils import FileUtilities as Futils
from FCM.utils.XMLUtils import XMLUtilities as Xmlutils
from SCM.constants import Constants as const


_author_='naveenkumar b'
_email_='naveen.b@emc.com'

class ResultUtilities:
    str_exec_result_folder = ""
    exec_start_time = Dutils.getCurrentDate("%H:%M:%S")
    startTime = datetime.datetime.now()
    endTime = datetime.datetime.now()
    summary_start_date = time.time()
    summary_start_time = time.time()
    startDate = datetime.datetime.now()
    detail_start_date = time.time()
    detail_start_time = time.time()
    str_current_report_filename = ""
    str_report_file=""
    inTestCount = 0
    inStepCount = 0
    reportFilesMap = {}
    strThreadID = ""
    strCurrentReportID = ""
    strReportFileMap = {}

    @staticmethod
    def createSummaryReport(str_script_name):
        try:
            summary_start_date = Dutils.getCurrentDate("%d-%m-%y")
            summary_start_time = Dutils.getCurrentDate("%H:%M:%S")
            # Below line is static variable which will record the starttime. donot delete below line
            ResultUtilities.startTime = datetime.datetime.now()
            ResultUtilities.startDate = Dutils.getCurrentDate("%d-%m-%y")
            str_suite_name = str_script_name
            # result of below line looks like Result/NHC1.0-2016_May_17_15:14:40
            str_report_folder = const.nhcpath+os.path.sep+'Result'+os.path.sep+str_suite_name+"-"+datetime.datetime.now().year.__str__()+"_" +\
                                Dutils.getCurrentDate("%b_%d") + "_" + Dutils.getCurrentDate("%H_%M_%S")
            ResultUtilities.str_exec_result_folder = str_report_folder
            Futils.mkdir(str_report_folder)
            Futils.mkdir(str_report_folder + os.path.sep + "screenshot")
            str_summary_file = str_report_folder + os.path.sep+"Summary.html"

            #Futils.copy_tree(os.path.dirname("C:/Users/bn3/PycharmProjects/NHC/FCM/template/"), str_report_folder)
            Futils.copy_tree(const.fcmpath+os.path.sep+"template"+os.path.sep, str_report_folder)
            #Futils.copy_tree(os.path.dirname("FCM/template/"), str_report_folder)
            Xmlutils.add_text(str_summary_file, "&header&", str_script_name)
            Xmlutils.add_text(str_summary_file, "&testEnv&",const.dict['testEnv'])
            # Xmlutils.add_text(str_summary_file, "&sTime&", summary_start_time)
            Xmlutils.add_text(str_summary_file, "&date&", summary_start_date)
            ResultUtilities.strReportFileMap = {}
        except IOError as e:
            print >> sys.stderr, traceback.format_exc()
            traceback.print_exc()
        finally:
            return str_report_folder


    @staticmethod
    def timeDifference(starttime, endtime):
        return endtime - starttime

    @staticmethod
    def logger(my_list, strDesc, strExp, strActual, strResult):

        strTS_info = strDesc+"&&"+strExp+"&&"+strActual+"&&"+strResult

        if len(strTS_info.split("&&")) != 4:
            my_list.append(strTS_info + "&&" + str(Dutils.getCurrentDate("%H:%M:%S")))
            my_list.append("Pls provide all the log information to above Log in logger function&&-&&-&&info&&" + str(Dutils.getCurrentDate("%H:%M:%S")))
        else:
            my_list.append(strTS_info + "&&" + str(Dutils.getCurrentDate("%H:%M:%S")))
        return my_list


    @staticmethod
    def endSummaryReport():
        # time.sleep(10)
        str_summary_file = ResultUtilities.str_exec_result_folder + os.path.sep+"Summary.html"
        summary_end_time = Dutils.getCurrentDate("%H:%M:%S")
        ResultUtilities.endTime = datetime.datetime.now()
        Xmlutils.add_text(str_summary_file, "&eTime&", summary_end_time)
        # summary_end_date = Dutils.getCurrentDate("%d-%m-%y")
        total_time = ResultUtilities.timeDifference(ResultUtilities.startTime, ResultUtilities.endTime)
        str_total_time = total_time.__str__()
        hrs = str_total_time.split(':')[0]
        mins = str_total_time.split(':')[1]
        secs = str_total_time.split(':')[2].split(".")[0]
        # print("%s hrs, %s mins, %s secs" %(hrs, mins, secs))
        Xmlutils.add_text(str_summary_file, "&tTime&", "%sh %sm %ss" % (hrs, mins, secs))
        Xmlutils.add_text(str_summary_file, "&tCount&", str(ResultUtilities.inTestCount))
        ResultUtilities.inTestCount = 0


    @staticmethod
    def generate_tslist_summary(str_script_name, ts_list_totaldetails):

        try:
            # create test step wise tc dummy html report based on timestamp.
            ResultUtilities.detail_start_time = Dutils.getCurrentDate("%H:%M:%S")
            ResultUtilities.detail_start_date = Dutils.getCurrentDate("%d-%m-%y")
            str_report_filename = str_script_name + "-" + datetime.datetime.now().year.__str__() + "_" + Dutils.getCurrentDate(
                "%b_%d") + "_" + Dutils.getCurrentDate("%H_%M_%S")
            ResultUtilities.str_report_file = str_report_filename + ".html"
            ResultUtilities.str_current_report_filename = ResultUtilities.str_report_file
            Futils.createFile(ResultUtilities.str_exec_result_folder + os.path.sep + ResultUtilities.str_report_file)
            INPUT_FILE = ResultUtilities.str_exec_result_folder + os.path.sep + ResultUtilities.str_report_file


            test_step_data = []
            final_result = []
            pass_count, fail_count, cur_date = 0, 0, datetime.datetime.now()

            # splitting result and forming dynamic html rows for displaying result
            for i in range(len(ts_list_totaldetails)):
                try:
                    data = {}
                    data_set = ts_list_totaldetails[i].split('&&', 4)
                    data["sno"] = str(i+1)
                    data["description"] = data_set[0]
                    data["expected"] = data_set[1]
                    data["actual"] = data_set[2]
                    data_set[3] = str(data_set[3].lower())
                    data["status"] = data_set[3]
                    final_result.append(str(data_set[3].lower()))
                    data["link"] = "dummy"

                    try:
                        data["execution_time"] = str(data_set[4])
                    except:
                        data["execution_time"] = Dutils.getCurrentDate("%H:%M:%S")
                except:
                    print "Exception occured in resultutil: generate_tslist_summary"
                finally:
                    if data_set[3] == 'pass':
                        pass_count = pass_count + 1
                    elif data_set[3] == 'fail' or data_set[3] == 'exception':
                        fail_count = fail_count + 1
                    test_step_data.append(data)
            if "fail" in final_result or "exception" in final_result:
                final_result = "Fail"
            else:
                final_result = "Pass"
            ResultUtilities.generate_teststeps_htmlfile(str_script_name, test_step_data,INPUT_FILE, pass_count, fail_count, cur_date)
        except:
            "exception occuered in: generate_tslist_summary_2"
        finally:
            return final_result+"&&"+INPUT_FILE

    @staticmethod
    def generate_tclist_summary(tc_exe_details, src_htmlpath):
        tcs_data = []
        pass_count, fail_count, cur_date = 0, 0, datetime.datetime.now()
        for i in range(len(tc_exe_details)):
            data = {}
            data_set = tc_exe_details[i].split("&&")
            data["sno"] = str(i + 1)
            data["storyId"] = data_set[0]
            data["scriptName"] = data_set[1]
            data["execution_time"] = data_set[2]
            data["status"] = data_set[3]
            data["tc_filepath"] = data_set[4]

            if data_set[3] == "Pass":
                pass_count = pass_count + 1
            else:
                fail_count = fail_count + 1
            tcs_data.append(data)

        ResultUtilities.generate_summary_htmlfile(src_htmlpath, tcs_data, pass_count, fail_count)

        return tcs_data

    @staticmethod
    def generate_teststeps_htmlfile(str_script_name, test_step_data,src_html_file,pass_count,fail_count,cur_date):
        head = '<?xml version="1.0" encoding="UTF-8"?>\n<html>\n\n' \
               '<head> <meta http-equiv="Content-Type" content="text/html; ' \
               'charset=UTF-8" />  \n ' \
               '<style>.datagrid table {text-align: left; width: 100%; border: 1px solid black;}' \
               '.datagrid { font: normal 12px/150% Arial, Helvetica, sans-serif; background: #fff; overflow-x:auto; ' \
               'border: 1px solid #006699; -webkit-border-radius: 3px; -moz-border-radius: 3px; ' \
               'border-radius: 3px; }' \
               '.datagrid table td, ' \
               '.datagrid table th { ' \
               'padding: 3px 10px; }' \
               '.datagrid table thead th { background-color:#006699; color:#FFFFFF; font-size: 12px; font-weight: ' \
               'bold; border-left: 1px solid #0070A8; } ' \
               '.datagrid table thead th:first-child { border: none; }' \
               '.datagrid table tbody td { color: #00557F; border-left: 2px solid #E1EEF4;' \
               'font-size: 12px;font-weight: normal; }' \
               '.datagrid table tbody .alt td { background: #E1EEf4; color: #00557F; }' \
               '.datagrid table tbody td:first-child { border-left: none}' \
               '.datagrid table tbody tr:last-child td { border-bottom: none; }' \
               '.datagrid table tfoot td div { border-top: 1px solid #006699;background: #E1EEf4;} ' \
               '.datagrid table tfoot td { padding: 0; font-size: 12px } ' \
               '.datagrid table tfoot td div{ padding: 2px; }' \
               '.datagrid table tfoot td ul { margin: 0; padding:0; list-style: none; text-align: right; }' \
               '.datagrid table tfoot li { display: inline; }' \
               '.datagrid table tfoot li a { text-decoration: none; display: inline-block; padding: 2px 8px; margin: 1px;color: ' \
               '#FFFFFF;border: 1px solid #006699;-webkit-border-radius: 3px; -moz-border-radius: 3px; border-radius: 3px; ' \
               'background:-webkit-gradient( linear, left top, left bottom, color-stop(0.05, #006699), ' \
               'color-stop(1, #00557F) );background:-moz-linear-gradient( center top, #006699 5%, #00557F 100% );' \
               'filter:progid:DXImageTransform.Microsoft.gradient(startColorstr=\'#006699\', endColorstr=\'#00557F\');' \
               'background-color:#006699; }' \
               '.datagrid table tfoot ul.active, .datagrid table tfoot ul a:hover { text-decoration:none;' \
               'border-color: #00557F; color: #FFFFFF; background: none;background-color:#006699; }' \
               '.serviceDetail table { border-collapse: collapse; text-align: left; }' \
               '.serviceDetail { font: normal 9px/150% Arial, Helvetica, sans-serif; 	background: #fff;' \
               ' overflow-x: auto; border: 1px solid #1e1e1e; width: 85%; }' \
               '.serviceDetail table td, .serviceDetail table th { padding: 3px 10px; }' \
               '.serviceDetail table thead th {	background-color:#aaccee; color:#000000; font-size: 10px; ' \
               'font-weight: bold; border-left: 1px solid #aaccee; }' \
               '.serviceDetail table thead th:first-child {	border: none; }' \
               '.serviceDetail table tbody td {	color: #000000; border-left: 2px solid #E1EEF4;' \
               'font-size: 10px;font-weight: normal; }' \
               '.serviceDetail table tbody .alt td {	background: #E1EEf4; color: #00557F;}' \
               '.serviceDetail table tbody td:first-child {	border-left: none; }' \
               '.serviceDetail table tbody tr:last-child td { border-bottom: none; }' \
               '.serviceDetail table tfoot td div {	border-top: 1px solid #006699;background: #E1EEf4; }' \
               '.serviceDetail table tfoot td { padding: 0; font-size: 12px }' \
               '.serviceDetail table tfoot td div { padding: 2px; }' \
               '.serviceDetail table tfoot td ul {	margin: 0; padding:0; list-style: none; text-align: right; }' \
               '.serviceDetail table tfoot li {	display: inline; }' \
               '.serviceDetail table tfoot li a {	text-decoration: none;	display: inline-block;	padding: 2px 8px;' \
               'margin: 1px;	color: #FFFFFF;	border: 1px solid #006699;	-webkit-border-radius: 3px;	-moz-border-radius: 3px;	' \
               'border-radius: 3px;	background:-webkit-gradient( linear, left top, left bottom, color-stop(0.05, #006699), ' \
               'color-stop(1, #00557F) );	background:-moz-linear-gradient( center top, #006699 5%, #00557F 100% );' \
               'filter:progid:DXImageTransform.Microsoft.gradient(startColorstr=\'#006699\', endColorstr=\'#00557F\');' \
               'background-color:#006699; }' \
               '.serviceDetail table tfoot ul.active, .serviceDetail table tfoot ul a:hover { text-decoration:none;border-color: #00557F; color: #FFFFFF; background: none;background-color:#006699;}' \
               '</style> \n' \
               '<style>' \
               '#td{ border: 1px solid black; border-color: black}' \
               'table#summary tr:nth-child(even){background-color:#eee;} \n' \
                'table#summary tr:nth-child(odd){background-color:#fff;}'\
                '</style>'\
               '<script type="text/javascript"src="codebase/js/jquery.min.js">//Test</script> \n' \
               '<script src="codebase/js/highcharts.js">//Test</script>\n' \
               '<script src="codebase/js/result.js">//Test</script> \n' \
               '<script type = "text/javascript" src = "codebase/js/loader.js" > </script >' \
               '<script type = "text/javascript" > \n' \
               ' google.charts.load(\'current\','\
               '{\'packages\': [\'corechart\']}); ' \
               'google.charts.setOnLoadCallback(drawChart);'\
               'function drawChart(){' \
               'var data = google.visualization.arrayToDataTable('\
               '[[\'Task\', \'Hours per Day\'], [\'Work\', 0], [\'Fail\', '+ str(fail_count) +'], [\'Commute\', 0], ' \
                '[\'Pass\', '+ str(pass_count)+'],' \
               '[\'Sleep\', 0]]); ' \
               'var options = {}; ' \
               'var chart = new google.visualization.PieChart(document.getElementById(\'piechart\'));'\
               'chart.draw(data, options);} </script >\n'\
               '</head>\n ' \
               '<body onload="detail("container","test");">\n <div align="center">\n<h1 id="header">&header&</h1></div>\n'


        table = '<table align="center">\n <tr> <td> <div id="piechart" style="width: 500px; height: 500px;""></div></td> <td>\n' \
                '<div class="datagrid"> \n<table><thead> <tr>\n ' \
                '<th>Date</th> <th>No. of Steps Passed</th> <th>No. of Steps Failed</th></tr></thead>\n' \
                '<tbody><tr><td id="date">' + str(cur_date) + '</td>\n<td id="pCount">' + str(
            pass_count) + '</td>\n<td id="fCount">' + str(fail_count) + '</td>\n</tr>\n' \
            '</tbody> </table> </div> </td></tr></table>\n'

        body = '<div class="datagrid">\n <table>\n<thead><tr><th>S.No.</th>\n' \
               '<th>Description</th>\n<th>Expected</th>\n<th>Actual</th>\n<th>Timestamp</th>\n<th>Status</th>\n<th>Link</th>\n' \
               '</tr>'

        footer = '\n</thead>\n<tbody> </tbody> \n  </table>\n </div> \n </body>\n</html>'
        dynamic_data = ''
        for i in range(len(test_step_data)):
            if test_step_data[i]['status'].lower() == 'pass':
                dynamic_data = dynamic_data + '<tr><td id="td">\n' + test_step_data[i]['sno'] + '</td><td id="td">\n' + test_step_data[i][
                'description'] + '</td>\n<td id="td">' + test_step_data[i]['expected'] + '</td>\n<td id="td">' + test_step_data[i][
                               'actual'] + '</td><td id="td">' + test_step_data[i]['execution_time'] + '</td>\n<td id="td", bgcolor="#00FF00">' + \
                           test_step_data[i]['status'] + '</td>\n<td id="td">' + test_step_data[i]['link'] + '</td>\n</tr>\n'
            elif test_step_data[i]['status'].lower() == 'fail':
                dynamic_data = dynamic_data + '<tr><td id="td">\n' + test_step_data[i]['sno'] + '</td><td id="td">\n' + \
                               test_step_data[i][
                                   'description'] + '</td>\n<td id="td">' + test_step_data[i]['expected'] + '</td>\n<td id="td">' + \
                               test_step_data[i][
                                   'actual'] + '</td><td id="td">' + test_step_data[i]['execution_time'] + '</td>\n<td id="td", bgcolor="#FF0000">' + \
                               test_step_data[i]['status'] + '</td>\n<td id="td">' + test_step_data[i][
                                   'link'] + '</td>\n</tr>\n'
            else:
                dynamic_data = dynamic_data + '<tr><td id="td">\n' + test_step_data[i]['sno'] + '</td><td id="td">\n' + \
                               test_step_data[i][
                                   'description'] + '</td>\n<td id="td">' + test_step_data[i][
                                   'expected'] + '</td>\n<td id="td">' + \
                               test_step_data[i][
                                   'actual'] + '</td><td id="td">' + test_step_data[i][
                                   'execution_time'] + '</td>\n<td id="td", bgcolor="#958623">' + \
                               test_step_data[i]['status'] + '</td>\n<td id="td">' + test_step_data[i][
                                   'link'] + '</td>\n</tr>\n'

        html = head + table + body + dynamic_data + footer
        with open(src_html_file, 'w') as outfile:
            outfile.write(html)
        Xmlutils.add_text(src_html_file, "&header&", str_script_name)

    @staticmethod
    def generate_summary_htmlfile(src_htmlPath, tcs_data, pass_count, fail_count):
        head = '<?xml version="1.0" encoding="UTF-8"?>\n<html>\n\n' \
               '<head> <meta http-equiv="Content-Type" content="text/html; ' \
               'charset=UTF-8" />  \n ' \
               '<style>.datagrid table {text-align: left; width: 100%; border: 1px solid black;}' \
               '.datagrid { font: normal 12px/150% Arial, Helvetica, sans-serif; background: #fff; overflow-x:auto; ' \
               'border: 1px solid #006699; -webkit-border-radius: 3px; -moz-border-radius: 3px; ' \
               'border-radius: 3px; }' \
               '.datagrid table td, ' \
               '.datagrid table th { ' \
               'padding: 3px 10px; }' \
               '.datagrid table thead th ' \
               '{background:-webkit-gradient( linear, left top, left bottom, color-stop(0.05, #006699),' \
               ' color-stop(1, #00557F) );' \
               'background:-moz-linear-gradient( center top, #006699 5%, #00557F 100% );' \
               'filter:progid:DXImageTransform.Microsoft.gradient(startColorstr=\'#006699\', endColorstr=\'#00557F\');' \
               'background-color:#006699; color:#FFFFFF; font-size: 12px; ' \
               'font-weight: bold; border-left: 1px solid #0070A8; } ' \
               '.datagrid table thead th:first-child { border: none; }' \
               '.datagrid table tbody td { color: #00557F; border-left: 2px solid #E1EEF4;' \
               'font-size: 12px;font-weight: normal; }' \
               '.datagrid table tbody .alt td { background: #E1EEf4; color: #00557F; }' \
               '.datagrid table tbody td:first-child { border-left: none;}' \
               '.datagrid table tbody tr:last-child td { border-bottom: none; }' \
               '.datagrid table tfoot td div { border-top: 1px solid #006699;background: #E1EEf4;} ' \
               '.datagrid table tfoot td { padding: 0; font-size: 12px } ' \
               '.datagrid table tfoot td div{ padding: 2px; }' \
               '.datagrid table tfoot td ul { margin: 0; padding:0; list-style: none; text-align: right; }' \
               '.datagrid table tfoot li { display: inline; }' \
               '.datagrid table tfoot li a { text-decoration: none; display: inline-block; padding: 2px 8px; ' \
               'margin: 1px;color: #FFFFFF;border: 1px solid #006699;-webkit-border-radius: 3px; ' \
               '-moz-border-radius: 3px; border-radius: 3px; ' \
               'background:-webkit-gradient( linear, left top, left bottom, color-stop(0.05, #006699),' \
               ' color-stop(1, #00557F) );' \
               'background:-moz-linear-gradient( center top, #006699 5%, #00557F 100% );' \
               'filter:progid:DXImageTransform.Microsoft.gradient(startColorstr=\'#006699\', endColorstr=\'#00557F\');' \
               'background-color:#006699; }.datagrid table tfoot ul.active, ' \
               '.datagrid table tfoot ul a:hover { ' \
               'text-decoration:none;border-color: #00557F; color: #FFFFFF; background: none;' \
               'background-color:#006699;}</style>\n' \
               '<style> '\
               '#td{ border: 1px solid black; border-color: black}'\
               'table#summary tr:nth-child(even){background-color:#eee;}\n' \
               'table#summary tr:nth-child(odd){background-color:#fff;}'\
               '</style>' \
               '<script type="text/javascript"src="codebase/js/jquery.min.js"></script> \n' \
               '<script src="codebase/js/highcharts.js"></script>\n' \
               '<script src="codebase/js/result.js"></script> \n' \
               '<script type = "text/javascript" src = "codebase/js/loader.js" > </script >' \
               '<script type = "text/javascript" > \n' \
               ' google.charts.load(\'current\','\
               '{\'packages\': [\'corechart\']}); ' \
               'google.charts.setOnLoadCallback(drawChart);'\
               'function drawChart(){' \
               'var data = google.visualization.arrayToDataTable('\
               '[[\'Task\', \'Hours per Day\'], [\'Work\', 0], [\'Fail\', '+ str(fail_count) +'], [\'Commute\', 0], [\'Pass\', '+ str(pass_count)+'],' \
               '[\'Sleep\', 0]]); ' \
               'var options = {}; ' \
               'var chart = new google.visualization.PieChart(document.getElementById(\'piechart\'));'\
               'chart.draw(data, options);} </script >\n'\
               '</head>\n ' \
               '<body onload="summary("container","test");">\n ' \
               '<div align="center">\n<h1 id="header">&header&</h1></div>\n'

        table_envdetails = '<table align=\'center\'><tr> \n' \
                           '<td><div id="piechart" style="width: 500px; height: 500px;"></div></td> \n' \
                            '<td><div class=\'datagrid\'><table id=\'tblEnvDetails\'><thead>	' \
                           '<tr><th>Test Environment</th></tr>	</thead><tbody><tr><td id=\'testEnv\'>&testEnv&</td></tr></tbody></table>\n'


        table = '<table><thead><tr><th>Date</th><th>StartTime</th>' \
                '<th>EndTime</th><th>Execution Time</th><th>No. of TC passed</th><th>No. of TC Failed</th>' \
                '<th>Total Test Cases</th></tr>	</thead><tbody><tr><td id=\'date\'>&date&</td><td id=\'sTime\'>&sTime&</td>' \
                '<td id=\'eTime\'>&eTime&</td><td id=\'tTime\'>&tTime&</td><td id=\'pCount\'>'+ str(pass_count)+'</td>' \
                '<td id=\'fCount\'>' + str(fail_count) + '</td><td id=\'tCount\'>' + str(pass_count+fail_count) + '</td></tr></tbody></table></div></td></tr></table>'

        body = '<div class=\'datagrid\'><table><thead>'\
				'<tr><th>S.No.</th><th>Story ID</th><th>Script Name</th><th>Execution Time</th><th>Status</th></tr> '\

        footer = '\n</thead>\n<tbody> </tbody> \n  </table>\n </div> \n </body>\n</html>'

        dynamic_data = ''
        for i in range(len(tcs_data)):
            if tcs_data[i]['status'].lower() == 'pass':
                dynamic_data = dynamic_data + '<tr>\n<td id="td">' + tcs_data[i]['sno'] + '</td>\n' \
                '<td id="td"><a href="https://rally1.rallydev.com/#/38907343221d/dashboard"/>'+tcs_data[i]['storyId']+'</a></td>' \
                            '<td id="td"><a href=\"'+"."+os.path.sep+tcs_data[i]['tc_filepath']+'\">' + tcs_data[i]['scriptName'] + '</a></td>\n' \
                          '<td id="td">' + tcs_data[i]['execution_time'] + '</td>\n<td id="td", bgcolor="#00FF00">' + tcs_data[i]['status'] + '</td>\n' \
                          '</tr>\n'
            elif tcs_data[i]['status'].lower() == 'fail':
                dynamic_data = dynamic_data + '<tr>\n<td id="td">' + tcs_data[i]['sno'] + '</td>\n' \
                               '<td id="td"><a href="https://rally1.rallydev.com/#/38907343221d/dashboard"/>' + \
                               tcs_data[i]['storyId'] + '</a></td>' \
                               '<td id="td"><a href=\"' + tcs_data[i]['tc_filepath'] + '\">' + \
                               tcs_data[i]['scriptName'] + '</a></td>\n' \
                               '<td id="td">' + tcs_data[i]['execution_time'] + '</td>\n<td id="td"; bgcolor="#FF0000">' + \
                               tcs_data[i]['status'] + '</td>\n </tr>\n'

        html = head + table_envdetails + table + body + dynamic_data + footer
        with open(src_htmlPath+os.path.sep+"Summary.html", 'w') as outfile:
            outfile.write(html)
        summary_end_time = Dutils.getCurrentDate("%H:%M:%S")
        Xmlutils.add_text(src_htmlPath+os.path.sep+"Summary.html", "&eTime&", summary_end_time)
        Xmlutils.add_text(src_htmlPath+os.path.sep+"Summary.html", "&header&", const.dict['sol_name'])
        Xmlutils.add_text(src_htmlPath+os.path.sep+"Summary.html", "&testEnv&", const.dict['testEnv'])
        Xmlutils.add_text(src_htmlPath+os.path.sep+"Summary.html", "&sTime&", str(ResultUtilities.exec_start_time))
        Xmlutils.add_text(src_htmlPath+os.path.sep+"Summary.html", "&date&", ResultUtilities.startDate)

    @staticmethod
    def getCount():
        ResultUtilities.inTestCount += 1
        ResultUtilities.inStepCount = 0
        return ResultUtilities.inTestCount

    @staticmethod
    def getStepCount():
        ResultUtilities.inStepCount += 1
        return ResultUtilities.inStepCount