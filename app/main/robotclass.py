import itchat
from main import robotdb,googleAPI
import json, requests
from itchat.content import *
import io
import logging; logging.basicConfig(level=logging.INFO)
class RobotMachine(object):

    def __init__(self,robotInstance,user_name):
        self.robotInstance = robotInstance
        self.user_name = user_name

        @robotInstance.msg_register([TEXT,MAP,CARD,NOTE,SHARING]) 
        def text_reply(msg): 
            result = reply_by_type(msg,isGroupChat=False)
            logging.info('   text_reply   >>> nick name is %s and result: %s' % (msg.user.nickName,result)) 
            robotInstance.send_msg('%s' % result, msg['FromUserName'])
        @robotInstance.msg_register(TEXT, isGroupChat=True)
        def text_reply_inGroup(msg):
            #print(msg)
            if msg.isAt:
                result = reply_by_type(msg,isGroupChat=True)
                logging.info('   qunliao    >>> nick name is %s and result: %s' % (msg['ActualNickName'],result))
                robotInstance.send_msg(u'@%s %s' % (msg['ActualNickName'], result), msg['FromUserName'])
                
        @robotInstance.msg_register([RECORDING])
        def download_files(msg):
            result = handle_vedio(msg)
            logging.info('   audio    >>> nick name is %s and result: %s' % (msg.user.nickName,result))
            robotInstance.send_msg('%s' % result, msg['FromUserName'])
        @robotInstance.msg_register(PICTURE)
        def download_pic(msg):
            result = handle_picture(msg)
            robotInstance.send_msg('%s' % result, msg['FromUserName'])
        
    def login_callback_func(self):
        print('already login ...')
        robotdb.turnOnTheRobotByUserName(self.user_name)

    def exit_callback_func(self):
        print('already logout ...')
        robotdb.turnOffTheRobotByUserName(self.user_name)

    def wechat_auto_login(self):
        itchat.auto_login(enableCmdQR=2,loginCallback=self.login_callback_func, exitCallback=self.exit_callback_func)
        itchat.run()

    def auto_run(self,uuidValue):
        picPath = '././static/img/QR%s.png' % uuidValue
        self.robotInstance.auto_login(picDir=picPath,loginCallback=self.login_callback_func, exitCallback=self.exit_callback_func,statusStorageDir="newInstance.pkl")
        self.robotInstance.run(blockThread = False)
        #newRobotMachine.run(blockThread = False)

    def log_out(self):
        self.robotInstance.logout()
        
        
        
        
        
#调用图灵机器人的API
def tuling(info):
	apikey = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
    url = "http://www.tuling123.com/openapi/api?key=%s&info=%s"%(apikey,info)
    req = requests.get(url)
    content = req.text
    data = json.loads(content)
    answer = data['text']
    return answer
    
def handle_picture(msg):
    parm_translation_origin_language = 'zh' # will be overwriten by TEXT_DETECTION
    msg.download(msg.fileName)
    print('\nDownloaded image file name is: %s' % msg['FileName'])
    image_base64 = googleAPI.encode_image(msg['FileName'])
    if msg.user.nickName == u'晶':
        return googleAPI.KudosData_TEXT_DETECTION(image_base64, 'TEXT_DETECTION', googleAPI.parm_image_maxResults)
    else:
        
        ################### call image analysis APIs ####################
        image_analysis_reply = u'[ Image Analysis 图像分析结果 ]\n'
        # 1. LABEL_DETECTION:
        image_analysis_reply += googleAPI.KudosData_LABEL_DETECTION(image_base64, 'LABEL_DETECTION', googleAPI.parm_image_maxResults)
        # 2. LANDMARK_DETECTION:
        image_analysis_reply += googleAPI.KudosData_LANDMARK_DETECTION(image_base64, 'LANDMARK_DETECTION', googleAPI.parm_image_maxResults)
        # 3. LOGO_DETECTION:
        image_analysis_reply += googleAPI.KudosData_LOGO_DETECTION(image_base64, 'LOGO_DETECTION', googleAPI.parm_image_maxResults)
        # 4. TEXT_DETECTION:
        image_analysis_reply += googleAPI.KudosData_TEXT_DETECTION(image_base64, 'TEXT_DETECTION', googleAPI.parm_image_maxResults)
        # 5. FACE_DETECTION:
        image_analysis_reply += googleAPI.KudosData_FACE_DETECTION(image_base64, 'FACE_DETECTION', googleAPI.parm_image_maxResults)
        # 6. SAFE_SEARCH_DETECTION:
        image_analysis_reply += googleAPI.KudosData_SAFE_SEARCH_DETECTION(image_base64, 'SAFE_SEARCH_DETECTION', googleAPI.parm_image_maxResults)
    
        print('Compeleted: Image Analysis API ...result:%s' % image_analysis_reply)
        
        return image_analysis_reply

def handle_vedio(msg):
    parm_translation_origin_language = 'zh' # will be overwriten by TEXT_DETECTION
    msg.download(msg.fileName)
    print('\nDownloaded audio file name is: %s' % msg['FileName'])
    
    ##############################################################################################################
    #                                          call audio analysis APIs                                          #
    ##############################################################################################################
    
    audio_analysis_reply = u'[ Audio Analysis 音频处理结果 ]\n'

    # Voice to Text:
    audio_analysis_reply += u'\n[ Voice -> Text 语音识别 ]\n'
    response = googleAPI.Kudocs_voice_to_text(msg['FileName'], 'flac')
    print(response)
    print('---------------------------------------------------')
#     response = KudosData_voice_to_text(msg['FileName'], 'wav')
    if response != {}:
        print (response['results'][0]['alternatives'][0]['transcript'])
        print ('( confidence %f )' % response['results'][0]['alternatives'][0]['confidence'])
        audio_analysis_reply += response['results'][0]['alternatives'][0]['transcript'] + '\n'
        audio_analysis_reply += '( confidence ' + str(response['results'][0]['alternatives'][0]['confidence']) + ' )\n'
        # Translate recognised text to another language:
        parm_translation_origin_language = 'zh'
        parm_translation_target_language = 'en'
        translated_text_reply = googleAPI.KudosData_text_translation(response['results'][0]['alternatives'][0]['transcript'], 
                                                           parm_translation_origin_language, parm_translation_target_language)
        print('Translate result: %s' % translated_text_reply)
        audio_analysis_reply += translated_text_reply
        
        recognition_text = response['results'][0]['alternatives'][0]['transcript']
        audio_analysis_reply = tuling(recognition_text)
        #itchat.send('@%s %s' % (msg['FromUserName'],audio_analysis_reply), msg['FromUserName'])
    return audio_analysis_reply

def reply_by_type(msg, isGroupChat = True):
    result = 'init' 
    if u'翻译' == msg['Text'][0:2]:
        translate_content = msg['Text'][2:]
        result = googleAPI.KudosData_text_translation(translate_content,'zh','en')
    elif 'translate' == msg['Text'][0:9]:
        translate_content = msg['Text'][9:]
        result = googleAPI.KudosData_text_translation(translate_content,'en','zh')
    else: 
        result =  tuling(msg['Text'])
    
    #if isGroupChat:
        #result = '@'+msg['FromUserName']+' '+result
    return result



