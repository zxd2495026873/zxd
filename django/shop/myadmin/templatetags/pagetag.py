from django.utils.html import format_html

# 为了成为一个有效的标签库，模块必须包含一个名为register的模块级变量，
# 	该变量是一个template.Library实例，其中注册了所有标签和过滤器
from django import template
register = template.Library()

# 自定义页面优化显示标签

# 自定义简单标签
@register.simple_tag
def PageShow(count,request):
	# 获取请求的页数，没有则赋值为1
	p = int(request.GET.get('p',1))

	# 开始页数
	begin = p - 4
	# 结束页数
	end = p + 5


	# 页码默认显示10页

	# 判断页数大小
	# 	如果小于5，起始页为1，结束页为10
	if p < 5:
		begin = 1
		end = 10
	# 	如果当前页大于 总页数-5，起始页为count-9,结束页为count
	if p > count - 5:
		begin = count - 9
		end = count
	# 	如果开始页小于等于0，则开始页为1
	if begin <= 0:
		begin = 1

	# 拼接当前请求的参数
	u = ''
	for x in request.GET:
		# 排除p参数
		if x != 'p':
			u += '&' + x + '=' + request.GET[x]

	# 拼接页码列表
	s = ''

	# 拼接首页和上一页
	s += '<li><a href="?p=1'+u+'">首页</a></li>'
	if p - 1 <= 0:
		s += '<li class="am-disabled"><a href="?p=1'+u+'">上一页</a></li>'
	else:
		s += '<li><a href="?p='+str(p-1)+u+'">上一页</a></li>'

	# 遍历拼接中间页码
	for x in range(begin,end+1):
		# 判断是否为当前页
		if p == x:
			s += '<li class="am-active"><a href="?p='+str(x)+u+'">'+str(x)+'</a></li>'
		else:
			s += '<li><a href="?p='+str(x)+u+'">'+str(x)+'</a></li>'

	# 拼接尾页和下一页
	if p+1 >= count:
		s += '<li class="am-disabled"><a href="?p='+str(count)+u+'">下一页</a></li>'
	else:
		s += '<li><a href="?p='+str(p+1)+u+'">下一页</a></li>'
	s += '<li><a href="?p='+str(count)+u+'">尾页</a></li>'

	# 直接返回s不行，s中的特殊符号会被转义，所以要用format_html()转换一下
	return format_html(s)