from django.utils import timezone
from os.path import join, isdir, dirname, isfile
from os import makedirs, remove, listdir, removedirs
from random import randint
from subprocess import PIPE, Popen
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
    with open(join(path, filename + ext), mode='w', encoding='UTF-8')as fp:
        fp.writelines(code.split('\r'))


def class_refactor(code, filename):
    """ Ensure that the class name is equal a file name generated """
    try:
        old_class = code[0:code.index('{')].split()[-1]
        return code.replace(old_class, filename, 1)
    except ValueError:
        return code


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


def need_compile(lang):
    return get_compile_cmd(lang)


def make_paths() -> tuple:
    now = timezone.now()
    path = join('submissions', str(now.year), str(now.month), str(now.day))
    if not isdir(path):
        makedirs(path)
    filename = "File" + f"{now.year}{now.month}{now.day}{now.hour}{now.minute}{now.second}"
    return path, filename


def generate_cmd(cmd, path, filename) -> str:
    return cmd.replace('{path/filename}', join(path, filename)).replace('{filename}', filename).replace('{path}', path)


def run_subprocess(socket, cmd, _input=None) -> dict:
    cmd = shlex.split(cmd)
    if not _input:
        _input = "\n".join([f"'MISSING-INPUT-{x}'" for x in range(1, 21)])
    else:
        _input += '\n' if _input[-1] is not '\n' else ''

    _subprocess = Popen(cmd, shell=False, stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
    socket.subprocess = _subprocess
    try:
        stdout, stderr = _subprocess.communicate(timeout=5, input=_input)
        if stderr:
            logger.error(stderr)
    except Exception as e:
        stdout, stderr = "", f"ERROR: {e}"
        logger.error(str(e))
        socket.subprocess.kill()
    return dict(stdout=stdout, stderr=stderr)


def compile_and_run(socket, compile_cmd, run_cmd, _input=None) -> dict:
    compiler_output = run_subprocess(socket, compile_cmd, _input)
    if compiler_output['stderr']:
        return compiler_output
    else:
        return run_subprocess(socket, run_cmd, _input)


def runcode(socket, code: str, lang: str, _input=None) -> dict:
    if not valid_lang(lang):
        return dict(stdout="", stderr="ERROR: This programing language is not supported")
    path, filename = make_paths()
    create_source_file(path, filename, get_ext(lang), code)
    if get_compile_cmd(lang):
        output = compile_and_run(
            socket=socket, compile_cmd=generate_cmd(get_compile_cmd(lang), path, filename),
            run_cmd=generate_cmd(get_run_cmd(lang), path, filename), _input=_input
        )
    else:
        run_cmd = generate_cmd(get_run_cmd(lang), path, filename)
        output = run_subprocess(socket, run_cmd, _input)
    # delete_runtime_files(path, filename)
    return output
