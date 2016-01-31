from django.conf.urls.defaults import *

urlpatterns = patterns('fm.views',
    #url(r'^admin/', include(admin.site.urls)),
    (r'^quizz$', 'quizz'),
    (r'^answer$', 'answer'),
    (r'^missions$', 'represent_data'),
    (r'^refresh$', 'refresh'),
    (r'^start$', 'start'),
    (r'^stop$', 'stop'),
    (r'^launch_missions$', 'launch_missions'),
    (r'^start_launch_missions$', 'start_launch_missions'),
    (r'^start_launch_missions_no_refresh$', 'start_launch_missions_no_refresh'),
    (r'^taxes$', 'taxes'),
    (r'^start_taxes$', 'start_taxes'),
    (r'^sale_airports$', 'sale_airports'),
    (r'^test$', 'test'),
)