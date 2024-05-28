import time
import tkinter as tk
import json
from tkinter import messagebox
import os
from openai import OpenAI
# OpenAI.api_key = 'sk-YmOk1UMQHErq6q8NgCGjVTH0VYLadBLRU27E9OWJCrFkFqEl'

client = OpenAI(
    api_key="sk-YmOk1UMQHErq6q8NgCGjVTH0VYLadBLRU27E9OWJCrFkFqEl",
    base_url="https://api.chatanywhere.tech/v1"
)


def generate_reminders_from_prompt(input_text):
    t=time.localtime()
    cu_time=str(t.tm_year)+"-"+str(t.tm_mon)+"-"+str(t.tm_mday)+" "+str(t.tm_hour)+":"+str(t.tm_min)
    system_message={
        "role":"system",
        "content":
    f'''
        你是一个助手，帮助用户生成备忘事项。
        请从文本中提取备忘事项并根据当前时间计算出备忘事项的时间，然后以 JSON 格式返回，请不要添加其他任何无关内容。
        返回的 JSON 格式示例：
        [{{"任务": "去买菜", "时间": "2024-05-25 10:00:00"}},
        {{"任务": "开会", "时间": "2024-05-25 14:00:00"}}]
        
    '''
            # 请注意需要生成具有换行和缩进的正确JSON格式,确保生成内容能成功被json.loads()调用
            #"你是一个助手，帮助用户生成备忘事项。请从文本中提取备忘事项并根据当前时间计算出备忘事项的时间，然后以 JSON 格式返回。返回的 JSON 格式示例：[{{‘任务’: ‘去买菜’, ‘时间’: ‘2024-05-25 10:00:00’}},{{‘任务’: ‘开会’, ‘时间’: ‘2024-05-25 14:00:00’}}]"
    }
    user_message={
        "role":"user",
        "content":cu_time+input_text
    }
    messages=[system_message,user_message]
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",  # 根据需要选择合适的模型
        messages=messages,
    )

    # 解析 API 返回的结果
    try:
        content = response.choices[0].message.content
        reminders = json.loads(content)
        return reminders
    except json.JSONDecodeError:
        # print(json.JSONDecodeError)
        return []


# 函数：将备忘事项保存到 txt 文件
def save_reminders_to_txt(reminders, filename):
    with open(filename, 'w') as file:
        for reminder in reminders:
            file.write(f"{reminder['任务']}，{reminder['时间']}\n")


# 函数：从 txt 文件读取备忘事项
def read_reminders_from_txt(filename):
    reminders = []
    with open(filename, 'r') as file:
        lines = file.readlines()
        for line in lines:
            parts = line.strip().split('，')
            if len(parts) == 2:
                reminder = {
                    '任务': parts[0].strip(),
                    '时间': parts[1].strip()
                }
                reminders.append(reminder)
    return reminders


# 函数：处理生成备忘事项按钮点击事件
def handle_generate_reminders():
    input_text = text_input.get("1.0", tk.END).strip()
    if not input_text:
        messagebox.showwarning("输入错误", "请输入一些文本")
        return

    reminders = generate_reminders_from_prompt(input_text)
    save_reminders_to_txt(reminders, 'reminders.txt')
    display_reminders()


# 函数：显示备忘事项
def display_reminders():
    read_reminders = read_reminders_from_txt('reminders.txt')
    reminders_list.delete(0, tk.END)
    for reminder in read_reminders:
        reminders_list.insert(tk.END, f"任务：{reminder['任务']}，时间：{reminder['时间']}")


# 创建主窗口
root = tk.Tk()
root.title("备忘事项管理")

# 创建文本输入框
text_input = tk.Text(root, height=10, width=50)
text_input.pack(pady=10)

# 创建按钮的 Frame
button_frame = tk.Frame(root)
button_frame.pack(pady=5)

# 创建生成按钮
generate_button = tk.Button(button_frame, text="生成备忘事项", command=handle_generate_reminders)
generate_button.pack(side=tk.LEFT, padx=5)

# 创建关闭按钮
close_button = tk.Button(button_frame, text="关闭", command=root.quit)
close_button.pack(side=tk.LEFT, padx=5)

# 创建显示备忘事项的列表框
reminders_list = tk.Listbox(root, width=50, height=10)
reminders_list.pack(pady=10)

# 启动应用程序
root.mainloop()
handle_generate_reminders()

