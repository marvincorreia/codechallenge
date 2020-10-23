from django.utils import timezone
from os.path import join, isdir, dirname, isfile
from os import makedirs, remove, listdir
from random import randint
import subprocess
import logging
import shlex

logger = logging.getLogger(__name__)

""" {} will be replaced by path and filename
    cmd = command
    ext = file extension 
"""
VALID_LANGS = {
    'python': {
        'run_cmd': 'python "{path/filename}.py"',
        'ext': '.py'
    },
    # 'typescript': {'run_cmd': 'ts-node', 'ext': '.ts'},
    'javascript': {
        'run_cmd': 'node "{path/filename}.js"',
        'ext': '.js'
    },
    'c': {
        'run_cmd': '"{path/filename}"',
        'ext': '.c',
        'compile_cmd': 'gcc "{path/filename}.c" -o "{path/filename}"'
    },
    'java': {
        'run_cmd': 'java -cp "{path}" "{filename}"',
        'ext': '.java',
        'compile_cmd': 'javac "{path/filename}.java"'
    }
}


def create_source_file(path, filename, ext, code):
    if ext == '.java':
        code = class_refactor(code, filename)
    with open(join(path, filename + ext), mode='w')as fp:
        fp.writelines(code.split('\r'))


def class_refactor(code, filename):
    """ Ensure that the class name is equal a file name generated """
    old_class = code[0:code.index('{')][::-1].replace('\r\n', ' ').replace('\n', ' ').strip().split(' ')[0][::-1]
    return code.replace(old_class, filename)


def delete_runtime_files(path, filename):
    file_names = [f for f in listdir(path) if filename == f.split('.')[0]]
    for f in file_names:
        try:
            remove(join(path, f))
        except Exception as e:
            logger.error(str(e))


def valid_lang(lang) -> bool:
    return lang in VALID_LANGS


def get_run_cmd(lang) -> str:
    return VALID_LANGS[lang]['run_cmd']


def get_compile_cmd(lang) -> str:
    try:
        return VALID_LANGS[lang]['compile_cmd']
    except KeyError:
        return ''


def get_ext(lang) -> str:
    return VALID_LANGS[lang]['ext']


def generate_key() -> int:
    return randint(10000, 99999)


def generate_cmd(cmd, path, filename) -> str:
    # args = [join(path, filename) for _ in range(cmd.count('{}'))]
    # return cmd.format(*args)
    return cmd.replace('{path/filename}', join(path, filename)).replace('{filename}', filename).replace('{path}', path)


def run_subprocess(cmd) -> dict:
    cmd = shlex.split(cmd)
    process = subprocess.Popen(cmd, shell=False, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                               universal_newlines=True)
    try:
        stdout, stderr = process.communicate(timeout=10)
        if stderr:
            logger.error(stderr)
    except Exception as e:
        logger.error(str(e))
        stdout, stderr = "", f"ERROR: {e}"
    return dict(stdout=stdout, stderr=stderr)


def compile_and_run(compile_cmd, run_cmd) -> dict:
    compiler_output = run_subprocess(compile_cmd)
    if compiler_output['stderr']:
        return compiler_output
    else:
        return run_subprocess(run_cmd)


def runcode(code: str, lang: str) -> dict:
    if not valid_lang(lang):
        return dict(stdout="", stderr="ERROR: This programing language is not supported")
    now = timezone.now()
    path = join('submissions', str(now.year), str(now.month), str(now.day))
    if not isdir(path):
        makedirs(path)
    filename = "File" + f"{now.year}{now.month}{now.day}{now.hour}{now.minute}{now.second}"
    create_source_file(path, filename, get_ext(lang), code)
    if get_compile_cmd(lang):
        output = compile_and_run(
            compile_cmd=generate_cmd(get_compile_cmd(lang), path, filename),
            run_cmd=generate_cmd(get_run_cmd(lang), path, filename),
        )
    else:
        run_cmd = generate_cmd(get_run_cmd(lang), path, filename)
        output = run_subprocess(run_cmd)
    # delete_runtime_files(path, filename)
    return output
