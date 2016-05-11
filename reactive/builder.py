from charms.reactive import when_not
from charms.reactive import set_state
from charmhelpers.core import hookenv

@when_not('builder.ready')
def bootstrap():
    hookenv.status_set('active', 'Ready')
    set_state('builder.ready')
