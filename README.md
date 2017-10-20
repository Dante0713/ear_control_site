# earthquake control site

This is a site prsent Taiwan Earthquake Information. You can see different kind of present chart, figure in this website.

All of Python package you need are in requirement.txt


## 初步 Django 觀念
大家對MVC都有一定的概念
但Django這邊是以MTV為使用方式
M: model
T: template
V: view


以網頁呼叫一個指令的順序來說
Django Framework:

    網址列輸入網址 => url.py => views.py => model.py => SQL, SQLite3, MySQL
    SQL, SQLite3, MySQL => model.py => views.py => url.py => 網頁

而目前本站使用 Django Rest Framework 順序會有一點點不同，後面會提到

### url.py 做了什麼?

我們先在網址欄上打上 our_domain/index.html 開啟了一個叫做 index.html 的網頁
會從 django_project/project_name/url.py 當中
看有沒有一個叫做 /index 的 url 指令
去執行 views.def_name 當中指定的資料表現方式

```python
	from app_name import views
```

####對應範例: 
our_domain => localhost or 127.0.0.1
django_project/project_name/url.py => ear_control_site/ear_control_site/url.py
views.def_name => views.EarthquakeList
/index => /earthquakes/

ear_control_site/ear_control_site/url.py
```python
	...
	from ear_info import views

	urlpatterns = [
		...
		url(r'^earthquakes/$', views.EarthquakeList),
		...
	]
	...
```

#### 

接下來看看 views.py 裡面做了什麼
ear_control_site/ear_info/views.py

## Celery beat 設定

Worker(RabbitMQ) 會執行在ear_control_site/celery.py中的task
當設定Celery定時任務時

### 先設定

當 Celery 設定完定時任務內容時 (ear_control_site/ear_control_site/celery.py), (ear_control_site/crawler/task.py)
記得將task註冊在 app.conf.update(CELERYBEAT_SCHEDULE) 中

如下所示

ear_control_site/celery.py
```python
	...

	app.conf.update(
		CELERYBEAT_SCHEDULE={
			'per5minute': {
				'task': 'tasks.crawing_job', # register here
				'schedule': timedelta(seconds=300),
				'args': (phantomjs_path,db_path)
			}
		}
	)
	@app.task(name='tasks.crawing_job') # task name mark here
	def crawing_job(phantomjs_path, db_path):
		job(phantomjs_path, db_path)
		return ' crawling_job run success. '

	...
```


### 啟動方式

啟動 Worker 時，記得 Broker要先啟動，

步驟如下

1. Start RabbitMQ
2. 啟動 Celery Worker
3. 有定時任務再開啟 Celery beat
4. 有flower介面監控worker再開啟flower

順序如下

```Bash
$celery -A ear_control_site -l INFO worker
$celery -A ear_control_site -l INFO beat
$celery flower -A ear_control_site --address=127.0.0.1 --port=5555
```
	
	=> 開啟RabbitMQ
	=> 開啟worker
	=> 開啟beat
	=> 開啟flower監控worker

TODO LIST: 
1. db item lg, lt, scale, deep change to integer item
2. fix model type, celery job input, recrawling data
3. show_map.html, widget_page.html need search function pull search result into chart.js, googlemapapi.js
4. save widget order into backend
5. rwd
6. accout control, user group, group auth