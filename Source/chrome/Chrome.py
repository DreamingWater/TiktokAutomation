# Lenovo-"Xie Yan"
import subprocess
import threading
import psutil


# 随机选择语言
def random_choice_language():
    En_language_list = ['en-AU', 'en-CA', 'en-GB', 'en-IN', 'en-US']
    import random
    this_language = random.choice(En_language_list)
    return this_language

# 启动chrome线程
def run_chrome_thread(run_port: int):
    def google_thread():
        subprocess.run(
            # ["C:\Program Files\Google\Chrome\Application\chrome.exe", '--remote-debugging-port=%s' % run_port])
            ["D:\WorkingFiles\Chrome-bin\chrome.exe", '--remote-debugging-port=%s' % run_port,'--lang=%s' % random_choice_language()])

    t = threading.Thread(target=google_thread)
    t.daemon = True
    t.start()


def shut_chrome_thread(run_port: int):
    # 查找端口为 run_port 的进程
    for proc in psutil.process_iter():
        try:
            connections = proc.connections()
        except (psutil.AccessDenied, psutil.ZombieProcess):
            continue
        for conn in connections:
            if conn.laddr.port == run_port:
                proc.terminate()
