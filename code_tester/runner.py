from django.utils import timezone
from os.path import join, isdir, dirname
from os import makedirs, remove
from random import randint
import subprocess
import logging

VALID_LANGS = {
    'python': {'ext': '.py', 'cmd': 'python'},
    # 'typescript': {'ext': '.ts', 'cmd': 'ts-node'},
    'javascript': {'ext': '.js', 'cmd': 'node'}
}


def create_runtime_file(path, filename, code):
    with open(join(path, filename), mode='w')as fp:
        fp.writelines(code.split('\r'))


def delete_runtime_file(path, filename):
    try:
        remove(join(path, filename))
    except Exception as e:
        logging.getLogger(__name__).error(str(e))


def valid_lang(lang):
    return lang in VALID_LANGS


def get_cmd(lang):
    return VALID_LANGS[lang]['cmd']


def get_ext(lang):
    return VALID_LANGS[lang]['ext']


def generate_key():
    return randint(10000, 99999)


def run_subprocess(*args):
    process = subprocess.Popen(args, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               universal_newlines=True)
    try:
        stdout, stderr = process.communicate(timeout=10)
    except Exception as e:
        logging.getLogger(__name__).error(str(e))
        stdout, stderr = "", f"ERROR: {e}"
    return dict(stdout=stdout, stderr=stderr)


def runcode(code: str, lang: str):
    if not valid_lang(lang):
        return dict(stdout="", stderr="ERROR: This programing language is not supported")
    now = timezone.now()
    path = join(dirname(__file__), 'submitions', str(now.year), str(now.month), str(now.day))
    if not isdir(path):
        makedirs(path)
    filename = f"{now.year}-{now.month}-{now.day}-{now.hour}-{now.minute}-{now.second}{get_ext(lang)}"
    create_runtime_file(path, filename, code)
    output = run_subprocess(get_cmd(lang), join(path, filename))
    # delete_runtime_file(path, filename)
    return output
