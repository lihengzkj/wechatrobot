#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Jul 17, 2017

@author: kejingzuo
''' 
'''
create table robot_records(uuid varchar(200) primary key,robot_user varchar(100) not null, robot_status varchar(5) not null)
create table robot_user(
    user_id INT UNSIGNED AUTO_INCREMENT,
    user_name varchar(200) not null,
    user_pwd varchar(200) not null,
    PRIMARY KEY ( user_id )
)
'''

import logging; logging.basicConfig(level=logging.INFO)
import mysql.connector

def getConnection():
    return mysql.connector.connect(user='root', password='robotadmin', database='robotdb', host='172.17.0.4')

def getAllUser():
    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute("select b.user_id,b.user_name,ifnull(a.robot_status,'OFF') from robot_user b left join robot_records a on a.robot_user = b.user_name order by b.user_id;")
        results = cursor.fetchall()
        count = len(results)
        #conn.commit()
        logging.info('Search all user and search count is %s' % count)
        
        conn.close()
        if count == 0:
            return None
        else:
            return results
    except Exception as e:
        logging.info(e)
    finally:
        conn.close()
    return None
def deleteUser(user_id):
    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute('delete from robot_user where user_id = %s ', [user_id])
        count = cursor.rowcount
        conn.commit()
        logging.info('Delete %s user success, delete count -> %s' % ( user_id,count))
        conn.close()
        return count
    except Exception as e:
        logging.info(e)
    finally:
        conn.close()
    return 0
def addUser(user_name,user_pwd):
    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute('insert into robot_user (user_name,user_pwd) values (%s,%s)', [ user_name,user_pwd])
        count = cursor.rowcount
        conn.commit()
        logging.info('Insert User [%s, %s] success, insert count -> %s' % (user_name,user_pwd,count))
        conn.close()
        return count
    except Exception as e:
        logging.info(e)
    finally:
        conn.close()
    return 0

def getUserCount(username, pwd):
    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute('select user_name from robot_user where user_name = %s and user_pwd = %s', [username,pwd])
        #count = cursor.rowcount 
        count = len(cursor.fetchall())
        logging.info('Search record username: %s password: %s search count: %s' % (username,pwd,count))
        conn.close()
        return count
    except Exception as e:
        logging.info(e)
    finally:
        conn.close()
    return 0

def insertRobotRecord(uuidValue,user_name,robot_status):
    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute('insert into robot_records (uuid, robot_user,robot_status) values (%s, %s,%s)', [str(uuidValue), user_name,robot_status])
        count = cursor.rowcount
        conn.commit()
        logging.info('Insert record [%s, %s, %s] success, insert count -> %s' % (uuidValue, user_name,robot_status,count))
        conn.close()
        return count
    except Exception as e:
        logging.info(e)
    finally:
        conn.close()
    return 0
        
def updateRobotRecord(uuidValue,username):
    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute('update robot_records set uuid = %s where robot_user = %s ', [str(uuidValue), username])
        count = cursor.rowcount
        conn.commit()
        logging.info('Update record username %s and uuid %s and update count is %s' % (username,uuidValue,count))
        conn.close()
        return count
    except Exception as e:
        logging.info(e)
    finally:
        conn.close()
    return 0

def turnOnTheRobotByUserName(username):
    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute('update robot_records set robot_status = %s where robot_user = %s ', ['ON', username])
        count = cursor.rowcount
        conn.commit()
        logging.info('Turn on the %s robot, result is ' % (username,count))
        conn.close()
        return count
    except Exception as e:
        logging.info(e)
    finally:
        conn.close()
    return 0

def turnOffTheRobotByUserName(username):
    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute('update robot_records set robot_status = %s where robot_user = %s ', ['OFF', username])
        count = cursor.rowcount
        conn.commit()
        logging.info('Turn on the %s robot, result is ' % (username,count))
        conn.close()
        return count
    except Exception as e:
        logging.info(e)
    finally:
        conn.close()
    return 0

def turnWaitTheRobotByUserName(username):
    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute('update robot_records set robot_status = %s where robot_user = %s ', ['WAIT', username])
        count = cursor.rowcount
        conn.commit()
        logging.info('Turn WAIT the %s robot, result is ' % (username,count))
        conn.close()
        return count
    except Exception as e:
        logging.info(e)
    finally:
        conn.close()
    return 0

def updateUUIDByUserName(uuidValue,username,rstatus):
    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute('update robot_records set uuid = %s , robot_status = %s where robot_user = %s ', [str(uuidValue),rstatus,username])
        count = cursor.rowcount
        conn.commit()
        logging.info('Update record uuid %s and username %s , update count: %s' % (uuidValue,username,count))
        conn.close()
        return count
    except Exception as e:
        logging.info(e)
    finally:
        conn.close()
    return 0

def searchRobotCountByUserName(username):
    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute('select uuid, robot_user,robot_status from robot_records where robot_user = %s ', [username])
        #count = cursor.rowcount 
        count = len(cursor.fetchall())
        logging.info('Search record username %s and search count: %s' % (username,count))
        conn.close()
        return count
    except Exception as e:
        logging.info(e)
    finally:
        conn.close()
    return 0

def searchRobotByUserName(username):
    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute('select uuid, robot_user,robot_status from robot_records where robot_user = %s ', [username])
        results = cursor.fetchall()
        count = len(results)
        #conn.commit()
        logging.info('Search record by username %s and search count is %s' % (username,count))
        
        conn.close()
        if count == 0:
            return None
        else:
            return results
    except Exception as e:
        logging.info(e)
    finally:
        conn.close()
    return None

def deleteRobotByUUID(user_name):
    try:
        conn = getConnection()
        cursor = conn.cursor()
        cursor.execute('delete from robot_records where robot_user = %s ', [user_name])
        count = cursor.rowcount
        conn.commit()
        logging.info('Delete %s robot success, delete count -> %s' % ( user_name,count))
        conn.close()
        return count
    except Exception as e:
        logging.info(e)
    finally:
        conn.close()
    return 0
