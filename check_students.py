#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys
import os
import urllib.request
import urllib.parse

url_prefix="."

class Student:
    _file_header_str=\
"""<html><head>
    <meta http-equiv="content-type" content="text/html; charset=UTF-8">
</head>
<body>
<h1> %s </h1>

"""

    _task_header_str=\
"""
<h2> %s </h2>
            
<table border="1">
<tr> 
    <td> (контест) авторcкие run id : время </td>
    <td> похожий студент </td>
    <td> (контест) чужие run id : время</td>
    <td> разница (размер) </td>
</tr>

"""

    def __init__(self,full_name= None):
        self.full_name = full_name
        self.tasks = dict()

    def print_to_html(self):
        """
        Create new html file with full_name as pattern
        """
        if len(self.tasks) == 0:
            print ("For student '%s' there nothing to write" % (self.full_name))
            return

        file_name = "stud_%s.html" % (self.full_name.replace(" ","_"))
        f=open(file_name,"w")

        f.write( self._file_header_str % (self.full_name))
        
        for task_name , matches in self.tasks.items():
            f.write(self._task_header_str % (task_name))

            matches.sort()
            for match in matches:
                match.print_to_html(f)


            f.write("</table>\n\n")

        f.write("</body></html>")
        f.close()    

class matching:
    
    _html_print_str=\
            """
    <tr><td> (%s) %s : %s </td><td> %s <td> (%s) %s : %s </td><td> <a href="%s"> diff </a> (size: %d) </td></tr>
"""

    def __init__(self):
        self.student_contest_id = "wrong"
        self.student_run_id     = "wrong"
        self.student_datetime   = "wrong"
        self.other_contest_id   = "wrong"
        self.other_run_id       = "wrong"
        self.other_datetime     = "wrong"
        self.other_student_name = "wrong"
        self.similarity         = -1
        self.diff_url           = ""
       
    def __lt__(self,right):
        return self.similarity < right.similarity

    def print_to_html(self,f):
        f.write(self._html_print_str % ( 
            self.student_contest_id, 
            self.student_run_id,
            self.student_datetime,
            self.other_student_name,
            self.other_contest_id,
            self.other_run_id,
            self.other_datetime,
            "%s/%s" % (url_prefix, self.diff_url),
            self.similarity))

def process_task(stream, students):
    task_name="unknown"

    for line in stream:
        line=line.decode('utf8')
        index=line.find('<h1>')
        if index == -1:
            continue
        task_name=line[index+4:-6] # len </h1>
        break
     
    for line in stream:
        line=line.decode('utf8')

        for student in students:
            if line.find(student.full_name) == -1:
                continue
            
            student_matching = matching()

            items=line.split("</td><td>")
            diff_url = items[-1][9:-21]
            if diff_url == "&nbsp;":
                continue
            student_matching.diff_url=diff_url
            
            if items[2].find(student.full_name) != -1:
                student_matching.student_contest_id = items[0][8:]
                student_matching.student_run_id     = items[1]
                student_matching.student_datetime   = items[3]
                student_matching.other_contest_id   = items[4]
                student_matching.other_run_id       = items[5]
                student_matching.other_datetime     = items[7]
                student_matching.other_student_name = items[6]
            else:
                student_matching.student_contest_id = items[4]
                student_matching.student_run_id     = items[5]
                student_matching.student_datetime   = items[7]
                student_matching.other_contest_id   = items[0][8:]
                student_matching.other_run_id       = items[1]
                student_matching.other_datetime     = items[3]
                student_matching.other_student_name = items[2]
            
            student_matching.similarity = int(items[8])
            
            if task_name in student.tasks:
                student.tasks[task_name].append(student_matching)
            else:
                student.tasks[task_name] = [ student_matching ] # build new list 

    return    

def create_file_list(url):
    """
    Parse url and get list of plagiarism for all tasks
    ejudge contest
    """

    f=urllib.request.urlopen(url)
    url_lst=list()
    for file_line in f:
        file_line=file_line.decode('utf8')
        index=file_line.find('List')
        if index == -1:
            continue
        l=file_line.rfind("href=",0,index)
        url_lst.append("%s" % (file_line[l+6:index-2]))
    f.close()

    return url_lst

def main(args):

    url= "https://ejudge.ru/MW6Z8TtquR1gBORo/index.html"
    url_prefix=url[0:url.rfind('/')]
    
    file_list = create_file_list(url)
    print(file_list)

    students=list()
    stud = Student(full_name="Тараканов Игорь")
    students.append(stud)
    stud=Student(full_name="Косач (Мовтян) Денис")
    students.append(stud)

    for task_file in  file_list:
        f=urllib.request.urlopen("%s/%s" % (url_prefix, task_file) )
        process_task(f,students)
        f.close()

    for student in students:
        student.print_to_html()


    return 100

    if len(args) < 2:
        print("Bad number of arguments: student directory")
        return 1

    path = args[2]
    student = args[1]
    
    files=os.listdir(path)
    path += "/"
    

    for file_name in files:
        #print(file_name)
        if file_name[-6:] == "l.html":
            process(file_name,student,path+file_name)
    
    print("</table></body></html>")

    return 0

                       
if __name__ == "__main__":
    sys.exit(main(sys.argv))

