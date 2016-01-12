from charms.reactive import when, when_not
from charms.reactive import set_state
from charmhelpers.core import hookenv

from subprocess import check_call
from charmhelpers.fetch import apt_install

@when_not('bootstrapped')
def bootstrap():
    hookenv.status_set('maintenance', 'Installing base resources')
    apt_install(['git', 'default-jre', 'openjdk-7-jdk'])
    check_call(['pip', 'install', '-U', 'pip'])  # 1.5.1 (trusty) pip fails on --download with git repos
    set_state('bootstrapped')


@when('bootstrapped')
def ready_to_act():
    hookenv.status_set('active', 'Ready')
