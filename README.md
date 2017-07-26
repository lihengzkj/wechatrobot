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
    ### 简单使用    
    
        * 使用 git 克隆代码到Linux    
        
        * 替换tuling和google的key为自己的key    
        
        * $ python ./app/webserver.py    
        
    ### 复杂使用(flask+uWSGI+upStar+nginx)    
    
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
                        listen 8080;    
                        server_name 13.67.59.242;    
                        location / {    
                            include uwsgi_params;    
                            uwsgi_pass unix:/home/user_name/robotapp/app/robotapp.sock;    
                        }    
                    }    
                
