from django.conf import settings
from django.conf.urls import patterns, url
from rest_framework.routers import DefaultRouter
from django.conf.urls.static import static

router = DefaultRouter()
urlpatterns = patterns(
    '',
    url(r'^test/', 'bms.views.test.test'),
    url(r'^test1/', 'bms.views.test.test1'),
    url(r'^test_template/', 'bms.views.test.test_template'),

    url(r'^index/', 'bms.views.usersview.index'),
    url(r'^login/', 'bms.views.usersview.login'),
    url(r'^logout/', 'bms.views.usersview.logout'),

    url(r'^wechat/', 'bms.views.wechat.wechat'),
    url(r'^pay/', 'bms.views.wechat.pay'),
    url(r'^pay_callback/', 'bms.views.wechat.pay_callback'),


    url(r'^get_business_list/', 'bms.views.business.business_list'),
    url(r'^business_info/', 'bms.views.business.create_business'),
    url(r'^modify_business_info/', 'bms.views.business.modify_business'),

    url(r'^get_machine_list/', 'bms.views.machine.machine_list'),
    url(r'^machine_info/', 'bms.views.machine.create_machine'),
    url(r'^modify_machine_info/', 'bms.views.machine.modify_machine'),

    url(r'^get_consume_list/', 'bms.views.consume.consume_list'),
    # url(r'^loginuserinfo','aws.views.usersview.userinfo'),


    # game views===============
    url(r'^game/$', 'bms.views.game.test'),
    url(r'^game/rank/', 'bms.views.game.get_rank'),
    url(r'^game/game_list/', 'bms.views.game.get_game_list'),
    url(r'^game/start/', 'bms.views.game.start_game'),
    url(r'^game/end/', 'bms.views.game.end_game'),
    url(r'^game/qrcode/', 'bms.views.game.get_qrcode'),

)

urlpatterns += router.urls
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
