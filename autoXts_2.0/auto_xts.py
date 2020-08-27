import os
import time
import re

try:
    from bs4 import BeautifulSoup
    import configparser
    from prettytable import PrettyTable
except:
    os.system("pip3 install bs4")
    os.system("pip3 install configparser")
    os.system("pip3 install prettytable")
    time.sleep(1)
    from bs4 import BeautifulSoup
    import configparser
    from prettytable import PrettyTable

def executed_xts(runfile, command, seconds):
    time.sleep(2)
    run = 'gnome-terminal -- ' + runfile + ' ' + command
    width = os.get_terminal_size().columns
    print("*".center(width, '*'))
    os.system(run)
    time.sleep(seconds)
    files = os.listdir("../results/")
    files = sorted(files)
    if len(files) % 2 == 0:
        if len(files) >= 2:
            return files[-2]
        else:
            return files[0]
    elif len(files) % 2 == 1:
        return files[-1]

def if_result_done(resul_file):
    files_zip = "../results/" + resul_file + ".zip"
    if os.path.exists(files_zip):
        return resul_file
    else:
        return "not done"

def check_results(file_name):
    filepath = os.getcwd()
    path = re.findall("(.*?).autoXts", filepath)
    new_path = path[0]
    url = os.path.join(new_path + "/results/" + file_name + "/test_result_failures_suite.html")
    with open(url, 'r') as f:
        soup = BeautifulSoup(f.read(), 'lxml').html
        result_pass = re.findall('.*?<td class="rowtitle">Tests Passed</td>.*?>(.*?)</.*?', str(soup))
        result_fail = re.findall('.*?<td class="rowtitle">Tests Failed</td>.*?>(.*?)</.*?', str(soup))
        result_module_done = re.findall('.*?<td class="rowtitle">Modules Done</td>.*?>(.*?)</.*?', str(soup))
        result_module_total = re.findall('.*?<td class="rowtitle">Modules Total</td>.*?>(.*?)</.*?', str(soup))
        results_list = [result_pass[0], result_fail[0], result_module_done[0], result_module_total[0]]
        if result_fail[0] == "0":
            return results_list, "done"
        fail_module_name = re.findall('.*?<td class="module" colspan="3"><a.*?>.*?(C.*?)</a>.*?', str(soup))
        se_cases = "CtsSecureElementAccessControlTestCases1" or \
                  "CtsSecureElementAccessControlTestCases2" or \
                  "CtsSecureElementAccessControlTestCases3" or \
                  "CtsSecureElementAccessControlTestCases1[instant]" or \
                  "CtsSecureElementAccessControlTestCases2[instant]" or \
                  "CtsSecureElementAccessControlTestCases3[instant]" or \
                  "VtsHalSecureElementV1_0Target"
        if se_cases in fail_module_name:
            return results_list, "se"
        sim_cases = "CtsTelecomTestCases" or \
                   "CtsTelecomTestCases2" or \
                   "CtsTelecomTestCases3" or \
                   "CtsTelephony2TestCases" or \
                   "CtsTelephony2TestCases[instant]" or \
                   "CtsTelephony3TestCases" or \
                   "CtsTelephonyProviderTestCases" or \
                   "CtsTelephonySdk28TestCases" or \
                   "CtsTelephonyTestCases" or \
                   "CtsPermissionTestCasesTelephony" or \
                   "CtsPermissionTestCasesTelephony[instant]" or \
                   "GtsTelephonyTestCases" or \
                   "GtsTelecomManagerTests" or \
                   "VtsHalAudioEffectV5_0Target" or \
                   "VtsHalAudioV2_0Target" or \
                   "VtsHalAudioV5_0Target" or \
                   "VtsHalRadioConfigV1_0Target"
        if sim_cases in fail_module_name:
            return results_list, "sim"
        uicc_cases = "CtsCarrierApiTestCases" or "GtsSimAppDialogTestCases"
        if uicc_cases in fail_module_name:
            return results_list, "uicc"
        return results_list, "all"

def read_config():
    config = configparser.ConfigParser()
    config.read("./config.init")
    test_item = config.get("config", "test_item")
    executed_file = config.get("config", "executed_file")
    executed_command = config.get("config", "executed_command")
    executed_command_1 = config.get("config", "executed_command_1")
    device_number = config.get("config", "device_number")
    full_run_number = config.get("config", "full_run_number")
    device1 = config.get("config", "device1")
    device2 = config.get("config", "device2")
    device3_uicc = config.get("config", "device3_uicc")
    device4_se = config.get("config", "device4_se")
    device5_sim = config.get("config", "device5_sim")
    device_set_all = config.get("config", "device_set_all")
    return test_item, executed_file, executed_command, executed_command_1, device_number, \
           full_run_number, device1, device2, device3_uicc, device4_se, device5_sim, device_set_all

def main():
    break_flag = False
    new_executed_command = ""
    test_item, executed_file, executed_command, executed_command_1, device_number, full_run_number, device1, device2, device3_uicc, device4_se, device5_sim, device_set_all = read_config()
    if "retry" in executed_command:
        index = 1
        new_executed_command = executed_command
    else:
        index = 0
    while True:
        test_item, executed_file, executed_command, executed_command_1, device_number, full_run_number, device1, device2, device3_uicc, device4_se, device5_sim, device_set_all = read_config()
        width = os.get_terminal_size().columns
        if test_item == "CTS":
            seconds = 100
            #global seconds
        else:
            seconds = 60
            #global seconds
        if index != 0:
            result_file = executed_xts(executed_file, new_executed_command, seconds)
            time.sleep(1)
            print("-{}- start testing".format(test_item).center(width))
            data = os.popen("ps a | grep bash").read()
            pid = re.findall("(.*?) pts/.*?/bash ../tools/{}-.*?".format(test_item.lower()), data)
            pids = "".join(pid[0])
        else:
            result_file = executed_xts(executed_file, executed_command, seconds)
            time.sleep(1)
            print("-{}- start testing".format(test_item).center(width))
            data = os.popen("ps a | grep bash").read()
            pid = re.findall("(.*?) pts/.*?/bash ../tools/{}-.*?".format(test_item.lower()), data)
            pids = "".join(pid[0])
        while True:
            test_item, executed_file, executed_command, executed_command_1, device_number, full_run_number, device1, device2, device3_uicc, device4_se, device5_sim, device_set_all = read_config()
            time.sleep(30)
            result = if_result_done(result_file)
            if result != "not done":
                time.sleep(120)
                os.popen("kill -9 {}".format(pids))
                # print("\n第" + str(index + 1) + "次执行完成正在分析结果")
                results_list, strif = check_results(result)
                p = PrettyTable(["Session", "Tests Passed", "Tests Failed", "Modules Done", "Modules Total"])
                passed = results_list[0]
                failed = results_list[1]
                done = results_list[2]
                total = results_list[3]
                p.add_row([str(index+1), passed, failed, done, total])
                print(p)
                if full_run_number == 2:
                    executed_command = executed_command.replace(executed_command_1, "retry --retry 0")
                    new_executed_command = executed_command
                    index += 1
                    full_run_number = 1
                    break
                else:
                    if strif == "done":
                        print("\nTest all pass，test done")
                        break_flag = True
                        break
                    if strif == "se":
                        new_executed_command = "run retry --retry {} -s {}".format(index, device4_se)
                        index += 1
                        break
                    if strif == "sim":
                        new_executed_command = "run retry --retry {} -s {}".format(index, device5_sim)
                        index += 1
                        break
                    if strif == "uicc":
                        new_executed_command = "run retry --retry {} -s {}".format(index, device3_uicc)
                        index += 1
                        break
                    if strif == "all":
                        new_executed_command = "run retry --retry {} -s {}".format(index, device_set_all)
                        index += 1
                        break
            else:
                continue
        if break_flag == True:
            break
if __name__ == "__main__":
    main()
