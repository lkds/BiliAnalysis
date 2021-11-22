from data import read_danmu
from calculate import cal

progress, danmu = read_danmu('data\BV19v411M7Rs\[CURR]BV19v411M7Rs_1.csv')
res = cal(danmu)
print(res)