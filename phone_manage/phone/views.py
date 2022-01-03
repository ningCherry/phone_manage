from django.shortcuts import render,redirect

# Create your views here.

from django.shortcuts import render
from django.http import *
from django.template import RequestContext,loader
from django.core.paginator import Paginator, PageNotAnInteger, InvalidPage, EmptyPage
from django.views.decorators.csrf import csrf_exempt
from django.contrib import messages
from django.core import serializers
from django.db.models import Q
from django.db import transaction

from .models import *
from phone.tools import *

import json
from datetime import datetime, time
from io import BytesIO
import xlwt
import xlrd

'''
知识点：
1、上传图片保存本地：https://www.cnblogs.com/cherry-ning/articles/12242615.html
2、{# 给class属性增加 required 必填#}： https://www.cnblogs.com/gcgc/p/14846072.html
3、警告弹窗：https://www.freesion.com/article/763357095/
4、使用模态框新增数据，成功后提示“提交成功”，并刷新表格bootstrap-table数据：https://www.cnblogs.com/gcgc/p/11176389.html
5、ajax交互，反显修改页的数据
6、django Q查询，https://www.cnblogs.com/huchong/p/8027962.html
7、Django中使用JS通过DataTable实现表格前端分页，https://www.likecs.com/show-64671.html
8、Django中获取URL路径参数(路径，查询，请求头，请求体)：https://www.cnblogs.com/fangyu-blog/p/14546934.html
9、文件的上传、下载，xlwt、xlrd
10、列表加上序号列


待研究
1、添加时，资产编号唯一，弹出提示框，并且停留在当前页面  ---需要请教大佬，不知道咋整
2、创建人 ---
3、图片覆盖上传 --
4、Select option默认选中及查询后选项值保留，https://www.pianshen.com/article/96241410655/  ---需要请教大佬，不知道咋整
5、注册
6、模块继承  --暂时没用上
7、记录倒序排序  --
8、加载本地绝对路径图片  --

9、django 前端使用ajax发送查询条件，后端查询并生成excel实现下载功能
https://blog.csdn.net/xiaogis/article/details/104763272/
https://blog.csdn.net/xiaotuwai8/article/details/108879129
9、django将table用excel导出
'''

def index(request):
    '''登录首页视图'''
    # temp=loader.get_template('booktest/index.html')  #加载模板
    # return HttpResponse(temp.render())   #将模板渲染出来
    users =LoginUser.objects.all()
    context={'users':users}
    return render(request,'phone/index.html',context)   #可以使用这一句代替上面注释的两行代码，即此行代码就是封装了上面两行代码

def login_action(request):
    '''登录操作'''
    # 接受请求信息
    post=request.POST
    username=post.get('form-username')
    password=post.get('form-password')
    # 根据用户名查询对象
    users = LoginUser.objects.filter(username=username)  #返回的是个列表[]
    # 判断：如果未查到则用户名错，如果查到则判断用户名是否正确，正确则转到用户中心
    if len(users)==1:
        if password==users[0].password:
            context = { 'name': username}
            return render(request,'phone/first_page.html',context)
        else:
            context = { 'error': '用户名或密码错误!', 'name': username}
            return render(request, 'phone/index.html', context)
    else:
        context = { 'error': '用户名不存在!', 'name': username}
        return render(request, 'phone/index.html', context)


def devices_list(request):
    """获取数据列表的视图"""
    devices = DeviceInfo.objects.order_by("-create_date")
    # print(devices)
    context = {'devices': devices}
    return render(request, 'phone/devices_list.html', context)

def first_page(request):
    return render(request, 'phone/first_page.html')


@csrf_exempt
def device_add(request):
    """增加记录的视图"""
    # 接受请求信息
    device_img1 = request.FILES.get('device_img')  # 获取上传的文件
    device_asset_img1 = request.FILES.get('asset_img')
    center_name1 = request.POST.get('center_name')
    device_name1 = request.POST.get('device_name')
    device_system1 = request.POST.get('device_system')
    device_factory1 = request.POST.get('device_factory')
    device_system_version1 = request.POST.get('device_system_version')
    device_asset_number1 = request.POST.get('device_asset_number')
    device_phone_number1 = request.POST.get('device_phone_number')
    device_recipient1 = request.POST.get('device_recipient')
    device_user1 = request.POST.get('device_user')
    creator1 = request.POST.get('creator')
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    device_asset_num=DeviceInfo.objects.filter(device_asset_num=device_asset_number1).count() #查找资产编号是否唯一
    if device_asset_num:
        re = "该资产编号已存在"
        messages.error(request, re)
        # return HttpResponse(json.dumps(re, ensure_ascii=False), content_type='application/json; charset=utf-8')
    else:
        DeviceInfo.objects.create(
            center_name=center_name1,
            device_name=device_name1,
            device_system=device_system1,
            device_factory=device_factory1,
            device_system_version=device_system_version1,
            device_asset_num=device_asset_number1,
            device_phone_num=device_phone_number1,
            device_recipient=device_recipient1,
            device_user=device_user1,
            creator=creator1,
            device_img=upload_file(device_img1),
            asser_img=upload_file(device_asset_img1),
            create_date=current_time,
            update_data=current_time

        )
        CirculationInfo.objects.create(
            device_asset_num=DeviceInfo.objects.filter(device_asset_num=device_asset_number1)[0],
            device_user=device_user1,
            handover_reason="创建",
            creator=creator1,
            created_date=current_time,
            update_data=current_time
        )
    return redirect('/devices_list')

@csrf_exempt
def get_device_by_id(request):
    """修改页面回显数据的视图"""
    json_dict = {}  # 先转成字典
    if request.is_ajax():
        device_id = request.POST.get("id")
        data = DeviceInfo.objects.get(id=device_id)
        json_dict['device_id'] = data.id
        json_dict["center_name"] = data.center_name
        json_dict['device_name'] = data.device_name
        json_dict['device_system'] = data.device_system
        json_dict['device_factory'] = data.device_factory
        json_dict['device_system_version'] = data.device_system_version
        json_dict['device_asset_number'] = data.device_asset_num
        json_dict['device_phone_number'] = data.device_phone_num
        json_dict['device_recipient'] = data.device_recipient
        json_dict['device_user'] = data.device_user
        json_dict['creator'] = data.creator
        return JsonResponse(json_dict, content_type='application/json; charset=utf-8')

@csrf_exempt
def device_update(request):
    """修改的视图"""
    center_name1 = request.POST.get('u_center_name')
    device_id1 = request.POST.get('u_device_id')
    device_name1 = request.POST.get('u_device_name')
    device_system1 = request.POST.get('u_device_system')
    device_factory1 = request.POST.get('u_device_factory')
    device_system_version1 = request.POST.get('u_device_system_version')
    device_asset_number1 = request.POST.get('u_device_asset_number')
    device_phone_number1 = request.POST.get('u_device_phone_number')
    device_recipient1 = request.POST.get('u_device_recipient')
    creator1 = request.POST.get('u_creator')
    device_img1 = request.FILES.get('device_img')
    asset_img1 = request.FILES.get('asset_img')

    nowTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')

    if device_img1 is not None and asset_img1 is not None:
        DeviceInfo.objects.filter(id=device_id1).update(
            center_name=center_name1,
            device_name=device_name1,
            device_system=device_system1,
            device_factory=device_factory1,
            device_system_version=device_system_version1,
            device_asset_num=device_asset_number1,
            device_phone_num=device_phone_number1,
            device_recipient=device_recipient1,
            creator=creator1,
            update_data=nowTime,
            device_img=upload_file(device_img1),
            asser_img=upload_file(asset_img1)
        )
    elif device_img1 is not None:
        DeviceInfo.objects.filter(id=device_id1).update(
            center_name=center_name1,
            device_name=device_name1,
            device_system=device_system1,
            device_factory=device_factory1,
            device_system_version=device_system_version1,
            device_asset_num=device_asset_number1,
            device_phone_num=device_phone_number1,
            device_recipient=device_recipient1,
            creator=creator1,
            update_data=nowTime,
            device_img=upload_file(device_img1),
        )
    elif asset_img1 is not None:
        DeviceInfo.objects.filter(id=device_id1).update(
            center_name=center_name1,
            device_name=device_name1,
            device_system=device_system1,
            device_factory=device_factory1,
            device_system_version=device_system_version1,
            device_asset_num=device_asset_number1,
            device_phone_num=device_phone_number1,
            device_recipient=device_recipient1,
            creator=creator1,
            update_data=nowTime,
            asser_img=upload_file(asset_img1),
        )
    else:
        DeviceInfo.objects.filter(id=device_id1).update(
            center_name=center_name1,
            device_name=device_name1,
            device_system=device_system1,
            device_factory=device_factory1,
            device_system_version=device_system_version1,
            device_asset_num=device_asset_number1,
            device_phone_num=device_phone_number1,
            device_recipient=device_recipient1,
            creator=creator1,
            update_data=nowTime,
        )
    return redirect('/devices_list')

devices_dic = {}
query_list = []

@csrf_exempt
def search(request):
    """搜索的视图"""
    center_name = request.GET.get("q_center_name")
    print(type(center_name))
    print(center_name)
    device_name = request.GET.get('q_device_name')
    device_system = request.GET.get('q_device_system')
    device_factory = request.GET.get('q_device_factory')
    device_system_version = request.GET.get('q_device_system_version')
    device_asset_num = request.GET.get('q_device_asset_number')
    device_phone_num = request.GET.get('q_device_phone_number')
    device_recipient = request.GET.get('q_device_recipient')
    device_user = request.GET.get('q_device_user')
    devices_dic["center_name"] = center_name
    devices_dic["device_name"] = device_name
    devices_dic["device_system"] = device_system
    devices_dic["device_factory"] = device_factory
    devices_dic["device_system_version"] = device_system_version
    devices_dic["device_asset_number"] = device_asset_num
    devices_dic["device_phone_number"] = device_phone_num
    devices_dic["device_recipient"] = device_recipient
    devices_dic["device_user"] = device_user

    # if set(devices_dic.values()) == {''}:
    if devices_dic.values() is None:
        return redirect("/devices_list")
    else:
        query = Q(device_name__contains=devices_dic["device_name"]) & Q(
            device_system__contains=devices_dic["device_system"]) & Q(
            device_factory__contains=devices_dic["device_factory"]) & Q(
            device_system_version__contains=devices_dic["device_system_version"]) & Q(
            device_asset_num__contains=devices_dic["device_asset_number"]) & Q(
            device_phone_num__contains=devices_dic["device_phone_number"]) & Q(
            device_recipient__contains=devices_dic["device_recipient"]) & Q(
            device_user__contains=devices_dic["device_user"]) & Q(
            center_name__contains=devices_dic["center_name"])

        devices_sets = DeviceInfo.objects.filter(query)
        content={"devices":devices_sets,"devices_dic":devices_dic}
        return render(request, 'phone/devices_list.html',content)


@csrf_exempt
def handover(request):
    """流转视图"""
    nowTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    device_id = request.POST.get('h_device_id')
    handover_user = request.POST.get("device_user")
    handover_reason = request.POST.get("handover_reason")
    creator = request.POST.get("handover_creator")
    device_asset_num = DeviceInfo.objects.get(id=device_id).device_asset_num
    device_user = DeviceInfo.objects.get(id=device_id).device_user
    if handover_user != device_user:
        CirculationInfo.objects.create(
            device_asset_num=DeviceInfo.objects.filter(device_asset_num=device_asset_num)[0],
            device_user=handover_user,
            handover_reason=handover_reason,
            creator=creator,
            created_date=nowTime,
            update_data=nowTime,
        )
        DeviceInfo.objects.filter(id=device_id).update(
            device_user=handover_user,
            update_data=nowTime,
        )
    else:
        CirculationInfo.objects.create(
            device_asset_num=DeviceInfo.objects.filter(device_asset_num=device_asset_num)[0],
            device_user=device_user,
            handover_reason="创建",
            creator=creator,
            created_date=nowTime,
            update_data=nowTime,
        )
    return redirect('/devices_list')


@csrf_exempt
def handover_record(request,device_id):
    """流转记录视图"""
    device = DeviceInfo.objects.get(id=device_id)
    record = CirculationInfo.objects.filter(device_asset_num=device)
    return render(request, 'phone/handover_record.html', {"record": record})


@csrf_exempt
def detail(request,device_id):
    """设备详情视图"""
    device = DeviceInfo.objects.get(id=device_id)
    return render(request, 'phone/device_detail.html', {"device": device})


@csrf_exempt
def file_down(request):
    """下载模板的视图"""
    file_name = "device_template.xlsx"  # 文件名
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))  # 项目根目录
    file_path = os.path.join(base_dir, 'upload', 'export_template', file_name)  # 下载文件的绝对路径

    def file_iterator(file_path, chunk_size=512):
        """
        文件生成器,防止文件过大，导致内存溢出
        :param file_path: 文件绝对路径
        :param chunk_size: 块大小
        :return: 生成器
        """
        with open(file_path, mode='rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    # 设置响应头
    # StreamingHttpResponse将文件内容进行流式传输，数据量大可以用这个方法
    response = StreamingHttpResponse(file_iterator(file_path))
    # 以流的形式下载文件,这样可以实现任意格式的文件下载
    response['Content-Type'] = 'application/octet-stream'
    # Content-Disposition就是当用户想把请求所得的内容存为一个文件的时候提供一个默认的文件名
    response['Content-Disposition'] = 'attachment;filename="{}"'.format(file_name)
    return response


@csrf_exempt
def export_excel(request):
    """导出记录的视图"""
    device_li = DeviceInfo.objects.order_by("-update_data")  #查询库里所有数据

    # 设置HTTPResponse的类型
    response = HttpResponse(content_type='application/vnd.ms-excel')
    response['Content-Disposition'] = 'attachment;filename=device_data.xls'
    """导出excel表"""
    if device_li:
        # 创建工作簿
        ws = xlwt.Workbook(encoding='utf-8')
        # 添加第一页数据表
        w = ws.add_sheet('sheet1')  # 新建sheet（sheet的名称为"sheet1"）
        # 写入表头
        w.write(0, 0, u'所属中心')
        w.write(0, 1, u'设备名称')
        w.write(0, 2, u'设备系统')
        w.write(0, 3, u'厂商')
        w.write(0, 4, u'系统版本')
        w.write(0, 5, u'资产编号')
        w.write(0, 6, u'手机号码')
        w.write(0, 7, u'出库领取人')
        w.write(0, 8, u'使用人')
        w.write(0, 9, u'创建人')
        # 写入数据
        excel_row = 1
        for obj in device_li:
            center_name = obj.center_name
            device_name = obj.device_name
            device_system = obj.device_system
            device_factory = obj.device_factory
            device_system_version = obj.device_system_version
            device_asset_number = obj.device_asset_num
            device_phone_number = obj.device_phone_num
            device_user = obj.device_user
            device_recipient = obj.device_recipient
            creator = obj.creator
            # created_date = obj.create_date
            # modified_date = obj.update_data
            w.write(excel_row, 0, center_name)
            w.write(excel_row, 1, device_name)
            w.write(excel_row, 2, device_system)
            w.write(excel_row, 3, device_factory)
            w.write(excel_row, 4, device_system_version)
            w.write(excel_row, 5, device_asset_number)
            w.write(excel_row, 6, device_phone_number)
            w.write(excel_row, 7, device_recipient)
            w.write(excel_row, 8, device_user)
            w.write(excel_row, 9, creator)
            excel_row += 1
        # 写出到IO
        output = BytesIO()
        ws.save(output)
        # 重新定位到开始
        output.seek(0)
        response.write(output.getvalue())
    return response


@csrf_exempt
def upload_device(request):
    """文件上传"""
    nowTime = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    if request.method == 'POST':
        f = request.FILES.get('file')
        excel_type = f.name.split('.')[-1]
        if excel_type in ['xls']:
            # 开始解析上传的excel表格
            wb = xlrd.open_workbook(filename=None, file_contents=f.read())
            table = wb.sheets()[0]
            rows = table.nrows  # 总行数
            for i in range(1, rows):
                row_values = table.row_values(i)
                if (row_values[0] != "" and row_values[1] != "" and row_values[2] != "" and row_values[
                    3] != "" and row_values[4] != "" and row_values[5] != "" and row_values[7] != "" and
                        row_values[8] != ""):
                    pass
                else:
                    return JsonResponse("第" + str(i) + "行除手机号外其余项均不能为空", safe=False,
                                        json_dumps_params={'ensure_ascii': False})
            with transaction.atomic():  # 控制数据库事务交易
                for j in range(1, rows):
                    row_values = table.row_values(j)
                    device_asset_num = row_values[5]
                    device_phone_num = row_values[6]
                    if isinstance(device_asset_num, str):
                        device_asset_num = device_asset_num
                    elif isinstance(device_asset_num, float) and device_asset_num.is_integer():
                        device_asset_num = int(float(device_asset_num))
                    else:
                        pass
                    if device_phone_num == "" or device_phone_num == "无":
                        device_phone_numb = "无"
                    elif isinstance(device_phone_num, str):
                        device_phone_num = device_phone_num
                    elif isinstance(device_phone_num, float):
                        device_phone_num = int(float(device_phone_num))
                    else:
                        pass
                    device_by_asset_num = DeviceInfo.objects.filter(
                        device_asset_num=device_asset_num)
                    if device_by_asset_num.exists():
                        #使用JsonResponse都需要添加 json_dumps_params={'ensure_ascii':False} 否则显示不是UTF-8格式.
                        # 如果是列表格式，使用JsonResponse，需要添加safe=False
                        return JsonResponse("资产编号%s已存在" % (device_asset_num), safe=False,
                                            json_dumps_params={'ensure_ascii': False})
                    else:
                        DeviceInfo.objects.create(center_name=row_values[0],
                                                     device_name=row_values[1],
                                                     device_system=row_values[2].lower(),
                                                     device_factory=row_values[3],
                                                     device_system_version=row_values[4],
                                                     device_asset_num=device_asset_num,
                                                     device_phone_num=device_phone_num,
                                                     device_recipient=row_values[7],
                                                     device_user=row_values[8],
                                                     creator=row_values[7],
                                                     create_date=nowTime,
                                                     update_data=nowTime
                                                     )
                        CirculationInfo.objects.create(
                            device_asset_num=DeviceInfo.objects.filter(device_asset_num=device_asset_num)[0],
                            device_user=row_values[8],
                            creator=row_values[7],
                            created_date=nowTime,
                            update_data=nowTime
                        )
        else:
            return JsonResponse("文件类型错误", safe=False, json_dumps_params={'ensure_ascii': False})
    return redirect('/devices_list')
