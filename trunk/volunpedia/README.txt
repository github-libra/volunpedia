1. 注册一个administrator用户，并设置为superuser

2. 将/Python/lib/tenjin.py拷贝到<python_install>/lib下:
- windows: e.g. D:/Python/Lib
- linux: e.g. /usr/lib/python2.7

3. 将/Wiki/wikiconfig.py替换MoinMoin安装目录的对应文件
- windows: e.g. <moin_base>/moin-1.9.7/wikiconfig.py
- linux: e.g. /src/www/moin/wiki/wikiconfig.py

3.1 对windows部署，还需要一步额外的操作，编辑<moin_base>/moin-1.9.7/wikiconfig.py：
找到data_dir = os.path.join(instance_dir, 'data', '')
修改为data_dir = os.path.join(instance_dir, 'wiki/data', '')
找到data_underlay_dir = os.path.join(instance_dir, 'underlay', '')
修改为data_underlay_dir = os.path.join(instance_dir, 'wiki/underlay', '')

4. 将/Wiki/MoinMoin下的文件拷贝替换到MoinMoin安装文件MoinMoin目录下
- windows: e.g. <moin_base>/moin-1.9.7/MoinMoin
- linux: /srv/www/moin/pythonenv/lib/python2.7/site-packages/MoinMoin

5. 将/Wiki/data下的文件拷贝替换到MoinMoin安装文件data目录下
- windows：e.g. <moin_base>/moin-1.9.7/wiki/data
- linux: e.g. /srv/www/moin/wiki/data

5.1 对Linux还需要一步额外的操作，把刚才copy的所有文件chown成www-data:www-data
- linux: chown -R www-data:www-data /srv/www/moin

6. administrator -> 设置 -> 用户设置 -> 主题，改为ngowiki

7. 输入url: /copyright?action=dbinit
- windows: e.g. http://localhost/wiki/copyright?action=dbinit
- linux: e.g. http://localhost/copyright?action=dbinit
这里会初始化数据库，如果没有错误，会显示一个空页面，表示操作执行成功

8. 修改apache/nginx配置，将静态文件路径映射到/moin_static197_20140407
- windows: 
修改httpd.conf：Alias /moin_static197_20140407 "<moin_base>/moin-1.9.7/MoinMoin/web/static/htdocs"
- linux:
修改available_sites中的配置，Location /moin_static197_20140407{...}

9. 输入url: /志愿百科?action=edit&line=2
- windows: e.g. http://localhost/wiki/%E5%BF%97%E6%84%BF%E7%99%BE%E7%A7%91?action=edit&line=2
- linux: e.g. http://localhost/%E5%BF%97%E6%84%BF%E7%99%BE%E7%A7%91?action=edit&line=2

将页面内容替换为：
#acl administrator:read,write,delete,revert,admin All:read
<<FrontpageMacro>>
然后保存

10. 对windows部署还有一步额外操作，将/cgi_patch/fcgi_base.py拷贝替换<moin_base>/moin-1.9.7/MoinMoin/support/flup/server中原来的fcgi_base.py文件