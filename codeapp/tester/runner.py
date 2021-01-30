from django.utils import timezone
from os.path import join, isdir, dirname, isfile, abspath
from os import makedirs, remove, listdir, removedirs, setgid, setuid, environ, system, getenv
from random import randint
from subprocess import PIPE, run, TimeoutExpired, Popen
import logging
import shlex
import platform
import pwd

logging.basicConfig(level=logging.NOTSET)
logger = logging.getLogger(__name__)

""" Subprocess execution time """
RUN_TIMEOUT = 5
COMPILER_TIMEOUT = 10

""" {filename} will be replaced by filename
    {path/filename} will be replaced by path/filename
    cmd = command
    ext = file extension
"""
VALID_LANGS = {
    'python': {
        'run_cmd': 'python {filename}.py',
        'ext': '.py'
    },
    'javascript': {
        'run_cmd': 'node {filename}.js',
        'ext': '.js'
    },
    'typescript': {
        'run_cmd': 'node {filename}.js',
        'compile_cmd': 'tsc {filename}.ts',
        'ext': '.ts'
    },
    'c': {
        'run_cmd': '{path/filename}.exe' if platform.system() == "Windows" else './{filename}',
        'ext': '.c',
        'compile_cmd': 'gcc {filename}.c -o {filename}'
    },
    'cpp': {
        'run_cmd': '{path/filename}.exe' if platform.system() == "Windows" else './{filename}',
        'ext': '.cpp',
        'compile_cmd': 'g++ {filename}.cpp -o {filename}'
    },
    'java': {
        'run_cmd': 'java {filename}',
        'ext': '.java',
        'compile_cmd': 'javac {filename}.java'
    }

}


def create_source_file(path, filename, ext, code):
    if ext == '.java':
        code = class_refactor(code, filename)
    with open(join(path, filename + ext), mode='w', encoding='UTF-8')as fp:
        fp.writelines(code.split('\r'))
        logger.debug(f"{filename}{ext} created at {abspath(path)}")


def class_refactor(code, filename):
    """ Ensure that the main java class name is equal a file name generated"""
    try:
        old_class = code[0:code.index('{')].split()[-1]
        return code.replace(old_class, filename, 1)
    except ValueError:
        return code


def delete_runtime_files(path, filename):
    try:
        file_names = [f for f in listdir(path) if filename == f.split('.')[0]]
        for f in file_names:
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
    logger.debug(f"Path created at: {abspath(path)}")
    filename = "File" + \
        f"{now.year}{now.month}{now.day}{now.hour}{now.minute}{now.second}"
    return path, filename


def format_cmd(cmd, path, filename) -> str:
    return cmd.replace('{filename}', shlex.quote(filename)) \
        .replace('{path/filename}', shlex.quote(join(path, filename)))


"""
def run_subprocess(cmd, path, input=None) -> dict:
    logger.error(f"Subprocess running...\ncmd = {cmd}\tcwd = {path}")
    cmd = shlex.split(cmd)
    if not input:
        input = "\n".join([f"'MISSING-INPUT-{x}'" for x in range(1, 21)])
    else:
        input += '\n' if input[-1] is not '\n' else ''

    _subprocess = Popen(cmd, shell=True, stdin=PIPE, stdout=PIPE, stderr=PIPE, cwd=path, universal_newlines=True)
    try:
        stdout, stderr = _subprocess.communicate(timeout=5, input=input)
        if stderr:
            logger.error(stderr)
    except Exception as e:
        stdout, stderr = "", f"ERROR: {e}"
        logger.error(str(e))
        _subprocess.terminate()
    return dict(stdout=stdout, stderr=stderr)
"""


def demote(sandbox):
    def result():
        try:
            user = pwd.getpwnam(getenv("GUEST_USER"))
            setgid(user.pw_gid)
            setuid(user.pw_uid)
        except Exception as e:
            pass
            # logger.error("Can't demote user!")
    return result if sandbox else None


def code_firewall_ok(code):
    replaces = ['"', "'", '+', '\\']
    for x in replaces:
        code = code.replace(x, '')
    code = ' '.join([x for x in code.splitlines() if x])
    code = ' '.join([x for x in code.split(' ') if x])
    logger.debug(code)
    patterns = ['rm -', 'rm /', 'rm .', 'rm *','--no-preserve-root']
    for pattern in patterns:
        if pattern in code:
            return False
    return True


def run_subprocess(cmd, path, timeout=RUN_TIMEOUT, input=None, sandbox=None) -> dict:
    logger.info(f"Subprocess running...\ncmd = {cmd}\tcwd = {path}")
    cmd = shlex.split(cmd)
    if not input:
        input = "\n".join([f"'MISSING-INPUT-{x}'" for x in range(1, 21)])
    else:
        input += '\n' if input[-1] != '\n' else ''

    try:
        sp = run(cmd, shell=False, capture_output=True, cwd=path,
                 text=True, input=input, timeout=timeout, preexec_fn=demote(sandbox))
        if sp.stderr:
            logger.debug(sp.stderr)
    except Exception as e:
        logger.error(str(e))
        return dict(stdout="", stderr=f"ERROR: {e}")
    logger.debug(dict(stdout=sp.stdout, stderr=sp.stderr,
                      returncode=sp.returncode))
    return dict(stdout=sp.stdout, stderr=sp.stderr)


def compile_and_run(compile_cmd, run_cmd, path, input=None) -> dict:
    compiler_output = run_subprocess(compile_cmd, path, timeout=COMPILER_TIMEOUT)
    if compiler_output['stderr']:
        return compiler_output
    else:
        return run_subprocess(run_cmd, path, input=input, sandbox=True)


def runcode(code: str, lang: str, input=None) -> dict:
    if not valid_lang(lang):
        return dict(stdout="", stderr="ERROR: This programing language is not supported")
    if not code_firewall_ok(code):
        return dict(stdout="", stderr="ERROR: Dangerous commands are not allowed")
    path, filename = make_paths()
    create_source_file(path, filename, get_ext(lang), code)
    if need_compile(lang):
        output = compile_and_run(
            compile_cmd=format_cmd(get_compile_cmd(lang), path, filename),
            run_cmd=format_cmd(get_run_cmd(lang), path, filename),
            path=path,
            input=input
        )
    else:
        run_cmd = format_cmd(get_run_cmd(lang), path, filename)
        output = run_subprocess(run_cmd, path, input=input, sandbox=True)
    delete_runtime_files(path, filename)
    return output
