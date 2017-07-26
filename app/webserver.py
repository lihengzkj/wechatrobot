#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Jul 12, 2017

@author: kejingzuo
'''

import logging; logging.basicConfig(level=logging.INFO)
import json
from flask import Flask
from flask import request,render_template,session,redirect
import threading
from main import robot, robotdb,robotclass
import sys
import itchat
import uuid
logging.info('>>>>>>>>>>> the default encoding is %s' % sys.getdefaultencoding())

robotsDir = {}
application = Flask(__name__)
application.secret_key = 'i cannot guesss what the key is'

@application.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['pwd']
    usercount = robotdb.getUserCount(username,password)
    if usercount == 1:
        session['user'] = username
        #robotdb.turnOffTheRobotByUserName(username)
        return redirect('/')
    else:
        render_template('login.html',msg='User NOT exist, pls register first or login by other user')
        
@application.route('/userlist', methods=['GET','POST'])
def toUserList():
    if 'user' in session: 
        user_name = session['user']
        if user_name == 'admin': #这里的user_name可以是自定义的，但是数据库中需要存在
            userlist = robotdb.getAllUser()
            if userlist != None:
                #userlist_json = json.dumps(userlist)
                return render_template('robotuserlist.html',userlist=userlist)
    return render_template('login.html',msg='Session Invalid')
        
@application.route('/deleteuser', methods=['GET'])
def deleteUser():
    user_name = session['user']
    if user_name == 'admin':#这里的user_name可以是自定义的，但是数据库中需要存在
        user_id = request.args.get('user_id',None)
        if user_id != None:
            robotdb.deleteUser(user_id)
    return redirect('/userlist')

@application.route('/adduser', methods=['POST'])
def addRotoUser():
    username = request.form.get("username", type=str, default=None)
    password = request.form.get("pwd", type=str, default=None)
    logging.info(' >>>>>  Add user {%s,%s}' %(username,password))
    if username != None and password!= None:
        robotdb.addUser(username,password)
    return redirect('/userlist')
        

    
@application.route('/', methods=['GET', 'POST'])
def home(): 
    if 'user' in session:
        logging.info('User %s is alredy login, turn to the home page.' % session['user'])
        user_name = session['user'] 
        robotIns =  robotdb.searchRobotByUserName(user_name)
        if robotIns != None:
            robotInfo = robotIns[0]
            logging.info('Robot info from db is:uuid=%s, name=%s, status=%s' % (robotInfo[0],robotInfo[1],robotInfo[2])) 
            #targetRobot = robotsDir.get(user_name)
            #if targetRobot!= None:
            #   targetRobot.log_out()
            return render_template('home.html',uuid=robotInfo[0],robot_user=robotInfo[1], status=robotInfo[2])
        else:
            #session.pop('user', None) 
            logging.warn('User %s is in session, but DOT have robot in db.' % user_name) 
            return render_template('home.html',uuid=None,robot_user=user_name, status='OFF')
    else:
        return render_template('login.html')
    
@application.route('/stoprobot', methods=['POST'])
def stop_robot():
    user_name = session['user']
    logging.info('Current user is %s when stop the robot.' % user_name)
    targetRobot = robotsDir.get(user_name)
    #session.pop('user', None)
    robotdb.turnOffTheRobotByUserName(user_name)
    if targetRobot!= None: 
        targetRobot.log_out()
        logging.info('Robot already stop:%s' % user_name)
        #return render_template('login.html',msg='You stop the robot, Please login again.')
    else:
        logging.info("Current robot %s is not existing, when stop it."  % user_name)
        #return render_template('login.html',msg='Current robot %s is not existing, Please login again.' % user_name)
    return redirect('/')

@application.route('/startrobot', methods=['POST'])
def start_robot():
    user_name = session['user']
    logging.info('Current user is %s when start the robot.' % user_name)
        
    uuidValue = uuid.uuid1() 
    logging.info('>>>>>  %s will start a robot,QR uuid is %s' % (user_name,uuidValue))
    
    #根据user_name获取机器人的数量
    robotcount = robotdb.searchRobotCountByUserName(user_name)
    #当数量为1的时候，说明机器人已经存在，只需要开启
    if robotcount > 0:
        robotdb.updateUUIDByUserName(uuidValue,user_name,'WAIT')
    #当没有发现机器人的时候，直接插入数据库一个机器人，并设置状态为开启 
    else:
        robotdb.insertRobotRecord(uuidValue,user_name,'WAIT')
    
    threading.Thread(target=runRobot,args=((str(uuidValue),user_name)), name='RobotThread').start()
    
    #return render_template('startok.html',robotstatus='OFF',tag=uuidValue,msg='Robot is starting!')
    return redirect('/')
    #return render_template('home.html',uuid=str(uuidValue),robot_user=user_name, status='WAIT_END')

def getRobotByName(user_name):
    targetRobot = robotsDir.get(user_name)
    if targetRobot == None:
        netInstance = itchat.new_instance()
        targetRobot = robotclass.RobotMachine(netInstance,user_name)
        robotsDir[user_name]=targetRobot
    else:
        targetRobot.log_out()
    return targetRobot

def runRobot(uuidValue,user_name):
    targetRobot = getRobotByName(user_name)  
    logging.info('target robot type is %s' % type(targetRobot))
    picPath = '././static/img/QR%s.png' % uuidValue
    logging.info('The pic path is -> %s' % picPath)
    targetRobot.auto_run(uuidValue)
    
    #robot.wechat_auto_login(uuidValue)
        
@application.route('/logout', methods=['GET'])
def logout():
    if 'user' in session:
        user_name = session['user']
        session.pop('user', None)
    targetRobot = robotsDir.get(user_name)
    if targetRobot!= None: 
        targetRobot.log_out()
    return render_template('login.html')

def runServer():
    application.run(host='0.0.0.0', port=8080)

if __name__ == '__main__':
    #t1 = threading.Thread(target=runRobot, name='RobotThread')
    #t2 = threading.Thread(target=runServer, name='HttpServerThread')

    #t2.start()
    #t1.start()
    runServer()


