import asyncio
import pandas as pd
import random

async def task(index, name):
    # 模拟异步操作（例如 I/O 操作）
    print(f"Task {name} is running")
    tt = random.randint(0,9)
    await asyncio.sleep(tt)  # 模拟异步等待，这里改为1秒以加快演示速度
    print(f"{index} Task {name} is done")
    return index, f"{index} 任务{name}, {tt}完成"

async def main():
    result_df = pd.read_csv("../resources/download_info.csv")
    result_df['ind'] = None
    result_df['result'] = None
    # 创建任务列表
    tasks = []
    for i in range(len(result_df)):  # 确保创建7个任务
        name = result_df["file_name"][i]
        if len(name) >= 50:
            result_df.loc[i, 'ind'] = i
            result_df.loc[i, 'result'] = name
            continue
        # 创建一个协程对象并将其添加到列表中
        task_coroutine = task(i, name)
        task_obj = asyncio.create_task(task_coroutine)
        tasks.append(task_obj)
    
    # 等待所有任务完成，并收集返回值
    results = await asyncio.gather(*tasks)
    
    # 打印每个任务的返回值
    for index, result in results:
        result_df.loc[index, 'ind'] = index
        result_df.loc[index, 'result'] = result
        
    result_df.to_csv("./asyncio_test.csv", index=False)

if __name__ == "__main__":
    # 运行异步主函数
    asyncio.run(main())