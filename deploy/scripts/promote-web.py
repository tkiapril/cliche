#!/usr/bin/python3
import errno
import pathlib
import platform
import sys
import subprocess


def main():
    dist = platform.dist()
    if dist[0] != 'debian' and dist[0] != 'Ubuntu':
        print('This script can only be run on Debian GNU/Linux or Ubuntu.')
        sys.exit(errno.EPERM)

    workdir = pathlib.Path(__file__).resolve().parent.parent
    with (workdir / 'etc' / 'revision.txt').open('r') as revision_file:
        revision = (revision_file.readline().strip())
    venv_dir = pathlib.Path('/home/cliche/venv_{}'.format(revision)).resolve()

    subprocess.check_call(
        [
            'sudo',
            '-ucliche',
            'rm',
            '-f',
            '/home/cliche/etc/cliche.io',
        ]
    )

    subprocess.check_call(
        [
            'sudo',
            '-ucliche',
            'ln',
            '-fs',
            str(venv_dir / 'etc' / 'cliche.io'),
            '/home/cliche/etc/cliche.io',
        ]
    )

    subprocess.check_call(
        [
            'sudo',
            'service',
            'nginx',
            'reload',
        ]
    )

    subprocess.check_call(
        [
            'sudo',
            '-ucliche',
            'rm',
            '-f',
            '/home/cliche/bin/uwsgi',
        ]
    )

    subprocess.check_call(
        [
            'sudo',
            '-ucliche',
            'ln',
            '-fs',
            str(venv_dir / 'bin' / 'uwsgi'),
            '/home/cliche/bin/uwsgi',
        ]
    )

    subprocess.check_call(
        [
            'sudo',
            '-ucliche',
            'rm',
            '-f',
            '/home/cliche/etc/cliche-uwsgi.ini',
        ]
    )

    subprocess.check_call(
        [
            'sudo',
            '-ucliche',
            'ln',
            '-fs',
            str(venv_dir / 'etc' / 'cliche-uwsgi.ini'),
            '/home/cliche/etc/cliche-uwsgi.ini',
        ]
    )

    subprocess.check_call(
        [
            'sudo',
            'cp',
            '-f',
            str(venv_dir / 'etc' / 'cliche-uwsgi.conf'),
            '/etc/init/cliche-uwsgi.conf',
        ]
    )

    subprocess.call(
        [
            'sudo',
            'stop',
            'cliche-uwsgi',
        ]
    )

    subprocess.check_call(
        [
            'sudo',
            'start',
            'cliche-uwsgi',
        ]
    )


if __name__ == '__main__':
    main()
