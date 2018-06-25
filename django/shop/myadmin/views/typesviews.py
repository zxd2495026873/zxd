from django.shortcuts import render,reverse
from django.http import HttpResponse,JsonResponse
from .. models import Types

# 获取所有的分类
def getalltypes():
	tlist = Types.objects.extra(select = {'paths':'concat(path,id)'}).order_by('paths')
	for x in tlist:
		if x.pid == 0:
			x.pname = '顶级分类'
		else:
			t = Types.objects.get(id=x.pid)
			x.pname = t.name
		num = x.path.count(',')-1
		x.name = (num*'|----')+x.name

	return tlist

def add(request):
	if request.method == 'GET':
		tlist = getalltypes()
		context = {'tlist':tlist}
		# 返回添加分类页面
		return render(request,'myadmin/types/add.html',context)
	elif request.method == 'POST':
		# 执行添加分类
		ob = Types()
		ob.name = request.POST['name']
		ob.pid = request.POST['pid']
		if ob.pid == '0':
			ob.path = '0,'
		else:
			# 根据当前父级id获取path，再添加父级id
			t = Types.objects.get(id=ob.pid)
			ob.path = t.path+str(t.id)+','
		ob.save()
		return HttpResponse('<script>alert("添加成功");location.href="'+reverse('myadmin_types_list')+'"</script>')


def list(request):

	tlist = getalltypes()
	# print(tlist)
	context = {'tlist':tlist}
	# 返回添加分类页面
	return render(request,'myadmin/types/list.html',context)



def delete(request):
	tid = request.GET.get('uid',None)

	# 判断当前类下是否有子类
	num = Types.objects.filter(pid=tid).count()
	if num != 0:
		data = {'msg':'当前类下有子类,不能删除','code':1}
	else:
		ob = Types.objects.get(id=tid)
		ob.delete()
		data = {'msg':'删除成功','code':0}
	return JsonResponse(data)


def edit(request):
	if request.method == 'GET':
		tlist = getalltypes()
		id = request.GET.get('id')
		ob = Types.objects.get(id=id)
		context = {'types':ob,'tlist':tlist}
		return render(request,'myadmin/types/edit.html',context)
	elif request.method == 'POST':
		ob = Types.objects.get(id=request.GET.get('id'))
		ob.name = request.POST['name']

		tid = request.GET.get('id')
		num = Types.objects.filter(pid=tid).count()
		if num != 0:
			return HttpResponse('<script>alert("该分类下有子分类，不能修改该类的父类");location.href="'+reverse('myadmin_types_list')+'"</script>')
		else:
			ob.pid = request.POST['pid']
			if ob.pid == '0':
				ob.path = '0,'
			else:
				# 根据当前父级id获取path，再添加父级id
				t = Types.objects.get(id=ob.pid)
				ob.path = t.path+str(t.id)+','
			ob.save()
			return HttpResponse('<script>alert("修改成功");location.href="'+reverse('myadmin_types_list')+'"</script>')



