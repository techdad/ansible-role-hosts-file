import os

import testinfra.utils.ansible_runner

testinfra_hosts = testinfra.utils.ansible_runner.AnsibleRunner(
    os.environ['MOLECULE_INVENTORY_FILE']).get_hosts('all')


def test_hosts_file_exists(host):
    f = host.file('/etc/hosts')
    assert f.exists
    assert f.user == 'root'
    assert f.group == 'root'


def test_hosts_file_localhost(host):
    f = host.file('/etc/hosts')
    assert f.contains('127.0.0.1\s\+localhost')
    assert f.contains('^::1\s\+localhost')


def test_hosts_file_additions(host):
    f = host.file('/etc/hosts')
    assert f.contains('192.0.2.46\s\+dualstack')
    assert f.contains('2001:db8:192:2::46\s\+dualstack')
    assert f.contains('192.0.2.44\s\+ipv4only')
    assert f.contains('2001:db8:192:2::66\s\+ipv6only')
