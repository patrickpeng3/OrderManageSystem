#! /usr/bin/env python3
# -*- coding:utf-8 -*-

import pymysql
import pymysql.cursors
import time
import datetime
import sys
import getpass

class autoRun(object):
    def __init__(self):
        #判断参数个数
        if len(sys.argv) != 3:
            sys.exit("第一个参数为服务器id！请确认后重试！")
        dbName = sys.argv[2]
        #游戏服数据库
        self.db = pymysql.connect(
            host = '127.0.0.1',
            user='root',
            password='dkmwebmysql!q$EWQ23FD23',
            db=dbName,
            port=3306,
            charset='utf8')
        self.cursor = self.db.cursor()
        # password = getpass.getpass("密码:");

    def main(self):
        # self.testDb()
        self.outfile()

    #测试方法
    def testDb(self):
        self.cursor.execute("SELECT VERSION()")
        data = self.cursor.fetchone()
        print ("游戏数据库版本 : %s " % data)

        self.cursor.execute("SELECT VERSION()")
        data2 = self.cursor.fetchone()
        print ("后台数据库版本 : %s " % data2)
        sys.exit('dddddd')
        t = int(time.time())
        print(sys.argv)
        # data1 =self.cursor.execute("SELECT * from log_xunbao into outfile '/data/db_bak/test_" + str(t) + ".csv'")

        # print(str(data1))

    #导出游戏服log数据库
    def outfile(self):

        serverId = sys.argv[1]
        date = time.strftime("%Y-%m-%d", time.localtime())
        list = [
            "SELECT * FROM log_role_update into outfile '/data/db_bak/log_role_update_" + date + "_" + serverId + r".csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';",
            "SELECT * FROM log_role_daydata into outfile '/data/db_bak/log_role_daydata_" + date + "_" + serverId + r".csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';",
            "SELECT server_id,channel,platform,role_id,role_name,order_id,diamond,udpate_time FROM log_recharge into outfile '/data/db_bak/log_recharge_" + date + "_" + serverId + r".csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';",
            "SELECT date_time,server_id,account_id,char_name,item_id,type,number,surplus,sgin,flag FROM log_item WHERE  DateDiff(date_time,NOW())>-2  into outfile '/data/db_bak/log_item_" + date + "_" + serverId + r".csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';",
            # "SELECT server_id,channel,platform,role_id,act_type,second_type,update_time FROM log_open_act_second  where DateDiff(update_time,NOW())>-2  into outfile  '/data/db_bak/log_open_act_second_" + date + "_" + serverId + r".csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';",
            "SELECT date_time,server_id,pid,char_name,diamond_surplus,sgin,flag,type,number FROM log_diamond_surplus  where DateDiff(date_time,NOW())>-2  into outfile '/data/db_bak/log_diamond_surplus_" + date + "_" + serverId + r".csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';",
            "SELECT server_id,role_id,operate_type,char_name,buy_id,buy_name,diamond_dle,diamond_surplus,date_time FROM log_propmall  where DateDiff(date_time,NOW())>-2  into outfile '/data/db_bak/log_propmall_" + date + "_" + serverId + r".csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';",
            "SELECT role_id,role_name,role_type,server_id,level,update_time FROM log_role_level  where DateDiff(update_time,NOW())>-2  into outfile '/data/db_bak/log_role_level_" + date + "_" + serverId + r".csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';",
            "SELECT num,date_time FROM log_online_num  where DateDiff(date_time,NOW())>-2  into outfile '/data/db_bak/log_online_num_" + date + "_" + serverId + r".csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';",
            # "SELECT server_id,role_id,operate_type,char_name,xunbao_type,reward_item,diamond_dle,diamond_surplus,date_time FROM log_xunbao  where DateDiff(date_time,NOW())>-4  into outfile '/data/db_bak/log_xunbao_" + date + "_" + serverId + r".csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';",
            "SELECT server_id,channel,platform,role_id,role_name,level,copy_id,copy_type,boss_id,operate_type,end_type,update_time FROM log_copy  where DateDiff(update_time,NOW())>-8  into outfile '/data/db_bak/log_copy_" + date + "_" + serverId + r".csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';",
            "SELECT role_id,role_name,role_type,uid,server_id,channel,platform,level,evolution,login_time,logout_time,newbie_id,barrier,update_time FROM log_role_login  where DateDiff(update_time,NOW())>-181  into outfile '/data/db_bak/log_role_login_" + date + "_" + serverId + r".csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';",
            "SELECT role_id,role_name,role_type,uid,server_id,channel,platform,update_time FROM log_role_create  where DateDiff(update_time,NOW())>-181  into outfile '/data/db_bak/log_role_create_" + date + "_" + serverId + r".csv' FIELDS TERMINATED BY ',' LINES TERMINATED BY '\n';"
        ]
        fo = open("/tmp/php_merge_outfile.log", "w")
        for i in list:
            print(i+'\n')
            fo.write(i+'\n')

        for i in list:
            self.cursor.execute(i)
        print('mysql data is outfile')

if __name__ == '__main__':
    autoRun().main()
