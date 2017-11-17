from ift import IFT
from objects import Point

ift = IFT(1, 3, 0.01, 1.4)
pnt3 = Point(ift, M=1.53, theta=12, x=0.69, y=0.62, gamma=1.4)
pnt6 = Point(ift, M=1.53, theta=0, x=1.08, y=0, gamma=1.4)

pnt7 = Point(ift, a=pnt6, b=pnt3, gamma=1.4)

print(pnt7.set_all())
