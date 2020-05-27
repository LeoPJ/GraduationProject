from pyecharts import options as opts
from pyecharts.charts import Bar
from pyecharts.faker import Faker




#cs
# ~ x=[]
# ~ for i in range(0,20):
	# ~ x.append(154/20*i)
# ~ x=[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
# ~ y=[854, 377, 319, 282, 360, 392, 597, 609, 392, 241, 206, 161, 165, 89, 70, 58, 39, 29, 32, 24]
# ~ length=154

#dt
# ~ x=[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
# ~ y=[2060, 628, 225, 249, 177, 86, 101, 74, 36, 72, 59, 48, 50, 62, 55, 80, 73, 51, 122, 137]
# ~ length=53

#dt_routelength
# ~ x=[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
# ~ y=[3257, 405, 292, 271, 142, 51, 12, 4, 4, 4, 1, 1, 0, 0, 0, 0, 0, 0, 0, 1]

#cs_routelength
# ~ x=[' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ',' ']
# ~ y=[1174, 614, 595, 937, 710, 453, 293, 213, 115, 86, 54, 24, 15, 3, 2, 4, 3, 0, 0, 1]


# ~ c = (
    # ~ Bar(init_opts=opts.InitOpts(width="900px", height="500px"))
    # ~ .add_xaxis(x)
    # ~ .add_yaxis("课程：大唐兴衰", y,category_gap=0,color='#C0C0C0')
    # ~ .set_global_opts(
        # ~ title_opts=opts.TitleOpts(title="用户观看视频覆盖范围分布"),
        # ~ xaxis_opts=opts.AxisOpts(name_location="end",name="视频数",name_gap=15,axistick_opts=opts.AxisTickOpts(is_show=False)),
        # ~ yaxis_opts=opts.AxisOpts(name_location="end",name="频数",name_gap=15)
        # ~ )
    # ~ .render("bar_base.html")
# ~ )
 # 纹理填充
    # color: {
    #    image: imageDom, // 支持为 HTMLImageElement, HTMLCanvasElement，不支持路径字符串
    #    repeat: 'repeat' // 是否平铺, 可以是 'repeat-x', 'repeat-y', 'no-repeat'
    # }

#dt
# ~ x=[1,2,3,4,5,6,7,8,9,10,11,12]
# ~ y=[564,313,276,201,205,197,191,216,146,154,138,153]

#cs
x=[1,2,3,4,5,6,7,8,9,10,11,12,13,14,15]
y=[211,287,147,402,273,213,163,134,206,178,219,141,186,157,41]


d= (
    Bar()
    .add_xaxis(x)
    .add_yaxis("课程：大学计算机基础", y,color='#C0C0C0')
    .set_global_opts(
        title_opts=opts.TitleOpts(title="低覆盖率学习者学习时间分布"),
        xaxis_opts=opts.AxisOpts(name_location="end",name="周次",name_gap=15),
        yaxis_opts=opts.AxisOpts(name_location="end",name="学习人数",name_gap=15)
        )
    .render("bbase.html")
)
