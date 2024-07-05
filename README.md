# 智能备忘录应用
智能备忘录能够根据用户输入随意的自然语言，让 LLM 整理出需要提醒用户的多项备忘事项以及对应时间。提醒事项会记录在UI界面上，同时也可在reminder.txt文件中查看。
## 使用方式

### 方式一
在自己电脑上部署代码：
1.从Github上下载代码：
```
git clone https://github.com/ChenYvyv/Reminder.git
```
2.环境配置
根据代码仓库中yaml文件创建环境
```
conda create -n env-name -f environment.yaml
conda activate env-name
```
3.运行代码
```
python train.py
```
### 方式二
直接使用打包的exe文件
2.1获取exe文件
```
git clone https://github.com/ChenYvyv/Reminder.git
```
2.2运行exe文件


