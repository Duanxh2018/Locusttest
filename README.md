# Locust + python实现性能压测

用Locust和python实现http交易接口性能测试，性能并发所用fromaddress和toaddress数据分别存放于fromaddress.txt、toaddress.txt

测试步骤：
1、修改Q2Test.py文件中的url地址为获取接口数据地址（即部署的链地址）

2、压力机安装Locust: pip install locustio 

3、压力机安装web3-5.0.0a6-py3-none-any.whl文件： pip install web3-5.0.0a6-py3-none-any.whl

4、运行脚本：如在本地机器上作为压力机：locust -H http://IP+post(服务器IP和端口号) -f Q2Test.py

		分布式压测需设置master，然后slave机启动时需声明master机是哪台，master和slave为1对多的关系。具体参数可使用locust --help查看。

5、浏览器打开:localhost:8089 设置并发数和每秒启动用户数 

6、最终优化版本：Q5test.py