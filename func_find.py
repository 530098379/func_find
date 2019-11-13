#!/usr/bin/python

import os
import commands
import re

base_file_name = {}

def command(method_name):
    result_data = []
    result_data.append(method_name)
    status, output = commands.getstatusoutput("grep -wE 'file_name:|" + method_name + "' ./objdump.txt")
    if status == 0:
        output_list = output.split('\n')
        for output_str in output_list:
            output_str = output_str.strip("\n")

            s_file = output_str.find('file_name:')
            if s_file > -1:
                file_name = output_str[10:]

            s_index = output_str.find('<')
            e_index = output_str.find('+')

            if s_index == -1 or e_index == -1:
                continue

            call_name = output_str[s_index + 1:e_index]

            if call_name != method_name:
                if (call_name != 'func01' or method_name != 'func02'):
                    if call_name == 'main':
                        result_data.append(call_name + '-' + file_name)
                        base_file_name[call_name + '-' + file_name] = file_name
                    else:
                        result_data.append(call_name)
                        base_file_name[call_name] = file_name

        news_result_data = []
        for rd in result_data:
            if rd not in news_result_data:
                news_result_data.append(rd)
        print news_result_data

        if len(news_result_data) == 1:
            if news_result_data[0].find('main-') == -1:
                print 'no_main'
            print ''

        del news_result_data[0]
        for item in news_result_data:
            command(item)

def walkFile(file_path):
    objdump_file_name = './objdump.txt'
    with open(objdump_file_name, 'a+') as obj_f:
        for root, dirs, files in os.walk(file_path):
            for f in files:
                m=re.findall(r'(.+?)\.o',f)
                if m:
                    status, output = commands.getstatusoutput("objdump  -drw " + os.path.join(root, f) + " |grep -w call")
                    if status == 0:
                        obj_f.write('file_name:' + os.path.join(root, f))
                        obj_f.write('\n')
                        obj_f.write(output)
                        obj_f.write('\n')

if __name__ == '__main__':
    with open('./method_names.txt', 'r') as f:
        method_names = f.readlines()

    walkFile("项目文件所在目录")

    for method_name in method_names:
        method_name = method_name.strip("\n")
        print 'start ' + method_name
        command(method_name)
        print 'end ' + method_name
        print '\n'

    for item in sorted(base_file_name):
        print "['" + item + "',", "'" + base_file_name[item] + "']"