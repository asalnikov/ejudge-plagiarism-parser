#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os

def process(file_name, student, path):
    f=open(path,"r")
    for line in f:
        if line.find(student) == -1:
            continue
        items=line.split("</td><td>")
        
        diff_url = items[-1][:-11]
        if diff_url == "&nbsp;":
            continue

        
        student_run_id="wrong"
        student_datetime="wrong"
        other_run_id="wrong"
        other_datetime="wrong"
        other_student_name="wrong"

        if items[2].find(student) != -1:
            student_run_id = items[1]
            student_datetime = items[3]
            other_run_id =  items[5]
            other_datetime = items[7]
            other_student_name = items[6]
        else:
            student_run_id = items[5]
            student_datetime = items[7]
            other_run_id =  items[1]
            other_datetime = items[3]
            other_student_name = items[2]


        print("<tr><td> %s </td><td>  %s : %s </td><td> %s </td><td> %s : %s </td><td> %s </td></tr>" %
                (file_name, student_run_id, student_datetime, other_student_name, other_run_id,  other_datetime, diff_url))
    
    f.close()


def main(args):
    
    if len(args) < 2:
        print("Bad number of arguments: student directory")
        return 1

    path = args[2]
    student = args[1]
    
    files=os.listdir(path)
    path += "/"
    
    print("""<html><head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
</head>
<body>
<h1> %s </h1> 
<table>
<tr>
    <td> файл </td> 
    <td> авторcкие run id : время </td>
    <td> похожий студент </td>
    <td> чужие run id : время</td>
    <td> разница </td>
<tr>

""" % (student))

    for file_name in files:
        #print(file_name)
        if file_name[-6:] == "l.html":
            process(file_name,student,path+file_name)
    
    print("</table></body></html>")

    return 0

                       
if __name__ == "__main__":
    sys.exit(main(sys.argv))

