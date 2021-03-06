#! /usr/bin/env python3
# -*- coding:utf-8 -*-
"""
====================================================================
Project Name: kyls_script
Description :
Author      : Liao Heng
Create Date : 2022-05-19
====================================================================
"""
keywords_valid = """
矿
球团
废钢
钢铁原料
炉料
有色金属
黑色金属
稀有金属
轻金属
重金属
开采
采选
砂石骨料
建筑石材
砂石工业
产能置换
超低排放
环境评价
碳排放
碳中和
"""

keywords_search = """"
矿
铁
球团
废钢
钢铁原料
炉料
有色金属
黑色金属
稀有金属
轻金属
重金属
开采
采选
砂石骨料
建筑石材
砂石工业
产能置换
超低排放
环境评价
碳排放
碳中和
非金属矿		澳洲铁矿
化工矿山		巴西铁矿
有色金属矿		耙矿绞车
黑色金属矿		爆破
贵金属矿		爆破安全
稀有金属		别列佐夫铁矿
轻金属		采掘矿石
重金属		采矿
矿山		地下采矿
石灰石		地下矿
石英		多金属矿
叶蜡石		非煤矿山
凹凸棒石		非洲铁矿
钒矿		废钢  电炉钢
方解石		分级  磨矿
沸石		改建
高岭土		改扩建
铬铁矿		钢铁  安全评价
硅灰石		钢铁  搬迁
硅藻土		钢铁  搬迁改造
海泡石		钢铁  产能
红柱石		钢铁  产业园
花岗岩		钢铁  产业转型
滑石		钢铁  产业转型升级
辉绿岩		钢铁  超低排放
钾盐		钢铁  粗钢产量
灰岩		钢铁  工程建设
安山岩		钢铁  环境影响
白云岩		钢铁  环评
大理岩		钢铁  技改
橄榄岩		钢铁  技术改造
花岗岩		钢铁  建设项目
辉绿岩		钢铁  炼铁
建筑用
砂		钢铁  料场
建筑用
砂岩		钢铁  深加工
建筑用
闪长岩		钢铁  铁精粉  深加工
建筑用
石料		钢铁  退城进园
建筑用
玄武岩		钢铁  脱硫
金红石		钢铁  脱销
金矿		钢铁  循环利用
蓝晶石		钢铁  烟气
锂矿		钢铁  原料堆场
磷矿		钢铁  置换升级
菱镁矿		铬球
硫铁矿		海外矿
铝土矿		海外铁矿
锰矿		化学矿山
钼矿		建设
铌矿		进口矿
铌钽矿		进口铁矿石
镍矿		精矿
凝灰岩		井下采矿
硼矿		开采项目 环境影响评价
膨润土		矿  AngloAmerican
片麻岩		矿  ArcelorMittal
铅矿		矿  Assmang
砂金		矿  Atlas
石膏		矿  BHP
石灰岩		矿  bod
石榴子石		矿  CAP
石煤		矿  CFR
石棉		矿  ChampionIron
石墨		矿  CiticPacific
锶矿		矿  Clevel  Cliffs
天青石		矿  Cliffs
钛矿		矿  CSN
钽矿		矿  Evraz
陶瓷土		矿  Ferrexpo
锑矿		矿  FerrousResources
石英砂		矿  FMG
铁钒土		矿  FOB
铁矿		矿  Fomento
铜矿		矿  GDP
钨矿		矿  GIS
锡矿		矿  GPSRTK
霞石正长岩		矿  GrangeResource
锌矿		矿  Grangeresources
玄武岩		矿  IRC
冶金用脉石英		矿  Isa磨机
叶腊石		矿  Karara
伊利石		矿  Kumba
银矿		矿  LKAB
萤石		矿  Mechel
云母		矿  Metalloinvest
长石		矿  Metinvest
珍珠岩		矿  Midwest-WeldRange
蛭石		矿  MinasRio
重晶石		矿  MineralResource
稀土矿		矿  MineralResources
钒钛磁铁矿		矿  MountGibson
磁铁矿		矿  NLMK
褐铁矿		矿  NMDC
菱 铁矿		矿  PB粉
混合矿		矿  PMC
红矿		矿  RioTinto
赤铁矿		矿  RioTinto(IOC)
氧化矿		矿  Samarco
高岭土矿		矿  Severstal
锆矿		矿  ShougangGroup
铬矿		矿  SIMEC
汞矿		矿  SNIM
钴矿		矿  Usiminas
硅灰石矿		矿  VALE
硅藻土矿		矿  VedantaMining
海泡石矿		矿  VMSalgaocar
滑石矿		矿  安评
钾盐矿		矿  安全
建材矿		矿  安全认证
菱铁矿		矿  安全系统
镁矿		矿  安赛乐米塔尔
膨润土矿		矿  澳大利亚
铅锌矿		矿  巴粗
石膏矿		矿  巴西
石灰石矿		矿  搬迁
石棉矿		矿  板框式 自动压滤机
石墨矿矿		矿  棒磨机
石英矿		矿  棒条筛
霞石正长岩矿		矿  保有储量
叶蜡石矿		矿  爆破
伊利石矿		矿  备件
萤石矿		矿  备品
云母矿		矿  焙烧
长石矿		矿  泵
珍珠岩矿		矿  必和必拓
铝矿		矿  闭坑
		矿  闭库
		矿  闭库设计
		矿  边坡监测
		矿  变质岩
		矿  剥胎机
		矿  捕收剂
		矿  擦洗机
		矿  材料车
		矿  采购成本
		矿  采掘
		矿  采空区
		矿  采矿项目
		矿  采区
		矿  采石场
		矿  采选
		矿  测距仪
		矿  产能
		矿  铲齿
		矿  铲斗
		矿  铲运
		矿  铲运机
		矿  铲装
		矿  超导磁选机
		矿  超低排放
		矿  超贫
		矿  超特粉
		矿  衬板
		矿  衬胶泵
		矿  冲击磨
		矿  冲击破碎机
		矿  冲击器
		矿  冲击式
		矿  充填
		矿  出让
		矿  除尘
		矿  除铁器
		矿  储量
		矿  穿孔
		矿  磁场筛
		矿  磁滚筒
		矿  磁滑轮
		矿  磁化焙烧
		矿  磁团聚
		矿  磁性衬板
		矿  磁选
		矿  粗精矿
		矿  大块
		矿  输送机
		矿  单级泵
		矿  淡水河谷
		矿  到岸价
		矿  到港价
		矿  道路养护
		矿  地理信息
		矿  地下开采
		矿  地压监测
		矿  地质调查
		矿  地质构造
		矿  地质环境
		矿  地质品位
		矿  地质灾害
		矿  低品位
		矿  底卸式
		矿  电耙
		矿  电铲
		矿  电磁
		矿  电机车
		矿  电缆
		矿  电线
		矿  电选
		矿  斗轮混匀
		矿  堆浸
		矿  堆料机
		矿  堆取料设备
		矿  对外依存
		矿  多级泵
		矿  多级机站
		矿  多绳摩擦
		矿  俄罗斯
		矿  二期
		矿  阀门
		矿  方案
		矿  方法
		矿  废石
		矿  废石场
		矿  废油再生
		矿  沸腾炉
		矿  分级
		矿  分级机
		矿  分选设备
		矿  粉尘
		矿  风机
		矿  风井
		矿  服务年限
		矿  浮选
		矿  福蒂斯丘
		矿  辅助车辆
		矿  附属设施
		矿  复垦
		矿  改建
		矿  改造
		矿  干排
		矿  干抛
		矿  干散货
		矿  干选
		矿  干燥
		矿  干燥机
		矿  钢球
		矿  港口
		矿  高炉
		矿  高梯度
		矿  格子型
		矿  隔离泵
		矿  隔膜泵
		矿  给料机
		矿  给料系统
		矿  工程
		矿  工业泵
		矿  骨料
		矿  固定筛
		矿  固体废物
		矿  拐点坐标
		矿  冠军铁
		矿  管道
		矿  罐笼
		矿  光选
		矿  广义磨
		矿  规划
		矿  辊磨机
		矿  辊式
		矿  辊套
		矿  滚轴筛
		矿  国土资源
		矿  过流件
		矿  过滤除尘
		矿  过滤机
		矿  哈萨克斯坦
		矿  还原铁粉
		矿  海运
		矿  后卸式汽车
		矿  弧形筛
		矿  化探设备
		矿  环保
		矿  环境保护
		矿  环境地质
		矿  环境评价
		矿  环境生态
		矿  环境污染
		矿  环境影响
		矿  环境整治
		矿  环冷机
		矿  环评
		矿  黄金
		矿  灰分检测
		矿  灰渣泵
		矿  恢复
		矿  回采
		矿  回收
		矿  回转窑
		矿  混合砂
		矿  混凝土
		矿  混装炸药
		矿  机车
		矿  机械化
		矿  机制砂
		矿  基建
		矿  箕斗
		矿  吉普森
		矿  技改
		矿  技经指标
		矿  技术
		矿  加高扩容
		矿  加工
		矿  加拿大
		矿  加油车
		矿  价款
		矿  监测
		矿  兼并重组
		矿  拣选
		矿  检测设备
		矿  检修车
		矿  减排
		矿  减速器
		矿  建筑石料
		矿  建筑用砂
		矿  浆体输送
		矿  胶带
		矿  搅拌
		矿  搅拌槽
		矿  接替
		矿  节能
		矿  结构构造
		矿  金属
		矿  进口
		矿  经伟仪
		矿  精粉
		矿  精选
		矿  井提升系统
		矿  井下
		矿  井巷
		矿  净化器
		矿  局扇
		矿  开采
		矿  开发利用
		矿  开拓运输
		矿  勘查
		矿  勘探
		矿  可行性
		矿  克利夫斯
		矿  坑探
		矿  空气过滤器
		矿  空气净化
		矿  空气压缩机
		矿  空压机
		矿  扩建
		矿  扩能
		矿  劳动保护
		矿  雷管
		矿  雷蒙磨
		矿  离岸价
		矿  力拓
		矿  立磨
		矿  粒度检测
		矿  联合运输
		矿  链篦机
		矿  料场
		矿  溜槽
		矿  流态化
		矿  六大系统
		矿  炉料
		矿  露采转
		矿  露天开采
		矿  露天转
		矿  轮胎
		矿  罗盘
		矿  罗伊山
		矿  绿色
		矿  麦克粉
		矿  麦克块
		矿  毛里塔尼亚
		矿  锚杆
		矿  锚索
		矿  美国
		矿  磨机
		矿  磨球
		矿  磨选
		矿  墨西哥
		矿  耐磨
		矿  南非
		矿  内滤
		矿  能耗
		矿  能评
		矿  能源
		矿  泥浆泵
		矿  年处理
		矿  纽曼
		矿  浓度检测
		矿  浓缩
		矿  浓缩机
		矿  排土场
		矿  排岩
		矿  炮孔
		矿  配套
		矿  膨润土
		矿  批复
		矿  品位
		矿  平板车
		矿  平路机
		矿  平巷
		矿  评估
		矿  评价
		矿  评价指标
		矿  破碎
		矿  破碎机
		矿  破碎站
		矿  期货
		矿  起泡剂
		矿  起重机
		矿  凿岩机
		矿  汽车
		矿  潜孔钻
		矿  强力粉碎
		矿  撬毛台车
		矿  清洁生产
		矿  球磨机
		矿  球团
		矿  取料机
		矿  权益
		矿  全站仪
		矿  人工砂
		矿  人员定位
		矿  人员监测
		矿  容积式
		矿  入选
		矿  软件
		矿  瑞典
		矿  润滑
		矿  三大巨头
		矿  三期
		矿  扫描仪
		矿  色选
		矿  砂泵
		矿  砂金
		矿  砂石
		矿  筛分
		矿  烧结机
		矿  设备
		矿  设计
		矿  设施
		矿  深部
		矿  深加工
		矿  升级
		矿  升贴水
		矿  生产
		矿  生态
		矿  生铁
		矿  施工作业
		矿  湿选
		矿  石料
		矿  石英岩
		矿  收益
		矿  疏干水
		矿  输送
		矿  竖井
		矿  竖炉
		矿  数据库
		矿  数字化
		矿  水泵
		矿  水分检测
		矿  水污染
		矿  水准仪
		矿  碎石机
		矿  碎石加工
		矿  塔磨机
		矿  探转采
		矿  碳达峰
		矿  碳汇
		矿  碳排放
		矿  碳市场
		矿  碳中和
		矿  碳足迹
		矿  唐克里里
		矿  淘汰
		矿  淘洗
		矿  提升
		矿  天井
		矿  跳汰机
		矿  通风
		矿  投标
		矿  土壤治理
		矿  推土机
		矿  退城进园
		矿  脱磁
		矿  脱硫
		矿  脱泥槽
		矿  脱水
		矿  脱硝
		矿  挖机
		矿  挖掘机
		矿  瓦斯抽放
		矿  完全成本
		矿  万吨
		矿  尾矿
		矿  尾砂
		矿  委内瑞拉
		矿  乌克兰
		矿  污染
		矿  污水处理
		矿  无害化
		矿  无人
		矿  物探设备
		矿  物位检测
		矿  稀土
		矿  稀有金属
		矿  洗选厂
		矿  现状
		矿  现状评价
		矿  限产
		矿  项目
		矿  巷道
		矿  斜板
		矿  斜井
		矿  新技术
		矿  新建
		矿  新理论
		矿  玄武岩
		矿  旋流器
		矿  选比
		矿  选别
		矿  选厂
		矿  选矿厂
		矿  循环
		矿  压路机
		矿  压滤机
		矿  压气辅助
		矿  压通排
		矿  牙轮钻
		矿  烟气
		矿  岩浆岩
		矿  岩石
		矿  研究
		矿  杨迪粉
		矿  杨迪块
		矿  摇床
		矿  遥感探测
		矿  药剂
		矿  冶金建材
		矿  叶轮式泵
		矿  液压铲
		矿  一期
		矿  伊朗
		矿  溢流型
		矿  印度
		矿  印度尼西亚
		矿  印尼
		矿  应急处置
		矿  英美资源
		矿  影响评价
		矿  永磁
		矿  油水分离
		矿  有轨运输
		矿  有色金属
		矿  预评价
		矿  预审
		矿  元素分析
		矿  原料厂
		矿  原料场
		矿  原料堆场
		矿  圆筒筛
		矿  运矿车
		矿  运矿卡车
		矿  运输
		矿  再生骨料
		矿  再生资源
		矿  再选
		矿  在建
		矿  赞比亚
		矿  凿岩
		矿  渣浆泵
		矿  炸药
		矿  招标
		矿  振动
		矿  振网筛
		矿  整合
		矿  整体搬迁
		矿  支护
		矿  治理
		矿  智能化
		矿  中标
		矿  重介质
		矿  重选
		矿  主扇
		矿  柱钉
		矿  柱磨机
		矿  柱塞泵
		矿  铸球
		矿  专篇
		矿  专项监察
		矿  转包
		矿  转型升级
		矿  转载站
		矿  装岩
		矿  装药
		矿  装运
		矿  装载
		矿  资格
		矿  资源
		矿  自磨
		矿  自然保护
		矿  自卸
		矿  综采
		矿  综合利用
		矿  综合治理
		矿  钻杆
		矿  钻机
		矿  钻探
		矿  钻头
		矿产资源
		矿车
		矿床
		矿床模型
		矿价
		矿井
		矿区范围
		矿权
		矿山  安全
		矿山  爆破
		矿山  采剥
		矿山  充填
		矿山  地理信息
		矿山  地质环境
		矿山  定位
		矿山  复产
		矿山  复工
		矿山  改建矿山
		矿山  改扩建
		矿山  工程
		矿山  环境恢复
		矿山  机械
		矿山  经济合理
		矿山  井下采掘
		矿山  开采
		矿山  开发
		矿山  开发治理
		矿山  扩建
		矿山  绿地项目
		矿山  绿色
		矿山  拟建
		矿山  拟在建
		矿山  企业
		矿山  设备
		矿山  设计
		矿山  深井
		矿山  生产
		矿山  生态
		矿山  施工
		矿山  石材
		矿山  数字
		矿山  停产
		矿山  投资
		矿山  外包
		矿山  尾矿
		矿山  无废
		矿山  无人
		矿山  无人化
		矿山  物联网
		矿山  新建
		矿山  信息化
		矿山  选矿
		矿山  研究
		矿山  易耗品
		矿山  治理
		矿山  智慧
		矿山  智能
		矿山  重大隐患
		矿山  装备
		矿山  总承包
		矿山  作业
		矿石  构造
		矿石  化学成分
		矿石  类型
		矿物
		矿物成分
		矿物加工
		矿物检测
		矿冶工程
		矿业  投资
		矿业权
		矿渣
		矿政管理
		矿资源 勘察开发
		扩建
		扩建矿山
		离心选矿机
		炼钢  产能置换
		炼铁  超低排放
		炼铁  除尘
		炼铁  技术改造
		炼铁  料场
		炼铁  项目
		露天采矿
		露天矿
		绿色矿山
		绿色矿业
		磨矿
		磨矿设备
		南美洲铁矿
		拟建
		拟建矿山
		拟在建
		拟在建 矿山
		配矿系统
		破碎  磨矿
		破碎  筛分
		球团  安全评价
		球团  搬迁
		球团  产能置换
		球团  超低排放
		球团  除尘
		球团  带式
		球团  复合材料
		球团  高品质
		球团  工程
		球团  含镁
		球团  环境影响
		球团  环评
		球团  回转窑
		球团  技改
		球团  技术改造
		球团  减量
		球团  减量置换
		球团  碱性
		球团  建设项目
		球团  精品
		球团  链篦机
		球团  料场
		球团  镁质
		球团  能评
		球团  烧结
		球团  升级
		球团  生产线
		球团  竖炉
		球团  酸性
		球团  铁粉
		球团  铁精粉
		球团  退城进园
		球团  脱硫
		球团  脱销
		球团  项目
		球团  烟气
		球团  氧化
		球团  原料堆场
		球团  整体搬迁
		球团  质量
		球团  中性
		权益矿
		入选矿量
		三大矿
		烧结矿
		设计采矿能力
		深井矿山
		生产矿山
		石材矿山
		世界铁矿石
		数字矿山
		水力洗矿床
		四大矿
		探矿权
		探矿权转采矿权
		铁精粉生产线
		铁矿粉
		铁矿砂
		铁矿石
		停产矿山
		尾矿
		尾矿库
		尾矿品位
		尾矿再选
		尾矿综合利用
		无废矿山
		无人采矿
		无人矿山
		西芒杜铁矿
		洗矿机
		新建矿山
		选矿
		冶金矿山
		印度铁矿
		有毒有害气体
		原矿
		圆筒洗矿机
		圆锥重介质 选矿机
		云雾抑尘技术
		长协矿
		振动放矿机
		直接还原铁
		智慧矿山
		智能化矿山
		智能矿山
		重介质选矿机
		重晶石矿
		轴流扇风机

"""
