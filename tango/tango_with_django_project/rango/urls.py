from django.conf.urls import url,patterns
from rango import views

urlpatterns = patterns('',
	url(r'^$',views.index,name='index'),
	url(r'^about/',views.about,name='about'),
	url(r'^category/(?P<category_name_slug>[\w\-]+)/add_page/$',views.add_page,name='add_page'),
	url(r'^category/(?P<category_name_slug>[\w\-]+)/$',views.category,name='category'),
	url(r'^add_category/$',views.add_category,name='add_category'),
	url(r'^goto/(?P<page_id>[\w\-]+)$',views.track_url,name='goto')
	)