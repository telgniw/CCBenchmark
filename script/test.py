from common import MyProcess
p = MyProcess(url='/myblob/init', args={'num':1, 'size':100})
p.start()
p.join()
