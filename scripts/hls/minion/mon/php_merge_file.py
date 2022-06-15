#! /usr/bin/env python3
# -*- coding:utf-8 -*-

# A8日志合服处理

import pymysql
import pymysql.cursors
import time
import datetime
import sys

class autoRun(object):
    def __init__(self):
        dbName = sys.argv[2]
        self.db = pymysql.connect(
            host = '127.0.0.1',
            user='root',
            password='dkmwebmysql!q$EWQ23FD23',
            db=dbName,
            port=3306,
            local_infile=1,
            charset='utf8')
        # self.db = pymysql.connect(
        #     host = '192.168.10.138',
        #     user='xxx',
        #     password='123456',
        #     db='test',
        #     port=3306,
        #     charset='utf8')
        self.db.autocommit(1)
        self.cursor = self.db.cursor()

    def main(self):
        # self.testDb()
        self.loadfile()

    #测试方法
    def testDb(self):
        self.cursor.execute("SELECT VERSION()")
        data = self.cursor.fetchone()
        print ("Database version : %s " % data)
        t = int(time.time())
        data1 =self.cursor.execute("SELECT * from log_xunbao into outfile '/data/db_bak/test_" + str(t) + ".csv'")
        print(str(data1))

    #导出游戏服log数据库
    def loadfile(self):
        #判断参数个数
        serverId = sys.argv[1]
        date = time.strftime("%Y-%m-%d", time.localtime())
        list = [
            r"load data local infile '/data/db_bak/log_role_update_" + date + "_" + serverId + r".csv' into table log_role_update fields terminated by ',' lines TERMINATED BY '\n' ;",
            r"load data local infile '/data/db_bak/log_role_daydata_" + date + "_" + serverId + r".csv' into table log_role_daydata fields terminated by ',' lines TERMINATED BY '\n' ;",
            r"load data local infile '/data/db_bak/log_recharge_" + date + "_" + serverId + r".csv' into table log_recharge fields terminated by ',' lines TERMINATED BY '\n' (server_id,channel,platform,role_id,role_name,order_id,diamond,udpate_time);",
            r"load data local infile '/data/db_bak/log_item_" + date + "_" + serverId + r".csv' into table log_item fields terminated by ',' lines TERMINATED BY '\n' (date_time,server_id,account_id,char_name,item_id,type,number,surplus,sgin,flag);",
            # r"load data local infile '/data/db_bak/log_open_act_second_" + date + "_" + serverId + r".csv' into table log_open_act_second fields terminated by ',' lines TERMINATED BY '\n' (server_id,channel,platform,role_id,act_type,second_type,update_time);",
            r"load data local infile '/data/db_bak/log_diamond_surplus_" + date + "_" + serverId + r".csv' into table log_diamond_surplus fields terminated by ',' lines TERMINATED BY '\n' (date_time,server_id,pid,char_name,diamond_surplus,sgin,flag,type,number);",
            r"load data local infile '/data/db_bak/log_propmall_" + date + "_" + serverId + r".csv' into table log_propmall fields terminated by ',' lines TERMINATED BY '\n' (server_id,role_id,operate_type,char_name,buy_id,buy_name,diamond_dle,diamond_surplus,date_time);",
            r"load data local infile '/data/db_bak/log_role_level_" + date + "_" + serverId + r".csv' into table log_role_level fields terminated by ',' lines TERMINATED BY '\n' (role_id,role_name,role_type,server_id,level,update_time);",
            r"load data local infile '/data/db_bak/log_online_num_" + date + "_" + serverId + r".csv' into table log_online_num fields terminated by ',' lines TERMINATED BY '\n' ( num,date_time );",
            # r"load data local infile '/data/db_bak/log_xunbao_" + date + "_" + serverId + r".csv' into table log_xunbao fields terminated by ',' lines TERMINATED BY '\n' ( server_id,role_id,operate_type,char_name,xunbao_type,reward_item,diamond_dle,diamond_surplus,date_time );",
            r"load data local infile '/data/db_bak/log_copy_" + date + "_" + serverId + r".csv' into table log_copy fields terminated by ',' lines TERMINATED BY '\n' (server_id,channel,platform,role_id,role_name,level,copy_id,copy_type,boss_id,operate_type,end_type,update_time);",
            r"load data local infile '/data/db_bak/log_role_login_" + date + "_" + serverId + r".csv' into table log_role_login fields terminated by ',' lines TERMINATED BY '\n' (role_id,role_name,role_type,uid,server_id,channel,platform,level,evolution,login_time,logout_time,newbie_id,barrier,update_time);",
            r"load data local infile '/data/db_bak/log_role_create_" + date + "_" + serverId + r".csv' into table log_role_create fields terminated by ',' lines TERMINATED BY '\n' (role_id,role_name,role_type,uid,server_id,channel,platform,update_time);"
        ]
        fo = open("/tmp/php_merge_loadfile.log", "w")
        for i in list:
            fo.write(i + '\n')

        for i in list:
            print(i)
            self.cursor.execute(i)
        print('mysql  is merge ok')

if __name__ == '__main__':
    autoRun().main()

