from django.shortcuts import render,reverse
from django.http import HttpResponse,JsonResponse
from .. models import Goods,Types
from . typesviews import getalltypes
from . userviews import uploads
import os

def add(request):
	if request.method == 'GET':
		tlist = getalltypes()
		context = {'tlist':tlist}
		# 返回添加分类页面
		return render(request,'myadmin/goods/add.html',context)
	elif request.method == 'POST':
		print(request.FILES.get('pic'))
		# 判断是否上传图片
		if not request.FILES.get('pic',None):
			return HttpResponse('<script>alert("必须选择商品图片");location.href="'+reverse('myadmin_goods_add')+'"</script>')
		pic = uploads(request)
		if pic == 1:
			return HttpResponse('<script>alert("图片类型错误");location.href="'+reverse('myadmin_goods_add')+'"</script>')
		# 添加商品
		# 接收表单数据
		data = request.POST.copy().dict()
		# 删除掉 csrf验证的字段数据
		del data['csrfmiddlewaretoken']
		data['pics'] = pic
		data['typeid'] = Types.objects.get(id=data['typeid'])
		# 写入数据库
		ob = Goods.objects.create(**data)
		return HttpResponse('<script>alert("添加成功");location.href="'+reverse('myadmin_goods_list')+'"</script>')


def list(request):

	glist = Goods.objects.all()
	context = {'glist':glist}
	# 返回添加分类页面
	return render(request,'myadmin/goods/list.html',context)


def delete(request):
	try:
		# 获取删除商品id
		gid = request.GET.get('gid',None)
		# 获取用户对象
		ob = Goods.objects.get(id=gid)
		# 判断是否有头像
		if ob.pics:
			# 如果有就删除本地对应头像文件
			os.remove('.'+ob.pics)
		# 删除数据库用户信息
		ob.delete()
		data = {'msg':'删除成功','code':0}
	except:
		data = {'msg':'删除失败','code':1}
	return JsonResponse(data)


def edit(request):
	if request.method == 'GET':
		gid = request.GET.get('gid')
		ob = Goods.objects.get(id=gid)
		tlist = getalltypes()
		context = {'tlist':tlist,'goods':ob}
		# 返回添加分类页面
		return render(request,'myadmin/goods/edit.html',context)
	elif request.method == 'POST':
		gid = request.GET.get('gid')
		ob = Goods.objects.get(id=gid)
		try:
			# 判断是否有更新头像
			if request.FILES.get('pic',None):
				# 判断更新对象有没有原始头像，有则删除
				if ob.pics:
					os.remove('.'+ob.pics)
				# 上传头像
				ob.pics = uploads(request)
			# print(request.POST['typeid'])
			ob.typeid = Types.objects.get(id=request.POST['typeid'])
			ob.title = request.POST['title']
			ob.descr = request.POST['descr']
			ob.price = request.POST['price']
			ob.store = request.POST['store']
			ob.info = request.POST['info']
			ob.save()
			# 成功，返回列表页
			return HttpResponse('<script>alert("更新成功");location.href="'+reverse('myadmin_goods_list')+'"</script>')
		except:
			# 失败，返回列更新页面并将更新对象id做参数传出
			return HttpResponse('<script>alert("更新失败");location.href="'+reverse('myadmin_goods_edit')+'?gid='+str(ob.id)+'"</script>')




