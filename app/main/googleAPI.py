'''
Created on Jul 20, 2017

@author: kejingzuo
'''
import io, subprocess, sys 
from googleapiclient.discovery import build
from gtts import gTTS
import base64


##########################################################
##########################################################
##########################################################
#########      Google API start      #####################
##########################################################
##########################################################
########################################################## 
apikey = 'xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx'
#Below is for GCP Language Tranlation API
vservice = build('vision','v1',developerKey=apikey,cache_discovery=False)
service = build('translate', 'v2', developerKey=apikey,cache_discovery=False) 
speech_service = build('speech', 'v1', developerKey=apikey,cache_discovery=False)


# Pass the image data to an encoding function 把图片文件转换为base64编码格式
def encode_image(image_file):
    with open(image_file,'rb') as image_file:
        image_content = image_file.read()
    return base64.b64encode(image_content).decode('UTF-8')

def encode_audio(audio_file):
    with io.open(audio_file,'rb') as audio_file:
        audio_content = audio_file.read()
        return base64.b64encode(audio_content).decode('UTF-8')

#机器智能API接口控制参数 (Define control parameters for API)
#control parameter for Image API:
parm_image_maxResults = 10 # max objects or faces to be extracted from image analysis

# control parameter for Language Translation API:
parm_translation_origin_language = 'zh' # original language in text: to be overwriten by TEXT_DETECTION
parm_translation_target_language = 'zh' # target language for translation: Chinese
# parm_speech_synthesis_language = 'zh-tw' # speech synthesis API 'text to voice' language
# parm_speech_synthesis_language = 'zh-yue' # speech synthesis API 'text to voice' language

#API control parameter for 语音转换成消息文字（Speech recognition:voice to text)
# parm_speech_recognition_language = 'en' # speech API 'voice to text' language
parm_speech_recognition_language = 'cmn-Hans-CN' # speech API 'voice to text' language

#API control parameter for 消息文字转成语音(text to voice)
parm_speech_synthesis_language = 'zh-cn' # speech synthesis API 'text to voice' language


#把文字转换成语音
def KudosData_text_to_voice(text2voice):
    # Python 2
    if sys.version_info[0] < 3: 
        tts = gTTS(text=text2voice.encode('utf-8'), lang=parm_speech_synthesis_language, slow=False)
    # Python 3
    else:
        tts = gTTS(text=text2voice, lang=parm_speech_synthesis_language, slow=False)
    text2voiceMp3Name = 'Voice_For_You.mp3'
    tts.save(text2voiceMp3Name)
    print('\n Completed: Speech synthesis API ( Text -> Voice )')
    print('Content:%s' %text2voice)
    return text2voiceMp3Name

#把语音转换为文字
#        msg.download(msg.fileName)
#        print('\nDownloaded image file name is: %s' % msg['FileName'])
#        audio_file_input = msg['FileName']
#        audio_type = ['flac','wav']
parm_runtime_env_GCP = True
def Kudocs_voice_to_text(audio_file_input, audio_type):
    audio_file_output = str(audio_file_input)+'.'+str(audio_type)
    print('audio_file_input:%s and output: %s' %(audio_file_input, audio_file_output))
    
    #conver mp3 file to target GCP audio file:
    #  remove audio_file_output if exist
    retcode = subprocess.call(['rm',audio_file_output])
    print('retcode: %s' % retcode)
    
    if parm_runtime_env_GCP: # using Datalab in Google Cloud Platform
        retcode = subprocess.call(['avconv','-i',audio_file_input,'-ac','1',audio_file_output])
    else:# using a Kudos Data Virtual Machine, or local machine
        #VM: use ffmpeg to convert audio
        retcode = subprocess.call('ffmpeg','-i',audio_file_input,'-ac','1',audio_file_output)
    
    # call GCP API 
    response = speech_service.speech().recognize(body={
        'config':{
            #'encoding': 'LINEAR16',
            #'sampleRateHertz': 16000,
            'languageCode': parm_speech_recognition_language
            },
        'audio':{
            'content': encode_audio(audio_file_output)
            }
        }).execute()
    print('Completed: Speech  recognition API ( Voice -> Text )')
    return response

#识别图像中的物体
def KudosData_LABEL_DETECTION(image_base64, API_type, maxResults):
    
    request = vservice.images().annotate(body={
        'requests': [{
                'image': {
#                     'source': {
#                         'gcs_image_uri': IMAGE
#                     }
                      "content": str(image_base64)
                },
                'features': [{
                    'type': API_type,
                    'maxResults': maxResults,
                }]
            }],
        })
    responses = request.execute(num_retries=3)
    image_analysis_reply = u'\n['+API_type+'物体识别]\n'
    
    if responses['responses'][0] != {}:
        for i in range(len(responses['responses'][0]['labelAnnotations'])):
            image_analysis_reply += responses['responses'][0]['labelAnnotations'][i]['description'] \
            + '\n( confidence ' +  str(responses['responses'][0]['labelAnnotations'][i]['score']) + ' )\n'
        else:
            image_analysis_reply += u'[ Nill 无结果 ]\n'
    return image_analysis_reply

#识别图像中的地表
def KudosData_LANDMARK_DETECTION(image_base64, API_type, maxResults):
    request = vservice.images().annotate(body={
        'requests': [{
                'image': {
#                     'source': {
#                         'gcs_image_uri': IMAGE
#                     }
                      "content": str(image_base64)
                },
                'features': [{
                    'type': API_type,
                    'maxResults': maxResults,
                }]
            }],
        })
    responses = request.execute(num_retries=3)
    image_analysis_reply = u'\n[ ' + API_type + u' 地标识别 ]\n'
    # 'LANDMARK_DETECTION'
    if responses['responses'][0] != {}:
        for i in range(len(responses['responses'][0]['landmarkAnnotations'])):
            image_analysis_reply += responses['responses'][0]['landmarkAnnotations'][i]['description'] \
            + '\n( confidence ' +  str(responses['responses'][0]['landmarkAnnotations'][i]['score']) + ' )\n'
    else:
        image_analysis_reply += u'[ Nill 无结果 ]\n'
        
    return image_analysis_reply

#识别图像中的商标名
def KudosData_LOGO_DETECTION(image_base64, API_type, maxResults):
    request = vservice.images().annotate(body={
        'requests': [{
                'image': {
#                     'source': {
#                         'gcs_image_uri': IMAGE
#                     }
                      "content": str(image_base64)
                },
                'features': [{
                    'type': API_type,
                    'maxResults': maxResults,
                }]
            }],
        })
    responses = request.execute(num_retries=3)
    image_analysis_reply = u'\n[ ' + API_type + u' 商标识别 ]\n'
    # 'LOGO_DETECTION'
    if responses['responses'][0] != {}:
        for i in range(len(responses['responses'][0]['logoAnnotations'])):
            image_analysis_reply += responses['responses'][0]['logoAnnotations'][i]['description'] \
            + '\n( confidence ' +  str(responses['responses'][0]['logoAnnotations'][i]['score']) + ' )\n'
    else:
        image_analysis_reply += u'[ Nill 无结果 ]\n'
        
    return image_analysis_reply

#识别图片中的文字
def KudosData_TEXT_DETECTION(image_base64, API_type, maxResults):
    request = vservice.images().annotate(body={
        'requests': [{
                'image': {
#                     'source': {
#                         'gcs_image_uri': IMAGE
#                     }
                      "content": str(image_base64)
                },
                'features': [{
                    'type': API_type,
                    'maxResults': maxResults,
                }]
            }],
        })
    responses = request.execute(num_retries=3)
    image_analysis_reply = u'\n[ ' + API_type + u' 文字提取 ]\n'
    # 'TEXT_DETECTION'
    if responses['responses'][0] != {}:
        image_analysis_reply += u'----- Start Original Text -----\n'
        image_analysis_reply += u'( Original Language 原文: ' + responses['responses'][0]['textAnnotations'][0]['locale'] \
        + ' )\n'        
        image_analysis_reply += responses['responses'][0]['textAnnotations'][0]['description'] + '----- End Original Text -----\n'

        ##############################################################################################################
        #                                        translation of detected text                                        #
        ##############################################################################################################
        parm_translation_origin_language = responses['responses'][0]['textAnnotations'][0]['locale']
        # Call translation if parm_translation_origin_language is not parm_translation_target_language
        if parm_translation_origin_language != parm_translation_target_language:
            inputs=[responses['responses'][0]['textAnnotations'][0]['description']] # TEXT_DETECTION OCR results only
            outputs = service.translations().list(source=parm_translation_origin_language, 
                                                  target=parm_translation_target_language, q=inputs).execute()
            image_analysis_reply += u'\n----- Start Translation -----\n'
            image_analysis_reply += u'( Target Language 译文: ' + parm_translation_target_language + ' )\n'
            image_analysis_reply += outputs['translations'][0]['translatedText'] + '\n' + '----- End Translation -----\n'
            print('Compeleted: Translation    API ...')
        ##############################################################################################################
    else:
        image_analysis_reply += u'[ Nill 无结果 ]\n'
        
    return image_analysis_reply

#基于人脸的表情来识别喜怒哀乐等情绪 (Identify sentiment and emotion from human face)
def KudosData_FACE_DETECTION(image_base64, API_type, maxResults):
    request = vservice.images().annotate(body={
        'requests': [{
                'image': {
#                     'source': {
#                         'gcs_image_uri': IMAGE
#                     }
                      "content": str(image_base64)
                },
                'features': [{
                    'type': API_type,
                    'maxResults': maxResults,
                }]
            }],
        })
    responses = request.execute(num_retries=3)
    image_analysis_reply = u'\n[ ' + API_type + u' 面部表情 ]\n'
    # 'FACE_DETECTION'
    if responses['responses'][0] != {}:
        for i in range(len(responses['responses'][0]['faceAnnotations'])):
            image_analysis_reply += u'----- No.' + str(i+1) + ' Face -----\n'
            
            image_analysis_reply += u'>>> Joy 喜悦: \n' \
            + responses['responses'][0]['faceAnnotations'][i][u'joyLikelihood'] + '\n'
            
            image_analysis_reply += u'>>> Anger 愤怒: \n' \
            + responses['responses'][0]['faceAnnotations'][i][u'angerLikelihood'] + '\n'
            
            image_analysis_reply += u'>>> Sorrow 悲伤: \n' \
            + responses['responses'][0]['faceAnnotations'][i][u'sorrowLikelihood'] + '\n'
            
            image_analysis_reply += u'>>> Surprise 惊奇: \n' \
            + responses['responses'][0]['faceAnnotations'][i][u'surpriseLikelihood'] + '\n'
            
            image_analysis_reply += u'>>> Headwear 头饰: \n' \
            + responses['responses'][0]['faceAnnotations'][i][u'headwearLikelihood'] + '\n'
            
            image_analysis_reply += u'>>> Blurred 模糊: \n' \
            + responses['responses'][0]['faceAnnotations'][i][u'blurredLikelihood'] + '\n'
            
            image_analysis_reply += u'>>> UnderExposed 欠曝光: \n' \
            + responses['responses'][0]['faceAnnotations'][i][u'underExposedLikelihood'] + '\n'
    else:
        image_analysis_reply += u'[ Nill 无结果 ]\n'
            
    return image_analysis_reply

#不良内容识别 (Explicit Content Detection)

def KudosData_SAFE_SEARCH_DETECTION(image_base64, API_type, maxResults):
    request = vservice.images().annotate(body={
        'requests': [{
                'image': {
#                     'source': {
#                         'gcs_image_uri': IMAGE
#                     }
                      "content": str(image_base64)
                },
                'features': [{
                    'type': API_type,
                    'maxResults': maxResults,
                }]
            }],
        })
    responses = request.execute(num_retries=3)
    image_analysis_reply = u'\n[ ' + API_type + u' 不良内容 ]\n'
    # 'SAFE_SEARCH_DETECTION'
    if responses['responses'][0] != {}:
        image_analysis_reply += u'>>> Adult 成人: \n' + responses['responses'][0]['safeSearchAnnotation'][u'adult'] + '\n'
        image_analysis_reply += u'>>> Violence 暴力: \n' + responses['responses'][0]['safeSearchAnnotation'][u'violence'] + '\n'
        image_analysis_reply += u'>>> Spoof 欺骗: \n' + responses['responses'][0]['safeSearchAnnotation'][u'spoof'] + '\n'
        image_analysis_reply += u'>>> Medical 医疗: \n' + responses['responses'][0]['safeSearchAnnotation'][u'medical'] + '\n'
    else:
        image_analysis_reply += u'[ Nill 无结果 ]\n'
    return image_analysis_reply

# 翻译功能，英文翻译为中文
def KudosData_text_translation(text,source_lanauage, target_language):
    #vservice = build('translate', 'v2', developerKey=apikey)
    response = service.translations().list(
            q=text,
            source=source_lanauage,
            target=target_language,
            format='text'
        ).execute()
    #responses = request.execute(num_retries=3)
    # 'SAFE_SEARCH_DETECTION'
    #print(response)
    return response['translations'][0]['translatedText']

##########################################################
##########################################################
##########################################################
#########      Google API end      #######################
##########################################################
##########################################################
##########################################################

