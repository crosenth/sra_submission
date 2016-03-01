"""
Marker gene classification pipeline
"""

# System-level imports.  These should be very stable
import os
import sys

from ConfigParser import SafeConfigParser, NoSectionError
from glob import glob

from SCons.Script import (Decider, Variables, ARGUMENTS, Help)
#####

Decider('MD5-timestamp')

# get the settings
settings = ARGUMENTS.get('settings', 'settings.conf')
limits = ARGUMENTS.get('limits', 'limits.conf')
if not os.path.exists(settings):
    sys.exit("Can't find {}".format(settings))

_params = SafeConfigParser(allow_no_value=True)
_params.read(settings)

# either we're already operating in an activated virtualenv (which we can
# activate again harmlessly) or we use the one defined in settings.conf
try:
    venv = os.environ.get('VIRTUAL_ENV') or _params.get('env', 'virtualenv')
except NoSectionError:
    msg = 'No virtualenv is activated, and none is defined in settings.conf'
    sys.exit(msg)

print 'using virtualenv "{}"'.format(venv)
if not os.path.exists(venv):
    msg = 'The virtualenv \'{}\' does not exist or is not readable'
    sys.exit(msg.format(venv))

# activate the virtualenv
activate_this = os.path.join(venv, 'bin', 'activate_this.py')
execfile(activate_this, dict(__file__=activate_this))

# Explicitly define path, ensuring that we don't inherit the users' path

PATH = [
    'bin',
    os.path.join(venv, 'bin'),
    '/usr/local/bin',
    '/usr/bin',
    '/bin'
]

# Put local bin first in the PATH
os.environ['PATH'] = 'bin:' + os.environ['PATH']

# These and all subsequent imports come from the virtualenv
from bioscons.slurm import SlurmEnvironment

vars = Variables()

for k, v in _params.items('env'):
    vars.Add(k, default=v)

vars.Add('specimen')

# if use_cluster is set appropriately, submit jobs to slurm daemon
use_cluster = _params.get('env', 'use_cluster')
use_cluster = str.lower(use_cluster) in ['true', '1', 't', 'y', 'yes']

scons_env = dict(os.environ, PATH=':'.join(PATH))

env = SlurmEnvironment(
    ENV=scons_env,
    variables=vars,
    SHELL='bash',
    use_cluster=use_cluster,
    time=True
)

Help(vars.GenerateHelpText(env))

# find xl files but not the ones with ~ in them
for xl in (fname for fname in glob('data/*.xlsx') if '~' not in fname):
    proj_name = os.path.splitext(os.path.basename(xl))[0]
    env.Replace(specimen=os.path.join(env['out'], proj_name))

    specimens = env.Command(
        target='$specimen/specimens.csv',
        source=xl,
        action=('in2csv $SOURCE'
                ' | sed "s/pyro_plate/specimen/"'  # some filtering
                ' | csvcut -c specimen'
                ' | csvgrep  -c specimen -r ".+"'
                ' > $TARGET'))

    seqs, info, labels = env.Command(
        target=['$specimen/seqs.fasta',
                '$specimen/seq_info.csv',
                '$specimen/labels.csv'],
        source=specimens,
        action=('walk_data.py'
                ' --fastq-dir %s/fastq '
                ' --seqs ${TARGETS[0]}'
                ' --seq-info ${TARGETS[1]}'
                ' --md5sums ${TARGETS[2]}'
                ' $SOURCE' % env['specimen']))
