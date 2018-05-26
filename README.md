# letsdoubi
Doubi project

目前版本 0.1.0
Map/26/2018

这是一个企图使用身边现有知识实现股价分析的逗比尝试，摸着石头过河，祝我们成功，哦耶！

master branch 用于存放 stable code
develop branch 用于存放 正在开发版本的code
feature branch 请使用 feature/**的路径格式， 用于实现某个功能
bugfix branch 请使用 bugfix/**的路径格式，用于修复某个bug

Lifecycle：
1. 确定下一个版本需要解决的问题和实现的代码
2. 分配任务和时间
3. 分别或合作完成任务，建立feature分支。
4. 提交feature代码到develop branch，测试验证
5. 讨论这个版本的问题和下一个版本需要解决的问题和实现的代码，回到step 2.

0.1.0版本需要解决的问题：
1. 如何实现信息的收集
	1.1 如果获取tweet数据
	1.2 如何获取新闻数据
2. 如何进行数据的语义分析
	2.1 使用何种框架
	2.2 使用何种语义分析lib
3. 股价与分析结果之间的关系
	3.1 是否存在正相关
	3.2 如何确定消息对股价浮动和市场的影响