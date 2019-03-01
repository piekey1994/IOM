import xiaoiceapi 
import multiprocessing
xb = xiaoiceapi.xiaoiceApi()

def task(param):
    try:
        print(param+':'+str(xb.chat(param)))
    except Exception as e:
        print(e)

if __name__=='__main__': 
    pool = multiprocessing.Pool(processes=4) # 创建4个进程
    text=['','你在哪呀','我想你了','你快回来']
    for i in range(4):
        param=text[i]
        pool.apply_async(task, (param,))
    pool.close() # 关闭进程池，表示不能在往进程池中添加进程
    pool.join() # 等待进程池中的所有进程执行完毕，必须在close()之后调用
    print("所有进程已完成.开始写回···")