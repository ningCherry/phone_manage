from django.conf.urls import include,url
from . import views

urlpatterns=[
    url(r'^index/',views.index), #当匹配成功后，调用views.login视图
    url(r'^login_action/',views.login_action),
    url(r'^devices_list/',views.devices_list),
    url(r'^first_page/',views.first_page),
    url(r'^device_add/$',views.device_add),
    url(r'^get_device_by_id$',views.get_device_by_id),
    url(r'^device_update/$',views.device_update),
    url(r'^search/',views.search),
    url(r'^handover/',views.handover),
    url(r'^handover_record/(\d+)/$',views.handover_record),
    url(r'^detail/(\d+)/$',views.detail),
    url(r'^file_down/$',views.file_down),
    url(r'^export_excel/$',views.export_excel),
    url(r'^upload_device/$',views.upload_device),

    # url(r'^(\d+)$',views.detail)  #(\d+)即取id值
]

