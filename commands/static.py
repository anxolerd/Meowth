from flask.ext.script import Manager
from subprocess import call
from commands.utils import perform

import os


def alt_exec(cmd, alt=None):
    """
    Tries to execute command.
    If command not found, it tries to execute the alternative comand
    """
    try:
        call(cmd)
    except OSError as e:
        if e.errno == os.errno.ENOENT and alt:
            try:
                call(alt)
            except OSError as ex:
                raise ex
        else:
            raise e

StaticCommand = Manager(usage='Commands to build static')


@StaticCommand.option(
    '--noinput',
    dest='noinput',
    action='store_true',
    default=False,
    help='Do not ask user anything',
)
def npm(noinput=False):
    """ Run npm install script """
    with perform(
        name='static npm',
        before='run npm install',
    ):
        cmd = ["npm", "install"]
        if noinput:
            cmd.append("--noinput")
        alt_exec(
            cmd=cmd,
        )


@StaticCommand.command
def bower():
    """ Run bower install script """
    with perform(
        name='static bower',
        before='run bower install',
    ):
        alt_exec(
            cmd=["bower", "install"],
            alt=["./node_modules/bower/bin/bower", "install"],
        )


@StaticCommand.command
def gulp():
    """ Run gulp build script """
    with perform(
        name='static gulp',
        before='run gulp',
    ):
        alt_exec(
            cmd=["gulp"],
            alt=["./node_modules/gulp/bin/gulp.js"],
        )


@StaticCommand.command
def clean():
    """ Clean built static files """
    with perform(
        name='static clean',
        before='run gulp clean',
    ):
        alt_exec(
            cmd=["gulp", "clean"],
            alt=["./node_modules/gulp/bin/gulp.js", "clean"],
        )