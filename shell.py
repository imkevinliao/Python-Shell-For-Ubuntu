import re
import subprocess
import sys

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
            if stdout:
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
            log.info(info)
        stdout, stderr = process.communicate()
        ret = process.returncode
        log.info(f"Execute Command:{cmd}\nExecute status code: {ret}\n")
        if ret == 0:
            if stdout:
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
    config_source = ["sudo add-apt-repository ppa:deadsnakes/ppa -y",
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
    config_version = ["sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python3.10 1"]
    if python_version:
        config_version.append(
            f"sudo update-alternatives --install /usr/bin/python3 python3 /usr/bin/python{python_version} 0")
    else:
        log.info(f"没有获取到系统当前的python3版本")
    run(config_version)


def config_git():
    # 个人偏爱
    git_log_a = """git config --global alias.lg "log --no-merges --color --graph --date=format:'%Y-%m-%d %H:%M:%S'
    --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Cblue %s %Cgreen(%cd) %C(bold blue)<%an>%Creset' --abbrev-commit" """
    # 更详细
    git_log_b = """git config --global alias.lg "log --no-merges --color --stat --graph --date=format:'%Y-%m-%d
    %H:%M:%S' --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Cblue %s %Cgreen(%cd) %C(bold blue)<%an>%Creset'
    --abbrev-commit" """
    # 网上通常是这个
    git_log_c = """git config --global alias.lg --color --graph --pretty=format:'%Cred%h%Creset -%C(yellow)%d%Creset
    %s %Cgreen(%cd) %C(bold blue)<%an>%Creset' --abbrev-commit -- """
    
    config_alias = ['git config --global alias.gp pull',
                    'git config --global alias.br branch',
                    'git config --global alias.co checkout',
                    'git config --global alias.ci commit',
                    'git config --global alias.st status', git_log_a]
    config_user = ['git config --global user.name "imkevinliao"',
                   'git config --global user.email "imkevinliao@gmail.com"']
    config_editor = ['git config --global core.editor vim']
    cmds = []
    cmds.extend(config_alias)
    cmds.extend(config_user)
    cmds.extend(config_editor)
    popen(cmds)
    log.info(f"config git finished，please use command：<cat ~/.gitconfig> to check.")


if __name__ == '__main__':
    log = Log("shell.log")
    
