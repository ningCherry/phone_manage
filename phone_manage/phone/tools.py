import os
from ph_manage import settings

#文件上传
def upload_file(file=None):
    # 获取上传的文件file
    if file:
        filepathname = os.path.join(settings.MEDIA_ROOT, file.name)  # 拼接上传文件的路径
        filepath='/static/upload_img/'+file.name
        with open(filepathname, 'wb+') as pic:
            for c in file.chunks():  # 在file.chunks()上循环而不是用read()保证大文件不会大量使用系统内存
                pic.write(c)
        return filepath