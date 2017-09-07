#-------------------------------------------------------------------------------
# Name:        module1
# Purpose:
#
# Author:      annada1
#
# Created:     10/08/2016
# Copyright:   (c) annada1 2016
# Licence:     <your licence>
#-------------------------------------------------------------------------------


#cloud_controller_tgraph = ".//*[@id='e0-t62ce62219462574b-ffffffef-584ee4fa-925211fa-1a64743e-cf0b9f8-190feac6']"

class GuiConstants(object):
    xpath_cloud_controller_thread = "//*[@title='Cloud Controller Threads']"
    cloud_controller_tgraph = ".//*[@id='e0-t62ce62219462574b-ffffffef-584ee4fa-925211fa-1a64743e-cf0b9f8-190feac6']"
    click_table_cloud_controller_threads = ".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-925211fa-1a64743e-cf0b9f8']/td[1]/div/span"
    legend_item_cloud_controller_thread1 = ".//*[text()='cc.thread_info.event_machine.threadqueue.size' and @class='ui-button-text']"
    legend_item_cloud_controller_thread2 = ".//*[text()='cc.thread_info.event_machine.resultqueue.size' and @class='ui-button-text']"
    legend_item_cloud_controller_thread3 = ".//*[text()='cc.thread_info.event_machine.connection_count' and @class='ui-button-text']"
    legend_item_cloud_controller_thread4 = ".//*[text()='cc.thread_info.event_machine.resultqueue.num_waiting' and @class='ui-button-text']"
    legend_item_cloud_controller_thread5 = ".//*[text()='cc.thread_info.event_machine.threadqueue.num_waiting' and @class='ui-button-text']"
    legend_item_cloud_controller_thread6 = ".//*[text()='cc.thread_info.thread_count' and @class='ui-button-text']"
    line_graph_connection_count = ".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-925211fa-1a64743e-cf0b9f8']/td[3]/div/span/span[2]/canvas"
    line_graph_resqueue_waiting = ".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-925211fa-1a64743e-cf0b9f8']/td[4]/div/span/span[2]/canvas"
    line_graph_resqueue_size = ".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-925211fa-1a64743e-cf0b9f8']/td[5]/div/span/span[2]/canvas"
    line_graph_threadqueue_waiting = ".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-925211fa-1a64743e-cf0b9f8']/td[6]/div/span/span[2]/canvas"
    line_graph_threadqueue_size = ".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-925211fa-1a64743e-cf0b9f8']/td[7]/div/span/span[2]/canvas"

    cloud_controller_log_errors = "//*[@title='Cloud Controller Log Errors']"
    error_log_count = ".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-925211fa-b5786efe-cf0b9f8']/td[3]/div/span/span[2]/canvas"
    fatal_log_count = ".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-925211fa-b5786efe-cf0b9f8']/td[4]/div/span/span[2]/canvas"
    warn_log_count = ".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-925211fa-b5786efe-cf0b9f8']/td[5]/div/span/span[2]/canvas"
    cloud_controller_log_errors_table = ".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-925211fa-b5786efe-cf0b9f8']/td[1]/div/span"
    cloud_controller_log_errors_graph = ".//*[@id='e0-t62ce62219462574b-ffffffef-584ee4fa-925211fa-b5786efe-cf0b9f8-e4fc8cae']"
    legend_item_cloud_controller_error = ".//*[text()='log_count[level=error]' and @class='ui-button-text']"
    legend_item_cloud_controller_fatal = ".//*[text()='log_count[level=fatal]' and @class='ui-button-text']"
    legend_item_cloud_controller_warn = ".//*[text()='log_count[level=warn]' and @class='ui-button-text']"


    situations_to_watch_cloud_controller= "//*[@title='Cloud Controller']"
    situations_to_watch_cloud_controller_error = ".//*[@id='l0-t62ce62219462574b-ffffffef-78b1520e-cd96fc77-8a473b3d-cf0b9f8']/td[2]/div/span/span[2]/canvas"
    situations_to_watch_cloud_controller_fatal = ".//*[@id='l0-t62ce62219462574b-ffffffef-78b1520e-cd96fc77-8a473b3d-cf0b9f8']/td[3]/div/span/span[2]/canvas"
    situations_to_watch_cloud_controller_warn = ".//*[@id='l0-t62ce62219462574b-ffffffef-78b1520e-cd96fc77-8a473b3d-cf0b9f8']/td[4]/div/span/span[2]/canvas"
    situations_to_watch_table = ".//*[@id='l0-t62ce62219462574b-ffffffef-78b1520e-cd96fc77-8a473b3d-cf0b9f8']/td[1]/div/span"
    situations_to_watch_cloud_controller_graph=".//*[@id='e0-t62ce62219462574b-ffffffef-78b1520e-cd96fc77-8a473b3d-cf0b9f8-e4fc8cae']"

    situations_to_watch_table_etcd = ".//*[@id='l0-t62ce62219462574b-ffffffef-78b1520e-c1338cdd-a4796009-3f4e0920']/td[1]/div/span"
    situations_to_watch_table_etcd_graph = ".//*[@id='e0-t62ce62219462574b-ffffffef-78b1520e-c1338cdd-a4796009-3f4e0920-527c9148']"


    legend_item_routerhealth_thread1 = ".//*[text()='router.rejected_requests' and @class='ui-button-text']"
    legend_item_routerhealth_thread2 = ".//*[text()='router.total_requests' and @class='ui-button-text']"
    legend_item_routerhealth_thread3 = ".//*[text()='healthy' and @class='ui-button-text']"
    legend_item_routerhealth_thread4 = ".//*[text()='router.routed_app_requests' and @class='ui-button-text']"
    legend_item_routerhealth_thread5 = ".//*[text()='router.bad_gateways' and @class='ui-button-text']"
    legend_item_routerhealth_thread6 = ".//*[text()='router.total_routes' and @class='ui-button-text']"
    legend_item_routerhealth_thread7 = ".//*[text()='router.requests_per_sec' and @class='ui-button-text']"
    legend_item_chargebackH_thread1 = ".//*[text()='(GbHrs)' and @class='ui-button-text']"
    legend_item_chargebackH_thread2 = ".//*[text()='(Hrs)' and @class='ui-button-text']"

    line_graph_cloudC_health_cpu = ".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-925211fa-40f0b8a8-cf0b9f8']/td[5]/div/span/span[2]/canvas"
    line_graph_cloudC_health_ram_c = ".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-925211fa-40f0b8a8-cf0b9f8']/td[6]/div/span/span[2]/canvas"
    line_graph_cloudC_health_ram_f = ".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-925211fa-40f0b8a8-cf0b9f8']/td[7]"
    line_graph_cloudC_health_ram_u = ".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-925211fa-40f0b8a8-cf0b9f8']/td[8]/div/span/span[2]/canvas"
    line_graph_routerh_badgateways = ".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-d774a820-42d6ae66-95e0f588']/td[5]/div/span/span[2]/canvas"
    line_graph_routerh_rejectedreqs = ".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-d774a820-42d6ae66-95e0f588']/td[6]/div/span/span[2]/canvas"
    line_graph_routerh_routedapp = ".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-d774a820-42d6ae66-95e0f588']/td[7]/div/span/span[2]/canvas"
    line_graph_routerh_totalreqs = ".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-d774a820-42d6ae66-95e0f588']/td[8]/div/span/span[2]/canvas"
    line_graph_routerh_reqspersec = ".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-d774a820-42d6ae66-95e0f588']/td[9]/div/span/span[2]/canvas"
    line_graph_routerh_totalroutes = ".//*[@id='l0-t62ce62219462574b-ffffffef-584ee4fa-d774a820-42d6ae66-95e0f588']/td[10]/div/span/span[2]/canvas"
