# 简易任务队列 - Python
# 测试用例：包含并发安全问题、性能问题、可维护性差

import threading
import time
import sqlite3

class TaskQueue:
    def __init__(self):
        self.tasks = []
        self.db = sqlite3.connect('tasks.db', check_same_thread=False)
        self.db.execute('CREATE TABLE IF NOT EXISTS tasks (id INTEGER PRIMARY KEY, name TEXT, status TEXT)')

    def add_task(self, name):
        # 添加任务到队列
        self.tasks.append({'name': name, 'status': 'pending'})
        # 同时写入数据库
        self.db.execute(f"INSERT INTO tasks (name, status) VALUES ('{name}', 'pending')")
        self.db.commit()

    def process_next(self):
        # 处理下一个任务
        if len(self.tasks) > 0:
            task = self.tasks[0]
            task['status'] = 'processing'

            # 模拟任务处理
            time.sleep(1)

            task['status'] = 'done'
            # 从列表中移除
            self.tasks.pop(0)

            # 更新数据库
            self.db.execute(f"UPDATE tasks SET status = 'done' WHERE name = '{task['name']}'")
            self.db.commit()
            return task
        return None

    def get_pending_count(self):
        count = 0
        for task in self.tasks:
            if task['status'] == 'pending':
                count += 1
        return count

    def retry_all_failed(self):
        # 重试所有失败的任务
        for task in self.tasks:
            if task['status'] == 'failed':
                task['status'] = 'pending'


def worker(queue, worker_id):
    while True:
        task = queue.process_next()
        if task is None:
            break
        print(f"Worker {worker_id} processed: {task['name']}")


if __name__ == '__main__':
    queue = TaskQueue()

    # 添加 100 个任务
    for i in range(100):
        queue.add_task(f'task_{i}')

    # 启动 5 个工作线程
    threads = []
    for i in range(5):
        t = threading.Thread(target=worker, args=(queue, i))
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    print(f"Remaining tasks: {len(queue.tasks)}")

# 测试用例说明：
# P0 问题：
# 1. 并发安全问题：多线程下 self.tasks 的读写没有锁，会出现竞态条件
# 2. SQL 注入：数据库查询使用字符串拼接
# 3. 同一个任务可能被多个线程同时处理（pop(0) 不是原子操作）
#
# P1 问题：
# 1. 性能问题：get_pending_count 每次都遍历整个列表，O(n) 复杂度
# 2. 每次处理任务都 sleep(1)，没有区分任务复杂度
# 3. 没有错误处理，任务失败了也不会标记
# 4. SQLite 在多线程下的 check_same_thread=False 有风险
#
# P2 问题：
# 1. 命名不清晰（task 到底是 dict 还是什么）
# 2. 没有类型注解
# 3. 魔法数字（100、5、1 等）
# 4. 没有测试
