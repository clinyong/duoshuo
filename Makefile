export SHELL := /bin/bash

.PHONY: start stop restart clean

supervisor_conf := conf/supervisor.conf

supervisord:
	mkdir -p log
	supervisord -c $(supervisor_conf)

start:
	supervisorctl -c $(supervisor_conf) start duoshuo

stop:
	supervisorctl -c $(supervisor_conf) stop duoshuo

restart: stop start

clean:
	rm -rf log
