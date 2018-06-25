from django.shortcuts import render,reverse
from django.http import HttpResponse,JsonResponse
from .. models import Users
import os

# Create your views here.
# 用户添加
def add(request):
	# 判断是不是一个get请求
	if request.method == 'GET':
		# 如果是GET请求,则返回一个添加用户信息页面
		return render(request,'myadmin/user/add.html')
	elif request.method == 'POST':
		# 执行用户数据添加
		try:
			# # 接收数据，post的数据不能直接修改
			# data = request.POST
			# # copy()的数据中值为列表类型
			# data = data.copy()
			# # 将data数据中的列表类型转换成字符串，转换成标准的字典类型数据
			# data = data.dict()
			data = request.POST.copy().dict()
			# 删除csrf验证的字段数据
			del data['csrfmiddlewaretoken']
			# 密码加密  make_password 加密    check_password 解密
			from django.contrib.auth.hashers import make_password, check_password
			data['password'] = make_password(data['password'],None,'pbkdf2_sha256')
			# 头像上传
			# 	判断头像是否上传，没有则赋值为空
			if request.FILES.get('pic',None):
				data['pic'] = uploads(request)
				if data['pic'] == 1:
					return HttpResponse('<script>alert("上传的文件类型不符合要求");location.href="'+reverse('myadmin_user_add')+'"</script>')
			else:
				# data['pic'] = request.FILES.get('pic',None)
				# 删除pic字段
				del data['pic']
			print(data)
			obj = Users.objects.create(**data)
			return HttpResponse('<script>alert("添加成功");location.href="'+reverse('myadmin_user_list')+'"</script>')
		except:
			return HttpResponse('<script>alert("添加失败");location.href="'+reverse('myadmin_user_add')+'"</script>')

# 文件上传
def uploads(request):
	# 获取请求文件
	myfile = request.FILES.get('pic',None)
	# 获取上传文件的后缀名
	p = myfile.name.split('.').pop()
	arr = ['jpg','png','jpeg','gif']
	if p not in arr:
		return 1

	import time,random
	# 生成新的文件名
	filename = str(time.time())+str(random.randint(1,99999))+'.'+p
	# 打开文件
	destination = open("./static/pics/"+filename,"wb+")
	# 分块写入文件
	for chunk in myfile.chunks():
		destination.write(chunk)
	# 关闭文件
	destination.close()

	return '/static/pics/'+filename

# 用户列表
def list(request):
	# 查询所有用户
	# userlist = Users.objects.all()

	# 获取搜索条件,没有则给None
	types = request.GET.get('type',None)
	keywords = request.GET.get('keywords',None)

	# 判断是否具有搜索条件
	if types:
		if types == 'all':
			# 全条件搜索
			# 复杂搜索，需要导入Django框架的Q
			from django.db.models import Q
			userlist = Users.objects.filter(
					Q(username__contains=keywords)|
					Q(age__contains=keywords)|
					Q(email__contains=keywords)|
					Q(phone__contains=keywords)|
					Q(sex__contains=keywords)
				)
		elif types == 'username':
			# 按用户名搜索
			userlist = Users.objects.filter(username__contains=keywords)
		elif types == 'age':
			# 按年龄搜索
			userlist = Users.objects.filter(age__contains=keywords)
		elif types == 'email':
			# 按邮箱搜索
			userlist = Users.objects.filter(email__contains=keywords)
		elif types == 'phone':
			# 按手机号搜索
			userlist = Users.objects.filter(phone__contains=keywords)
		elif types == 'sex':
			# 按性别搜索
			userlist = Users.objects.filter(sex__contains=keywords)
	else:
		# 获取所有的用户数据
		userlist = Users.objects.filter()


	# 导入分页类
	from django.core.paginator import Paginator
	# 实例化分页对象
	# 	参数1：数据集合
	# 	参数2：每页显示条数
	paginator = Paginator(userlist,10)
	# print(paginator)
	# 获取当前页码数
	p = request.GET.get('p',1)
	# 获取当前页的数
	ulist = paginator.page(p)
	print(ulist.paginator.num_pages)
	# 分配数据
	content = {'userlist':ulist}
	return render(request,'myadmin/user/list.html',content)

# 删除用户
def delete(request):
	try:
		# 获取删除用户id
		uid = request.GET.get('uid',None)
		# 获取用户对象
		ob = Users.objects.get(id=uid)
		# 判断是否有头像
		if ob.pic:
			# 如果有就删除本地对应头像文件
			os.remove('.'+ob.pic)
		# 删除数据库用户信息
		ob.delete()
		data = {'msg':'删除成功','code':0}
	except:
		data = {'msg':'删除失败','code':1}


	return JsonResponse(data)

# 更新用户
def edit(request):
	# 获取更新用户id
	uid = request.GET.get('uid',None)
	# 获取更新用户对象
	ob = Users.objects.get(id=uid)
	# 判断  是get请求返回跟新页面，是post请求则更新数据库
	if request.method == 'GET':
		# 将更新对象传给跟新页面显示
		context = {'uinfo':ob}
		return render(request,'myadmin/user/edit.html',context)
	elif request.method == 'POST':
		try:
			# 判断是否有更新头像
			if request.FILES.get('pic',None):
				# 判断更新对象有没有原始头像，有则删除
				if ob.pic:
					os.remove('.'+ob.pic)
				# 上传头像
				ob.pic = uploads(request)
			# 更新数据
			ob.username = request.POST['username']
			ob.email = request.POST['email']
			ob.age = request.POST['age']
			ob.sex = request.POST['sex']
			ob.phone = request.POST['phone']
			ob.save()
			# 成功，返回列表页
			return HttpResponse('<script>alert("更新成功");location.href="'+reverse('myadmin_user_list')+'"</script>')
		except:
			# 失败，返回列更新页面并将更新对象id做参数传出
			return HttpResponse('<script>alert("更新失败");location.href="'+reverse('myadmin_user_edit')+'?uid='+str(ob.id)+'"</script>')