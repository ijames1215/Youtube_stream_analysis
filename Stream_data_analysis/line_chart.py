import matplotlib.pyplot as plt
from matplotlib.font_manager  import *
import pandas as pd
import numpy as np
from matplotlib.ticker import MultipleLocator
import time
myfont = FontProperties(fname='./msjhbd.ttc')
######設置error_bad_lines=False來忽略字段錯誤########

avg = ['TOP1','TOP2','TOP3','TOP4']
cat = ['Education','Entertainment','Game','Movie']
for int_width,num in enumerate(cat):
    # for top in avg:
        data = pd.read_csv(r'./Final/cat/{}.csv'.format(num), encoding='utf-8', error_bad_lines=False)
        #data = pd.read_csv(r'./data/{}/row_data_avg_{}_v2.csv'.format('cat','top5'),encoding='utf-8',error_bad_lines=False)
        #data.to_csv(r'./data/row_data_avg_{}.csv'.format('top'),encoding='utf-8-sig')
        ######只取流量數值的欄位############
        data_column = list(data.columns[10::])
        print(data_column)
        # ########每六小時計算一次流量#######
        # column=[]
        # for i in range(12,len(data_column),6):
        #     column.append(list(data.columns)[i])
        # print(column)
        # ######################取每三列流量的資料
        # row_data = list(data[column].iloc)
        # print(row_data)
        #########計算發片時間點#########
        data_list = list(data[data_column].iloc)
        count = list(range(0,24))  ;  count=[0 if x != 0 else x for x in count]
        count_2 = []
        for n in range(len(data_list)):
            data_TF = list(data_list[n].isnull())
            if data_TF[0] == True:
                # if data_TF[-1] == False:
                #     print(n)
                    count_2.append(n)
                    for count_time,m in enumerate(data_TF):
                        if m == False:
                            count_time = count_time % 24
                            count[count_time] += 1
                            break
                        else:
                            pass
            else:
                continue
        time_count = []
        time_oclock = []
        for time,final_count in enumerate(count):
            time_count.append(final_count)
            time_oclock.append(time)
            print('第',time,'時有',final_count,'個')
        # print(count_2)
        print(time_count)
        n = 24
        time_= np.arange(n)
        plt.xticks(time_oclock)
        # plt.ylim((0, 700))
        plt.xlabel('發片時間點(時)',fontproperties=myfont, fontsize=15)
        plt.ylabel('影片發佈量(部)',fontproperties=myfont, fontsize=15)
        plt.bar(time_oclock,time_count,align='center',color='darkorange',label= num +' '+ 'Category')#, time_+(-0.4+int_width*0.2),
        ax = plt.subplot(111)
        ax.xaxis.set_tick_params(labelsize = 14)
        ax.yaxis.set_tick_params(labelsize=14)
        # 添加数据标签
        for a, b in zip(time_oclock, time_count):
            if b !=0 :
                plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=8)
        # plt.xticks(time) # x軸刻度
        # plt.gca().yaxis.set_major_locator(MultipleLocator(50))
        # plt.ylim((0, 800))
        plt.legend(loc='upper right')
        plt.gcf().set_size_inches(15, 6)
        plt.title("影片發布時間點分析",fontproperties=myfont, fontsize=15)
        plt.gcf().savefig('./Final/cat_image/{}/{}.png'.format(num, num + '_hist'))
        plt.show()

# #####開始畫圖######
# data = []
# for i in range(len(data_TF)):
#     if data_TF[0] == True:
#         if data_TF[-1] == False:
#             data.append(i)

