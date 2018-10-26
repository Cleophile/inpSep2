# 开发笔记
## Windows主语句
`.>sas.exe <input.inp> output.out`
## 设置文件传输
`self.didGenerateFiles = False`  
`transmit_button.clicked.connect(self.transmit_file)`  
`self.current_folder = filecount`  
## 杀死进程：
- 工作进程：由sas负责  
- || Daemon进程：计时，时间到的时候结束主进程 主进程顺利完成则重新计时（Deprecated）||  
UNIX __测试用__ `os.kill(int pid,signal.SIGKILL)`  
WINDOWS __实际__ `os.popen('taskkill.exe /pid:'+str(pid))`  
PYTHON __内部__ 由上述任意一个进程结束时发送signal 收到signal调用Thread子类stop方法  
*如何检测运行结束:* 每隔x秒查看这个进程是否存在  
## 其他注意:
用multi_processing  
用start开启进程 不能用run  
注意log文件的完整性，尤其注意超时杀死进程的记录的完整性  

## 创建文件夹路径
`os.path.join(path_initial,'{}'.format(folder_count))i`  
`self.current_folder_file_count = filecount 生成文件数`  
`self.path_initial = path_initial 工作目录 下面有123这样的目录`  
`self.result_path_full = result_path`  

