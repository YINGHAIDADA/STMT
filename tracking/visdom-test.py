
import visdom
import torch as t
 
vis = visdom.Visdom(env=u'test', use_incoming_socket=True)
 
# 绘制三角函数
x = t.arange(1, 30, 0.01)
y = t.sin(x)
vis.line(X=x, Y=y, win='sinx', opts={'title': 'y=sin(x)'})
 
# append 追加数据
for ii in range(0, 10):
    # y = x
    x = t.Tensor([ii])
    y = x
    vis.line(X=x, Y=y, win='polynomial', update='append' if ii > 0 else None)
 
# updateTrace 新增一条线
x = t.arange(0, 9, 0.1)
y = (x ** 2) / 9
vis.line(X=x, Y=y, win='polynomial', name='this is a new Trace', update='new')
 
# 可视化一个随机的黑白图片
vis.image(t.randn(64, 64).numpy())
 
# 随机可视化一张彩色图片
vis.image(t.randn(3, 64, 64).numpy(), win='random2')