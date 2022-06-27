import subprocess


def cmd_run(cmd):
    ret = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    print(ret)
    return ret
