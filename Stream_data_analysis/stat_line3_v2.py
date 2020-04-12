import matplotlib.pyplot as plt
from matplotlib.font_manager import *
import statistics
import pandas as pd
import numpy as np
import math
from matplotlib.ticker import MultipleLocator, FuncFormatter
myfont = FontProperties(fname='./msjhbd.ttc')
######設置error_bad_lines=False來忽略字段錯誤########
avgs = ['TOP1','TOP2','TOP3','TOP4','TOP5']
cat = ['ent','edu','game','movie']
for num in avgs:
    data = pd.read_csv(r'./Final/avg/{}.csv'.format(num),encoding='utf-8',error_bad_lines=False)
    # data.to_csv(r'./rowdata_0216_v2.csv'.format(''),encoding='utf-8-sig',index=False)
    ######只取流量數值的欄位############
    data_column = list(data.columns[10::])
    print(data_column)

    #########計算時間點流量#########
    data_list = list(data[data_column].iloc)
    count_1 = []; list1 = [] ; list2 = [] ; stream_column = []  ##list2 = [[第i筆,哪一個時間點開始有流量,各時段的流量...]]

    for n in range(len(data_list)):
        data_TF = list(data_list[n].isnull())
        list1.append(str(n + 1))
        for add_time, m in enumerate(data_TF):
            try:
                if m == False:
                    list1.append(data_column[add_time])
                    break
            except Exception:
                pass
        if data_TF[0] == True:
            if data_TF[-1] == False:
                count_1.append(n)

        for add_time, m in enumerate(data_TF):
            try:
                if add_time > 0:
                    add_hour = data_column[add_time - 1]
                    add_hour2 = data_column[add_time]
                    list1.append(str(data_list[n][add_time] - data_list[n][add_time - 1]))
            except Exception as e:
                continue
        list2.append(list1)
        list1 = []
    ############建立流量欄位############
    for stream in range(len(data_TF)):
        if stream > 0:
            add_hour = data_column[stream - 1]
            add_hour2 = data_column[stream]
            stream_column.append(add_hour.split('2020')[1].split(' ')[0] + add_hour.split(' ')[1] + "~" +
                                 add_hour2.split(' ')[1])
            continue

    stream_column = ['number','Post_time'] + stream_column
    ############流量資料合併###########
    dflist = pd.DataFrame(list2,columns=stream_column)
    dflist.to_csv(r'./stream.csv',encoding='utf-8-sig',index=False)
    data_columns = list(dflist.columns[2::])
    row_data = list(dflist[data_columns].iloc)
    list3 = [] ; list4 = [] ; list5 = []
    ############流量格式轉換##############
    for jj in count_1:
        try:
            stream_2 = list2[jj]
            list3.append(stream_2[1].split(" ")[1])
            # print(stream_2)
            list3.append(0)
            for jjj in range(2,len(dflist.columns)):
                try:
                    if stream_2[jjj] == "nan":
                        list3.append(int(stream_2[jjj-1].split(".")[0]))
                        pass
                    else:
                        list5.append(jj)
                        if int(stream_2[jjj].split(".")[0]) >= 0:
                            list3.append(int(stream_2[jjj].split(".")[0]))
                        else:
                            list3.append(0)
                except :
                    pass
        except:
            pass
        list4.append(list3)
        list3 = []
    for nums in range(len(list4)):
        if len(list4[nums]) <= 719:
            for num1 in range(719-len(list4[nums])):
                list4[nums].append(float('nan'))
        else:
            pass
    avg = [];temp_avg = []
    for int_avg_pass_time in range(1,len(list4[1])-100):
        for int_avg in range(len(list4)):
            filter = list4[int_avg][int_avg_pass_time]
            if math.isnan(filter) != True:
                temp_avg.append(list4[int_avg][int_avg_pass_time])
                pass
            else:
                pass
        avg.append(int(statistics.mean(temp_avg)))
        temp_avg = []
        ###############發片時間點欄位轉換###########
    post_time = [] ;post_time_24 = []
    for post in range(0,len(list4[1])-1):
        posts = str(post)+'H'
        post_time.append(posts)
        if post % 24 ==0 :
            post_24 = str(post)+'H'
        post_time_24.append(post_24)
    ############畫折線圖###############
    # list6 = []
    # for qq in range(0,10):
    #     list6.append("0"+str(qq))
    # for qqq in range(10,24):
    #     list6.append(str(qqq))
    # for sss in list6:
    #     print(sss)
    # temp=[]
    # for sss in list6:
    #     for ss in range(len(list4)):
    #          if list4[ss][0] == sss:
    #########################################avg_1_24#####################################
    ax = plt.subplot(111)
    xmajorLocator = MultipleLocator(24)
    ax.xaxis.set_major_locator(xmajorLocator)
    plt.rcParams.update({'figure.max_open_warning': 0})
    plt.gca().yaxis.set_major_locator(MultipleLocator(1000))
    plt.xlabel('發片經過時間(時)',fontproperties=myfont, fontsize=15)
    plt.ylabel('平均流量(觀看次數)',fontproperties=myfont, fontsize=15)
    plt.plot(post_time[:289], avg[:289],label= num +'  ' + 'category')
    plt.legend(loc='upper right')
    plt.fill_between(post_time[:289],0,avg[:289] , facecolor = "lightsalmon", interpolate= True, alpha=0.6)
    plt.ylim((0, 24000))
    plt.title("影片發布流量高峰期",fontproperties=myfont, fontsize=15)
    plt.gcf().savefig('./Final/avg_image/{}/{}.png'.format(num, num + '_line3'))
    plt.show()
