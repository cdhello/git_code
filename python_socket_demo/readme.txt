学习python下的socket应用。

client与server端建立TCP连接，然后读取一个本地文件向server发送。server收到数据再回传给client。

下面是C/S两端都使用相同的Block/nonblock接口类型的数据对比
block接口

bufsize=10240
seconds: 2.454000, bytes: 6483058, rate: 2579.869605(KBs)

bufsize = 256
seconds: 47.036000, bytes: 6483058, rate: 134.599030(KBs)



nonblock

bufsize=10240
seconds: 2.049000, bytes: 6483058, rate: 3089.799865(KBs)

bufsize = 256
seconds: 8.328000, bytes: 6483058, rate: 760.206526(KBs)


window读写文件，如果不是文本文件一定要用b模式打开
