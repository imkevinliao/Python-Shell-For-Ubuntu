import re
import subprocess

from log import Log


def run(cmds):
    """
    cmds：
    传入参数类型 list 视为多条命令
    传入参数类型 str 视为一条命令
    """
    
    # 函数内定义函数原因：减少缩进层级
    def core(cmd):
        completed = subprocess.run(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        ret = completed.returncode
        stdout = completed.stdout
        stderr = completed.stderr
        log.info(f"Execute Command:{cmd}\nExecute status code: {ret}\n")
        if ret == 0:
            log.info(f"Output:{stdout}\n")
        else:
            log.error(f"Error:{stderr}\n")
    
    if isinstance(cmds, list):
        for _ in cmds:
            core(_)
    elif isinstance(cmds, str):
        core(cmds)


def popen(cmds):
    def core(cmd):
        process = subprocess.Popen(cmd, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE,
                                   stderr=subprocess.PIPE)
        for info in iter(process.stdout.readline()):
            print(info)
        stdout, stderr = process.communicate()
        ret = process.returncode
        log.info(f"Execute Command:{cmd}\nExecute status code{ret}\n")
        if ret == 0:
            log.info(f"Output:{stdout}\n")
        else:
            log.error(f"Error:{stderr}\n")
        process.kill()
    
    if isinstance(cmds, list):
        for _ in cmds:
            core(_)
    elif isinstance(cmds, str):
        core(cmds)


def config_python():
    """
    linux 下配置 sudo 免密，或者在 root 用户下执行
    """
    config_source = ["sudo add-apt-repository ppa:deadsnakes/ppa",
                     "sudo apt update -y",
                     "sudo apt install python3.10 -y"]
    run(config_source)
    check_version = ["python3 --version", "python --version", "py3 --version"]
    python_version = None
    for i in check_version:
        completed = subprocess.run(i, shell=True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        if completed.returncode == 0:
            _ = completed.stdout
            regex = r"3.\d+"
            match_result = re.search(regex, str(_))
            if match_result:
                python_version = match_result.group()
    config_version = ["sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 0"]
    if python_version:
        config_version.append(
            f"sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python{python_version} 1")
    else:
        log.info(f"没有获取到系统当前的python3版本")
    run(config_version)


if __name__ == '__main__':
    log = Log("shell.log")
    config_python()

