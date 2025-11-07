import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
data = pd.read_csv(r"C:\study\project\ecommerce_customer_data_large.csv",encoding = 'utf-8')
#pd.set_option('display.max_columns',None)
print(data)
data['Purchase Date'] = pd.to_datetime(data['Purchase Date'])
data['single_price'] = data['Product Price'] * data['Quantity']
###首先对数据进行填充缺失值
###查看缺失值在各特征中的分布
num_na = data.isna().sum()
print(num_na)
# row_na = data[data['Returns'].isna()]

# print(row_na)
# print(data['Returns'])


###根据缺失值所在列的总体比例来对缺失值根据比例进行随机填充


def fill_with_proportion(data,feature):
    data_with_na = data[data[feature].isna()][feature]
    data_with_no_na = data[feature].dropna()
    nums_na = len(data) - len(data_with_no_na)
    proportion1 = sum(data_with_no_na == 1) / len(data_with_no_na)
    print(proportion1)
    proportion2 = 1 - proportion1
    fillna_num = np.random.choice([0,1],nums_na,p = [proportion1,proportion2])
    index_mask = data[feature].isna()
    fillna_data = data.copy()
    fillna_data.loc[index_mask,feature] = fillna_num
    return fillna_data
data = fill_with_proportion(data,'Returns')
print(data.isna().sum())
data = data.drop_duplicates()
data['AgeGroup'] = pd.cut(data['Customer Age'],bins = [17,25,35,45,55,65,101],labels = ['17-24','25-34','35-44','45-54','55-64','65-100'])
print(data)
# # ###在处理完缺失值之后将数据导出并使用mysql进行将数据变得更有条理
# data.to_csv(r"C://study/project/data_anlysis.csv")

###通过mysql进行处理后，使用pandas进行导入
data2 = pd.read_csv(r"C:\Users\awa\Desktop\.vs\无标题.csv",encoding = 'utf-8')
#print(data2)


###将mysql所得数据进行可视化分析


def visible_data(data):
    total_money = data.groupby('agegroup')['total_money'].sum()
    fig,axes = plt.subplots(2,2,figsize = (10,8))
    axes[0,0].bar(total_money.index,total_money.values)
    #plt.show()
    ###由可视化图表可知，年龄在24-64之间的客户总消费量相似，且都占总额大头，所以我们需要着重把产品像成年化发展，面向成年以及中年客户
    total_customer = data.groupby('agegroup')['total_customer'].sum()
    single_money = total_money / total_customer
    axes[0,1].bar(single_money.index,single_money.values)
    #plt.show()
    ###通过图表我们可以得知各个年龄段的客户的客单价都是相近的，所以成交数量成为了总销售额的关键指标，我们应该将产品向销售数量的增加为目标前进
    # male_cost = data[data['Gender'] == 'Male'].set_index('agegroup')['total_money']
    # female_cost = data[data['Gender'] == 'Female'].set_index('agegroup')['total_money']
    pivot_data = data.pivot(index = 'agegroup',columns = 'Gender',values = 'total_money')
    pivot_data.plot(kind = 'bar',color = ['green','red'],ax = axes[1,0])
    ###通过图表我们可以发现男女的消费情况近似相等，所以我们的产品收到男女平等的喜爱，不要做出会让其中一方反感的事便能维持这样的平衡
    # axes[1,0].bar(male_cost.index,male_cost,color = 'red')
    # axes[1,0].bar(female_cost.index,female_cost,color = 'green')
    data_copy = data.copy()
    data_copy['each_money'] = data['total_money'] / data['total_customer']
    pivot_data2 = data_copy.pivot(index = 'agegroup',columns = 'Gender',values = 'each_money')
    pivot_data2.plot(kind = 'bar',color = ['blue','black'],ax = axes[1,1])
    ###男女之间的客单价也相似
    plt.show()
#visible_data(data2)


###使用FRM思想对客户进行分箱打分


def calculate_rfm_scores(data,current_date = None):
    if current_date == None:
        current_date = data['Purchase Date'].max()

    rfm_table = data.groupby('Customer ID').agg({
        'Purchase Date': lambda X: (current_date - X.max()).days,
        'Product Price': 'count',
        'single_price' : 'sum'
    }).rename(columns = {
        'Purchase Date': 'Recency',
        'Product Price': 'Frequency',
        'single_price' : 'total_money'
    })
    rfm_table = rfm_table[rfm_table['Frequency'] > 0] & rfm_table[rfm_table['total_money'] > 0]
    rfm_table['Recency_score'] = pd.qcut(rfm_table['Recency'],5,labels = [5,4,3,2,1])
    rfm_table['Frequency_score'] = pd.qcut(rfm_table['Frequency'],5,labels = [1,2,3,4,5])
    rfm_table['total_money_score'] = pd.qcut(rfm_table['total_money'],5,labels = [1,2,3,4,5])
    print(rfm_table)
    return rfm_table
data_score = calculate_rfm_scores(data)


###根据客户的分数对客户进行分类


def segment_customers(data):
    def assign_segment(row):
        r,f,t = row['Recency_score'],row['Frequency_score'],row['total_money_score']
        if r >= 4 and f>=4 and t >= 4:
            return '高级客户'
        elif r >= 4 and f <= 2 and t <= 2:
            return '新客户'
        elif r <= 2 and f >= 4 and t >= 3:
            return '沉睡忠诚用户'
        elif r <= 3 and f <= 3 and t >= 4:
            return '高价值用户'
        elif r >= 3 and f >= 3 and t >= 3:
            return '一般价值用户'
        elif r <= 2 and f <= 2 and t <= 2:
            return '流失用户'
        else:
            return '一般用户'

    data['segment'] = data.apply(assign_segment,axis = 1)
    return data
data_segment = segment_customers(data_score)


###对所得分类客户数据进行分析


def analysis_customers(data):
    customers_data = data.groupby('segment').agg({
        'Recency':'mean',
        'Frequency':'mean',
        'total_money':'sum',
        'Recency_score':'count'
    }).rename(columns = {'Recency_score':'total_customers'})
    print(customers_data)
    total_num = customers_data['total_customers'].sum()
    customers_data['propotion_num'] = customers_data['total_customers']/total_num * 100
    customers_data['single_value'] = customers_data['total_money']/customers_data['total_customers']
    return customers_data
data_analysis = analysis_customers(data_segment)
#print(data_analysis.sort_values(by = 'total_money',ascending = True))


###根据不同类别的客户指定不同的策略以提高营业额


def generate_strategies(analysis_data):
    strategies ={
        '高级客户':{
            '策略':'给予特殊特权与权限',
            '目的':'增添高级客户的粘性，增添高级客户的价值，让其他用户向往高级客户',
            '具体措施':'提供专属客服，优先解决客户问题，获取优先访问权',
            '预算分配':'高'
        },
        '新客户':{
            '策略':'培育关系，提高购买率',
            '目的':'转化为忠诚客户',
            '具体措施':'发放优惠卷，开启第二件半价的活动',
            '预算分配':'中'
        },
        '沉睡忠诚客户':{
            '策略':'召回活动',
            '目的':'对客户进行召回，恢复购买行为',
            '具体措施':'第一款商品半价，发放优惠卷，新品通知',
            '预算分配':'中'
        },
        '高价值客户':{
            '策略':'让其对商品感兴趣',
            '目的':'提升购买率',
            '具体措施':'向其推荐自家商品特点，新品特点',
            '预算分配':'中高'
        },
        '一般价值用户':
            {
                '策略':'让其注意到商品',
                '目的':'转化为高级客户',
                '具体措施':'发放优惠卷，开启促销活动，首页推荐',
                '预算分配':'中下'
            },
        '一般用户':
            {
                '策略': '让其注意到商品',
                '目的': '转化为高级客户',
                '具体措施': '发放优惠卷，开启促销活动，首页推荐',
                '预算分配': '中下'
            },
        '流失客户':{
            '策略':'让其注意到商品',
            '目的':'转化为一般价值客户',
            '具体措施':'开启召回活动商品半价，发放优惠卷',
            '预算分配':'下'
        }
    }

    return strategies[analysis_data]
#strategy = generate_strategies(data2.index[0])
#print(strategy)
pd.set_option('display.max_columns',None)
print(data_analysis)


###制定总体报告


def generate_report(data):
    total_customers = data['total_customers'].sum()
    total_money = data['total_money'].sum()
    high_value_radio = data.loc['高级客户','propotion_num']
    avg_customer_value = total_money / total_customers
    print(f"当前总共有{total_customers}名客户,总营业额为{total_money}")
    print(f"其中高级用户所占的比例为{high_value_radio:.0f}")
    print(f"平均每位用户消费{avg_customer_value:.0f}")
    print(f"总共有{data.index.tolist()}用户级别分类")
    print(f"建议基于各种用户的级别分类，实施不同的策略以提升营业额")
generate_report(data_analysis)


###对各类别客户数据进行可视化分析


def visible_analysis(data):
    segment = data.index
    print(segment)
    propotion = data['propotion_num']
    plt.rcParams['font.sans-serif'] = ['SimHei', 'Microsoft YaHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    fig,axes = plt.subplots(2,2,figsize = (15,12))
    colors = plt.cm.viridis(np.linspace(0,1,len(segment)))
    axes[0,0].bar(segment,propotion / 100,color = colors)
    axes[0,0].set_title('各类用户占比情况')
    axes[0,0].yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    for i in range(len(segment)):
        axes[0,0].text(segment[i],propotion.iloc[i] / 100 + 0.01,f"{propotion[i]:.0f}%",ha = 'center')
    ###我们可以看到普通用户的占比高达百分之四十二，而新用户的占比为百分之8,所以我们要尽力去留住普通用户，否则一旦流失将会造成较大影响
    each_money = data['total_money']
    axes[0,1].bar(segment,each_money,color = colors)
    axes[0,1].set_title('各类用户消费情况')
    for seg,money in zip(segment,each_money):
        axes[0,1].text(seg,money + 0.5,f"{money/10000:.1f}万",ha = 'center')
    ###可以看到高级用户的销售金额高达五千万，而普通用户则高达四千万，所以我们应当以普通用户与高级用户为主，实施不同策略，分配较高预算
    money_propotion = data['total_money'] / data['total_money'].sum()
    axes[1,0].bar(segment,money_propotion,color = colors)
    axes[1,0].set_title('各类用户消费金额占比情况')
    axes[1, 0].yaxis.set_major_formatter(mtick.PercentFormatter(1))
    for seg,value in zip(segment,money_propotion):
        axes[1,0].text(seg,value+0.01,f"{value * 100 :.0f}%",ha = 'center')
    ###可以看到一般客户与高级客户的消费总额占比总和为百分之六十八，所以我们要主要专注于这两类客户，确保其不会流失
    budget_allocation = [5,5,8,10,6,15,20]
    expected_improved = [10,10,15,20,10,15,20]
    axes[1,1].bar(segment,budget_allocation,color = colors)
    axes[1,1].plot(segment,expected_improved)
    axes[1,1].set_title('各类用户策略预算与预期提升效果')
    for seg,budget,improve in zip(segment,budget_allocation,expected_improved):
        axes[1,1].text(seg,budget+0.5,f"{budget}w",ha = 'center')
        axes[1,1].text(seg,improve+0.5,f"{improve}%",ha = 'center')
    fig.suptitle('各类用户情况可视图')
    plt.show()
visible_analysis(data_analysis)
###前百分之二十消费客户的消费金额所占总消费金额比例：
propotion = data_score[data_score['total_money_score'] == 5]['total_money'].sum() / data_score['total_money'].sum()
print(propotion)
###占比为37%
###整个项目我们完成了对数据的清洗，使用mysql进行选取数据，使用RFM对用户的距离上一次购买的天数，购买频率以及成交金额进行分箱打分
###然后再根据打分来分类出用户类别
###再根据不同的类别制定专属的策略与活动
###最后再从整体上的数据进行分析，绘制可视图来观察各个数据差异以及占比
###通过可视图来获得某些结论
###比如：高级客户与一般客户的消费总额占总体的68%
###所以需要重点把握住这两种类别客户，制定特殊策略，分拨较高预算，最后具体实施策略以确保销售额稳定上涨