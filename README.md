# basesite
项目启动模板
用这个模板记得修改secret key

# 开发相关  
后端：  
python 3.6.5  
django 2.2  
celery  //todo  

前端：  
vue  
vue apollo
element UI  
vue element admin  

数据库：  
mysql  
redis  

全文检索：  
elastic search  

完成的功能：  
1） 实现了一个简单的企业展示网站，动态部分仅一个最简的新闻系统   
2） 前后端接口是graphql，而不是restfull  
3)  有两套前端页面，分别对应pc端和移动端 
4)  用jwt客户端鉴权，方便网站做大了跨域，也方便记录nginx记录用户信息 


# 运维相关
openresty  
sentry  
pm2  
钉钉 //将各类运维信息发送到dingding上，进行消息提醒  

完成的功能：  
openresty:  
1） 根据user agent判断用户是来自pc端还是移动端，自动rewrite到响应的二级域名  
2)  分析出已登录用户的id(可能是邮箱，也可能是tel，取决于django中对jwt的设置)，将操作日志关联到人，便于后期做用户行为分析.   
需要安装lua-resty-jwt: luarocks install lua-resty-jwt //todo  
lua对jwt token解码需要用到django的secret key，所以get_auth_user.lua中的secretKey请务必和django的配置保持一致。
由于本例中我们是基于手机号码作为用户主键的，字段名是：tel。可以在相应的lua文件中修改。
3)  对静态内容的存取进行鉴权 //todo  

sentry:  接收各应用的错误日志  
pm2: 进程管理，挂机后自动重启  

# 数据统计
nifi  // 数据采集  
superset  //数据呈现  


# 常用的工具
数据库建模：  
powerdesign  

编辑器：  
vs code  
pycharm  
sublime  

其他：  
产品原型：balsamiq mockup  
UML：  starUml  
ssh客户端： secureCRT  
mysql客户端：  navicat  
抓包：  fiddler,  wireshark  
截屏：  FSCapture  
终端管理：  MobaXterm   //windows下的  


参考资料：  
[nginx+lua学习——记一次静态文件下载流程打点](https://www.jianshu.com/p/4fd8c2ad0223)  
[JSON Web Token 入门教程](https://www.ruanyifeng.com/blog/2018/07/json_web_token-tutorial.html)  
[openresty 日志输出的处理](https://zhuanlan.zhihu.com/p/37736874)
[使用nginx + lua 自定义access.log](https://bikong0411.github.io/2015/11/05/ngx-lua-custom-access-log-format.html)