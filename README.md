## 前言

当有新评论的时候，多说是不会自动推送的，这样子要自己经常登录多说的后台查看，很不方便，所以自己写了这个自动推送的脚本。

使用前，请确保已经安装了[requests](http://docs.python-requests.org/en/latest/)这个库，没有的话可以通过[pip](https://pip.pypa.io/en/latest/)安装

```
$ pip install requests
```

## 配置

通过`duoshuo.conf`这个文件进行配置

### duoshuo

有两个参数需要填写，可以从后台的设置那里看到

![](http://ww2.sinaimg.cn/large/71d1a325jw1eopj9nio4lj21go0wyq7j.jpg)

`short_name`是上图中的名称，这里是`leodots`。`secret`是图中的密钥。

### email

`host`：smtp邮箱的主机地址，我这里用的是126的邮箱

`name`：邮箱的名称，比如我是`leo@126.com`，则名称是`leo`

`password`：邮箱的密码

`to`：要发给哪个邮箱

`from`：从哪个邮箱发送

比如从`a@126.com`发到`b@163.com`，则`to`填的是`b@163.com`，`from`填写`a@126.com`

### others

只有一个参数，设置每隔多长时间检查一次评论数，单位是秒
