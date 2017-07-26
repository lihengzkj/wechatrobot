#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
Created on Jul 12, 2017

@author: kejingzuo
'''

import itchat  
import logging; logging.basicConfig(level=logging.INFO)

        
def login_callback_func(): 
    logging.info('already login ...')
       
def exit_callback_func(): 
    print('already logout ...')
    logging.info('already logout ...')
 

def wechat_auto_login(uuidValue):
    try: 
        picPath = '././static/img/QR%s.png' % uuidValue
        logging.info('The pic path is -> %s' % picPath)
        itchat.auto_login(picDir=picPath,loginCallback=login_callback_func, exitCallback=exit_callback_func)
        logging.info('--> login --> waiting --> auto run --> ...')
        itchat.run(blockThread = False)
    except Exception as e:
        logging.exception(e)

def wechat_robot_logout():
    logging.info(' >>  call logout methond to logout')
    itchat.logout()

@itchat.msg_register(itchat.content.TEXT)
def text_reply(msg):
    fmsg = msg['Text'].decode('ascii').encode('utf-8')
    logging.info('Receive message %s' % fmsg)
    return msg['Text']

