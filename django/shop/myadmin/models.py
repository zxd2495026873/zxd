from django.db import models

# Create your models here.

# 会员模型
class Users(models.Model):
	username=models.CharField(max_length=50)
	password=models.CharField(max_length=77)
	email=models.CharField(max_length=50)
	phone=models.CharField(max_length=11)
	age=models.IntegerField(null=True)
	sex=models.CharField(max_length=1,null=True)
	pic=models.CharField(max_length=100,null=True)
	# 状态  0:正常  1:禁用
	status=models.IntegerField(default=0)
	addtime=models.DateTimeField(auto_now_add=True)

# 商品分类模型
class Types(models.Model):
	name = models.CharField(max_length=20)
	pid = models.IntegerField()
	path = models.CharField(max_length=50)

# 商品模型
class Goods(models.Model):
	# 一对多
	typeid = models.ForeignKey(to="Types",to_field="id")
	# 标题
	title = models.CharField(max_length=255)
	# 描述
	descr = models.CharField(max_length=255,null=True)
	# 详情
	info = models.TextField(null=True)
	# 浮点类型，参数一：总为数  参数二：小数位数
	price = models.DecimalField(max_digits=10,decimal_places=2)
	# 图片
	pics = models.CharField(max_length=100)
	# 状态 0-新发布  1-下架
	status = models.IntegerField(default=0)
	# 库存
	store = models.IntegerField(default=0)
	# 订单数
	num = models.IntegerField(default=0)
	# 点击数
	clicknum = models.IntegerField(default=0)
	# 添加时间
	addtime = models.DateTimeField(auto_now_add=True)