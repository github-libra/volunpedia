������
-----------------------------------

```
1. ע��һ��administrator�û���������Ϊsuperuser

2. ��/Python/lib/tenjin.py������<python_install>/lib��:
- windows: e.g. D:/Python/Lib
- linux: e.g. /usr/lib/python2.7

3. ��/Wiki/wikiconfig.py�滻MoinMoin��װĿ¼�Ķ�Ӧ�ļ�
- windows: e.g. <moin_base>/moin-1.9.7/wikiconfig.py
- linux: e.g. /src/www/moin/wiki/wikiconfig.py

3.1 ��windows���𣬻���Ҫһ������Ĳ������༭<moin_base>/moin-1.9.7/wikiconfig.py��
�ҵ�data_dir = os.path.join(instance_dir, 'data', '')
�޸�Ϊdata_dir = os.path.join(instance_dir, 'wiki/data', '')
�ҵ�data_underlay_dir = os.path.join(instance_dir, 'underlay', '')
�޸�Ϊdata_underlay_dir = os.path.join(instance_dir, 'wiki/underlay', '')

4. ��/Wiki/MoinMoin�µ��ļ������滻��MoinMoin��װ�ļ�MoinMoinĿ¼��
- windows: e.g. <moin_base>/moin-1.9.7/MoinMoin
- linux: /srv/www/moin/pythonenv/lib/python2.7/site-packages/MoinMoin

5. ��/Wiki/data�µ��ļ������滻��MoinMoin��װ�ļ�dataĿ¼��
- windows��e.g. <moin_base>/moin-1.9.7/wiki/data
- linux: e.g. /srv/www/moin/wiki/data

5.1 ��Linux����Ҫһ������Ĳ������Ѹղ�copy�������ļ�chown��www-data:www-data
- linux: chown -R www-data:www-data /srv/www/moin

6. administrator -> ���� -> �û����� -> ���⣬��Ϊngowiki

7. ����url: /copyright?action=dbinit
- windows: e.g. http://localhost/wiki/copyright?action=dbinit
- linux: e.g. http://localhost/copyright?action=dbinit
������ʼ�����ݿ⣬���û�д��󣬻���ʾһ����ҳ�棬��ʾ����ִ�гɹ�

8. �޸�apache/nginx���ã�����̬�ļ�·��ӳ�䵽/moin_static197_20140407
- windows: 
�޸�httpd.conf��Alias /moin_static197_20140407 "<moin_base>/moin-1.9.7/MoinMoin/web/static/htdocs"
- linux:
�޸�available_sites�е����ã�Location /moin_static197_20140407{...}

9. ����url: /־Ը�ٿ�?action=edit&line=2
- windows: e.g. http://localhost/wiki/%E5%BF%97%E6%84%BF%E7%99%BE%E7%A7%91?action=edit&line=2
- linux: e.g. http://localhost/%E5%BF%97%E6%84%BF%E7%99%BE%E7%A7%91?action=edit&line=2

��ҳ�������滻Ϊ��
#acl administrator:read,write,delete,revert,admin All:read
<<FrontpageMacro>>
Ȼ�󱣴�

10. ��windows������һ�������������/cgi_patch/fcgi_base.py�����滻<moin_base>/moin-1.9.7/MoinMoin/support/flup/server��ԭ����fcgi_base.py�ļ�
```\n
