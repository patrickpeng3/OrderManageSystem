import subprocess


def cmd_run(cmd):
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8")
    out, err = p.communicate()
    code = p.returncode
    return out, err, code
