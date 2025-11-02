import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from scipy.stats import chi2_contingency
from scipy.stats import chi2
###通过pandas导入数据
data = pd.read_csv(r"C:\study\project\cookie_cats.csv",encoding = 'utf-8')
print(data)
###检查数据是否有na值或者重复行
data_na_count = data.isnull().sum(axis = 0)
print(data_na_count)
print(data.duplicated().sum())
###发现数据没有na值以及重复行
###我们存在一个困难门关卡，当前该关卡设置在第三十关，而我们当前问题是我们是否应该将困难门关卡设置在第四十关
###当前困难门设置在第三十关存在一个问题，那就是可能会导致新手玩家因为困难关卡的早早到来而导致游戏难度提升而难以通关，从而流失短期玩家
###但如果困难门设置在第四十关可能会导致长期玩家已经适应了关卡而不进行内购道具来通关而导致流水下降，以及可能出现长期玩家流失的现象
###所以我们需要考虑的问题是改变困难门的位置会导致短期玩家与长期玩家的留存率发生怎样的变化，再对流水问题进行分析
###而当前我们所需要考虑的仅仅只是改变困难门的位置会导致玩家留存率发生怎样的变化
###当前，我们先计算各个参数值的大小
control_group = data[data['version'] == 'gate_30']
treatment_group = data[data['version'] == 'gate_40']
retention_1_count1_pct = control_group['retention_1'].mean()
retention_1_count2_pct = treatment_group['retention_1'].mean()
retention_7_count1_pct = control_group['retention_7'].mean()
retention_7_count2_pct = treatment_group['retention_7'].mean()
retention_1_count1 = control_group['retention_1'].sum()
retention_1_count2 = treatment_group['retention_1'].sum()
retention_7_count1 = control_group['retention_7'].sum()
retention_7_count2 = treatment_group['retention_7'].sum()
###计算完参数后，我们可以通过图表来对数据进行分析
fig,axes = plt.subplots(2,2)
axes[0,0].plot(['gata_30','gata_40'],[retention_1_count1_pct,retention_1_count2_pct])
axes[0,0].yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
axes[0,0].set_ylim(0.4,0.5)
###我们可以看到一条极为平缓的斜线，我们可以从中得知困难门位置的设立不同造成短期玩家的留存率的改变是极小的
###所以我们提出零假设:困难门位置的设立对短期玩家的留存率没有影响
###同时提出备择假设:困难门位置的设立对短期玩家的留存率存在影响
###我们假设零假设是成立的情况下，计算出p值
len1 = len(control_group)
retention_1_count1_contra = len1 -retention_1_count1
len2 = len(treatment_group)
retention_1_count2_contra = len2 - retention_1_count2
arr1 = np.array([retention_1_count1,retention_1_count1_contra,retention_1_count2,retention_1_count2_contra]).reshape(2,2)
percent_avg = (retention_1_count1_pct +retention_1_count2_pct) / 2
retention_1_count1_exp = int(len1 * percent_avg)
retention_1_count1_contra_exp = len1 - retention_1_count1_exp
retention_1_count2_exp = int(len2 * percent_avg)
retention_1_count2_contra_exp = len2 - retention_1_count2_exp
arr1_exp = np.array([retention_1_count1_exp,retention_1_count1_contra_exp,retention_1_count2_exp,retention_1_count2_contra_exp]).reshape(2,2)
print(arr1)
chi2_1 = ((arr1 - arr1_exp) ** 2 / arr1_exp).sum()
print(chi2_1)###3.176
###自由度 = (2 - 1) * (2 - 1) =  1
p_value1 = chi2.sf(chi2_1,1)
print(p_value1)###0.0747
###接下来我们使用scipy库来一步算出卡方值与p值并对我们上面所算出来的值进行对比
contingency_table = pd.crosstab(data['version'],data['retention_1'])
print(contingency_table)
chi2_2,p_value2,dof,expected = chi2_contingency(contingency_table,correction = False)
print(chi2_2,p_value2,dof)
###得到chi2_2 = 3.182,p_value2 = 0.0744
###两个方式的卡方值与p值都近乎相等，所以所得结果无误
###最终我们算出p值大于0.05，所以我们没有足够的证据证明零假设是错误的
###所以我们可以先认为困难门位置的改变对短期玩家的留存率没有影响


###在验证完困难门的位置与短期玩家的留存率的相关性之后，我们开始验证困难门的位置与长期玩家留存率的关系了
###我们先试用图表来看清实验组与对照组留存率的变化
axes[0,1].plot(['gata_30','gata_40'],[retention_7_count1_pct,retention_7_count2_pct])
axes[0,1].set_ylim(0.15,0.25)
axes[0,1].yaxis.set_major_formatter(mtick.PercentFormatter(1))
plt.show()
###根据图表我们可以看到长期玩家留存率斜线是比短期玩家留存率斜线更斜一点，但是仍然无法看出明显倾斜，并且留存率存在着下降趋势
###所以我们可以提出零假设:困难门的位置的设立并不会对长期玩家的留存率产生影响
###我们在假设零假设成立的情况下，对p值进行计算
###接下来我们进行p值计算
retention_7_count1_contra = len1 -retention_7_count1
retention_7_count2_contra = len2 - retention_7_count2
arr1 = np.array([retention_7_count1,retention_7_count1_contra,retention_7_count2,retention_7_count2_contra]).reshape(2,2)
percent_avg = (retention_7_count1_pct +retention_7_count2_pct) / 2
print(percent_avg)
retention_7_count1_exp = int(len1 * percent_avg)
retention_7_count1_contra_exp = len1 - retention_7_count1_exp
retention_7_count2_exp = int(len2 * percent_avg)
retention_7_count2_contra_exp = len2 - retention_7_count2_exp
arr1_exp = np.array([retention_7_count1_exp,retention_7_count1_contra_exp,retention_7_count2_exp,retention_7_count2_contra_exp]).reshape(2,2)
print(arr1)
print(arr1_exp)
chi2_3 = ((arr1 - arr1_exp) ** 2 / arr1_exp).sum()
print(chi2_3)
###我们得出k值为10.0221
###自由度 = (2 - 1) * (2 - 1) = 1
p_value3 = chi2.sf(chi2_3,1)
print(p_value3)
###得出p值为0.0015
###我们再用scipy内置函数一步算出卡方值与p值在于我们得到的值进行对比
contingency_table2 = pd.crosstab(data['version'],data['retention_7'])
chi2_4,p_value4,dof4,expection2 = chi2_contingency(contingency_table2,correction = False)
print(chi2_4,p_value4)
###得到chi2_4 = 10.0131,p_value4 = 0.0015
print(p_value4 - p_value3)
###比较得手动算出结果与函数算出结果近乎相等
###所以因为 p 值 < 0.05,所以我们有证据拒绝原假设
###所以最后我们可以认为困难门位置的设立与长期玩家留存率存在着负面影响
print(retention_7_count1_pct - retention_7_count2_pct)#0.008
###我们得到位置的改变使留存率下降了0.8%
###最终我们得到结论，当困难门的位置从第三十关变到第四十关时，短期玩家留存率不会受到影响，而长期玩家留存率会下降
###最后，我们根据结论，决定保持原困难门的位置来确保玩家的留存率不会下降

###预测出现这样的结果的原因:
###因短期玩家无论哪种门槛的设立位置都没有打到付费门槛所以门槛的设立与短期玩家留存率无关，
###而如果设立在四十关长期玩家已经习惯了没有付费门槛而当突然有付费门槛时造成了心理预期不符不愿接受改变而造成留存率下降
###但如果将门槛设置在三十关玩家还没适应时再遇到付费门槛会比较容易接受改变
###这样子的心理预期的变化导致了留存率的下降问题



