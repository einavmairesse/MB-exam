from subprocess import Popen, PIPE


def run_gcp_command(command, *args):
    command = ['python', '../google_cloud.py', command, *args]

    stdout, stderr = Popen(command, stdout=PIPE, stderr=PIPE).communicate()

    if stderr != b'':
        return False, stderr
    else:
        return True, stdout
