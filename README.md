# wechatrobot
    本项目是基于第三方开源项目[itchat](https://github.com/littlecodersh/ItChat "itchat")搭建的。    
    主要功能是提供多个网页版的微信机器人的管理。    
    其中机器人的功能包括：自动应答各个领域的问题的功能和聊天功能：，这个功能基于[tuling](http://www.tuling123.com/ "tuling")机器人；翻译功能，提供中文翻译成英文和英文翻译成中文；图片解析功能：解析图片的内容和分析图片中的物体。翻译和分析功能是基于[Google的云端机器学习的API](https://console.cloud.google.com "Google API").这里需要注意，如果使用者需要使用这两个tuling和Google API 需要自行注册获取key.
    
### 运行环境要求
    系统要求： `Linux` `python3`   
    软件要求：   
    `pip3 install --upgrade google-api-python-client`   
        `pip3 install --upgrade urllib3 requests`   
        `pip3 install  -U gTTS`   
        `sudo apt-get install libav-tools -y`   
        `sudo apt-get install xdg-utils`   
        `sudo apt-get install desktop-file-utils`   
        

### 使用
   #### 简单使用    
    
        * 使用 git 克隆代码到Linux    
        * 替换tuling和google的key为自己的key    
        * $ python3 ./app/webserver.py    
        
   #### 复杂使用(flask+uWSGI+upStar+nginx)    
    
        * 参考[digitalocean](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-14-04 "digitalocean")的教程    
        
        * 以下是我参考[digitalocean](https://www.digitalocean.com/community/tutorials/how-to-serve-flask-applications-with-uwsgi-and-nginx-on-ubuntu-14-04 "digitalocean")的教程后自定义的一些关键的配置文件：    
        
            1. uWSGI Configuration File    
            
            file_name: robotapp.ini(注意替换路径中的用户名为自己的用户名)    
            
                [uwsgi]    
                module = wsgi    
                master = true    
                processes = 2    
                socket = robotapp.sock    
                chdir = /home/user_name/robotapp/app/    
                wsgi-file = app/wsgi.py    
                daemonize = /home/user_name/robotapp/app/log/server.log    
                threads = 2    
                chmod-socket = 660    
                vacuum = true    
                die-on-term = true*    
                

            2. nginx config file
                
                $ vim cat /etc/nginx/sites-available/robotapp    
                    server{    
                        listen your_port(e.g.80);    
                        server_name your_server_ip/domain;    
                        location / {    
                            include uwsgi_params;    
                            uwsgi_pass unix:/home/user_name/robotapp/app/robotapp.sock;     
                            }    
                        }    
                    
                
### trouble shooting
     1. Issu: FileNotFoundError: [Errno 2] No such file or directory: 'xdg-open'
     Solution: install xdg-utils   xdg-utils  

         $ sudo apt-get install xdg-utils

     2. Error: no "view" mailcap rules found for type "image/png"
     WARNING: You don't seem to have any mimeinfo.cache files.
     Try running the update-desktop-database command. If you
     don't have this command you should install the
     desktop-file-utils package.

         $ sudo apt-get install desktop-file-utils

     3. Error: no "view" mailcap rules found for type "image/png"

         itchat.auto_login(enableCmdQR=2)

     4. File "/usr/lib/python3/dist-packages/urllib3/util.py", line 144, in _validate_timeout

     This error happens because of an incompatibility between your urllib3 and requests version. You can solve the problem by updating urllib3 and requests:
         pip install --upgrade urllib3 requests

     5. Install google api client:

         $ sudo pip3 install --upgrade google-api-python-client

     6. Install some necessary tool:

         $ pip install  -U gTTS
         $ apt-get install libav-tools -y

     7. file_cache is unavailable when using oauth2client >= 4.0.0
         $ pip3 list | grep 'oauth2client' 
         $ pip3 uninstall oauth2client==4.1.2
         $ pip3 install oauth2client==1.5.2
     speech_service = build('speech', 'v1', developerKey=apikey,cache_discovery=False)

     8. UnicodeEncodeError: 'ascii' codec can't encode characters in position 62-71: ordinal not in range(128)
     Refer to: http://www.php.cn/python-tutorials-358717.html

         1. 查看所有服务器所有本地编码：$ locale
            发现LANGUAGE并没有设置
         2. 在文件uWSGI的启动文件中加入该参数的设置
              $ vim /etc/init/robotapp.conf

                   description "uWSGI server instance configured to serve robotapp"
                   start on runlevel [2345]
                   stop on runlevel [!2345]

                   setuid kejing_usr
                   setgid www-data

                   env LANG="en_US.UTF-8"
                   env LANGUAGE="en_US.UTF-8"
                   env PATH=/home/kejing_usr/robotapp/robotenv/bin
                   chdir /home/kejing_usr/robotapp/app
                   exec uwsgi --ini robotapp.ini
