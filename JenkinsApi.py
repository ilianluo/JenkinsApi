# -*- coding: utf-8 -*-
import  jenkins
import  time
from settings import Jenkins_HTTP_URI, Jenkins_User, Jenkins_User_API_Token

# Jenkins_HTTP_URI =  'http://xxx.xxx.xx.xx:xxx'
# Jenkins_User = 'xxxxxx'
# Jenkins_User_API_Token = 'xxx'


def Jenkins_apply(project,tag):
    conn = jenkins.Jenkins(Jenkins_HTTP_URI, username=Jenkins_User, password=Jenkins_User_API_Token)
    ##获取最后一次 build 的 ID
    last_build_number = conn.get_job_info(project)['lastCompletedBuild']['number']
    this_build_number = last_build_number + 1
    #判断当前是否有job在执行
    if conn.get_build_info(project,last_build_number)['building'] == False:

        conn.build_job(project, parameters={'tag': tag})

        while  True:
            #判断构建是否完成,构建完成则返回最后一次构建id,和last_build_number进行判断，成功则返回日志,否则循环
            if conn.get_job_info(project)['lastCompletedBuild']['number'] == this_build_number:
                result = conn.get_build_console_output(project, this_build_number)
                break
            else:
                continue

    else:
        result =  "The latest job is still building."
    return result




if  __name__  ==  "__main__":
    Jenkins_apply("tops","20180731_v0.8.01")
