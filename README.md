# earthquake control site

This is a site prsent Taiwan Earthquake Information. You can see different kind of present chart, figure in this website.

All of Python package you need are in requirement.txt


## Celery beat 設定

Worker(RabbitMQ) 會執行在earth_control_site/celery.py中的task
當設定Celery定時任務時

### 先設定

當 Celery 設定完定時任務內容時 (ear_control_site/earth_control_site/celery.py), (ear_control_site/crawler/task.py)
記得將task註冊在 app.conf.update(CELERYBEAT_SCHEDULE) 中

如下所示

earth_control_site/celery.py
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
