# Ansible Role: hosts-file

This is a super simple role with a single task and template to populate an `/etc/hosts` file from the given list variable.

The use-case is generally for systems like database cluster members, where it's desired that they can intercommunicate by name, even in the event of outside network access (and thus DNS) failure.

Please *do NOT* consider this a way to forego configuring real DNS for an environment!

## Role Variables:

| Parameter     | Default     |
|---------------|-------------|
| `hosts_hosts` | `[]` (none) |

Populate this with a list of dictionary entries that will be the lines to add to the `/etc/hosts` file, excluding `localhost`.

If empty, or not set, then *only* the default `localhost` entries are added.

### Format:

```yaml
hosts_hosts:
  - name: 
    ipv4: 
    ipv6: 
```

### Details:

* Do *not* add in 'localhost' entries. You can, but the are redundant and always added at the top in any case.
* Always use *short* **hostnames** - the systems default domain is also automatically appended as an additional name.
* Always have both `ipv4:` and `ipv6:` listed, even if one or the other is empty.

### Working Example:

```yaml
# hosts file variable
hosts_hosts:
  - name: "dualstack"
    ipv4: "192.0.2.46"
    ipv6: "2001:db8:192:2::46"
  - name: "ipv4only"
    ipv4: "192.0.2.44"
    ipv6:
  - name: "ipv6only"
    ipv4:
    ipv6: "2001:db8:192:2::66"
```

... would result in:

```
# Ansible managed hosts file
127.0.0.1   localhost localhost.localdomain localhost4 localhost4.localdomain4
::1         localhost localhost.localdomain localhost6 localhost6.localdomain6

192.0.2.46                 dualstack  dualstack.domain.tld
2001:db8:192:2::46         dualstack  dualstack.domain.tld

192.0.2.44                 ipv4only  ipv4only.domain.tld

2001:db8:192:2::46         ipv6only  ipv6only.domain.tld
```


# Example Playbook

Just specify the role:

```yaml
---
- name: hosts-file
  hosts: all
  become: True

  ## run role ##
  roles:
    - role: hosts-file
```

(It's preferable to specify the `hosts_hosts` variable in the inventory, host host or group).

License
-------

Apache 2.0

Author Information
------------------

Daniel Shaw <daniel@techdad.xyz>
