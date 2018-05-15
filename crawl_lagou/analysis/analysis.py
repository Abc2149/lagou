import pymysql
from collections import Counter
import pygal
import os


# 连接mysql
db = pymysql.Connect(
    host='127.0.0.1',
    port=3306,
    user='root',
    passwd='root',
    db='lagouspider',
    charset='utf8',
)
# 操作游标
cursor = db.cursor()

def getdata(filed):
    sql = "select %s from lagou" % filed
    cursor.execute(sql)
    # 返回查询到的所有记录(元组类型)
    data = cursor.fetchall()
    # 统计相同字段值出现的次数
    count = dict(Counter(each[0] for each in data))     # {'本科'：44}
    return count



# 柱状
def get_city():
    bar_chart = pygal.Bar()
    bar_chart.title = '技术类前20城市的招聘数量'
    city = sorted(getdata('city').items(),key=lambda x:x[1] ,reverse=True)
    for i in range(20):
        bar_chart.add(city[i][0],city[i][1])
    bar_chart.render_to_file(os.path.dirname(__file__)+'/chart/city.svg')

# 饼图
def get_workyear():
    pie_chart = pygal.Pie()
    pie_chart.title = '对工作经验的要求'
    workyear = sorted(getdata('workYear').items(),key=lambda x:x[1] ,reverse=True)
    for i in range(len(workyear)):
        pie_chart.add(workyear[i][0],workyear[i][1])
        pie_chart.render_to_file(os.path.dirname(__file__)+'/chart/workyear.svg')

if __name__ == '__main__':
    get_city()
    get_workyear()













