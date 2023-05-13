<a href="https://www.ansible-semaphore.com/">
<img src="https://repository-images.githubusercontent.com/23267883/6521ff0c-6a8d-4b67-897e-40354ecd5391" alt="Ansible-Semaphore - modern UI for Ansible" width="600"/>
</a>

# WORK-IN-PROGRESS

# Ansible Role - Ansible-Semaphore

Role to provision [Ansible Semaphore](https://github.com/ansible-semaphore/semaphore) on a linux server.

[![Molecule Test Status](https://badges.ansibleguy.net/sw_semaphore.molecule.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/molecule.sh.j2)
[![YamlLint Test Status](https://badges.ansibleguy.net/sw_semaphore.yamllint.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/yamllint.sh.j2)
[![PyLint Test Status](https://badges.ansibleguy.net/sw_semaphore.pylint.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/pylint.sh.j2)
[![Ansible-Lint Test Status](https://badges.ansibleguy.net/sw_semaphore.ansiblelint.svg)](https://github.com/ansibleguy/_meta_cicd/blob/latest/templates/usr/local/bin/cicd/ansiblelint.sh.j2)
[![Ansible Galaxy](https://img.shields.io/ansible/role/62323)](https://galaxy.ansible.com/ansibleguy/sw_semaphore)
[![Ansible Galaxy Downloads](https://img.shields.io/badge/dynamic/json?color=blueviolet&label=Galaxy%20Downloads&query=%24.download_count&url=https%3A%2F%2Fgalaxy.ansible.com%2Fapi%2Fv1%2Froles%2F62323%2F%3Fformat%3Djson)](https://galaxy.ansible.com/ansibleguy/sw_semaphore)


**Tested:**
* Debian 11

## Install

```bash
ansible-galaxy install ansibleguy.sw_semaphore

# or to custom role-path
ansible-galaxy install ansibleguy.sw_semaphore --roles-path ./roles

# install dependencies
ansible-galaxy install -r requirements.yml
```

## Functionality

* **Package installation**
  * Ansible-Semaphore in the specified version
  * Python3 Virtual-Environment
    * Ansible
    * common Ansible Jinja-Filter dependencies


* **Configuration**
  * Service: 'semaphore.service'
  * Service-user: 'semaphore'


  * **Default config**:
    * Directories:
      * Venv: '/var/local/lib/semaphore_venv'
      * Config: '/etc/semaphore'
      * Backup: '/var/backups/semaphore'
      * Tmp/Run: '/tmp/.semaphore'
 

  * **Default opt-ins**:
    * Nginx proxy => using [THIS Role](https://github.com/ansibleguy/infra_nginx)
    * MariaDB database => using [THIS Role](https://github.com/ansibleguy/infra_mariadb)
    * Daily local database backup (_if database is managed_)
    * Provisioning 'ansible.cfg' for serviceuser

  * **Default opt-outs**:
    * Persistent requirements

## Info

* **Note:** this role currently only supports debian-based systems


* **Note:** Most of the role's functionality can be opted in or out.

  For all available options - see the default-config located in the main defaults-file!


* **Warning:** Not every setting/variable you provide will be checked for validity. Bad config might break the role!


* **Info:* Persistent requirements can be used to speed up executions:

  It will install & update ansible-roles & ansible-collections using an external service/timer.

  By default, semaphore will need to re-install them ON EACH EXECUTION.

  For this to work - you will also have to make sure that the requirements files do not exist in your repositories:

  * $REPO/collections/requirements.yml
  * $REPO/roles/requirements.yml

## Usage

### Config

Define the config as needed:

```yaml
semaphore:
  manage:
    webserver: true  # install and configure local nginx with min-ca cert
    database: true  # install and configure local mariadb
    backup: true  # install service for daily local database backup (if database is managed)
    user: true  # create service-user 'semaphore'
    ansible_cfg: true  # provision /home/semaphore/ansible.cfg

  version: '2.8.90'  # see: https://github.com/ansible-semaphore/semaphore/releases

  persistent_requirements: false
  
  config:  # config key-value pairs as set in 'config.json': https://docs.ansible-semaphore.com/administration-guide/configuration
    concurrency_mode: 'node'
    email_sender: 'semaphore@template.ansibleguy.net'
    email_host: 'mail.template.ansibleguy.net'
    email_alert: true

    # optional
    ldap_enable: true
    ldap_needtls: true
    ldap_binddn: 'service_semaphore'
    ldap_bindpassword: !vault |
      $ANSIBLE_VAULT;1.1;AES256
      ...
    ldap_server: 'ldap.template.ansibleguy.net:636'
    ldap_searchfilter: '(&(mail=%s)(objectClass=person)(memberOf:=CN=semaphore,OU=Groups,DC=template,DC=ansibleguy,DC=net))'  # login with mail; must be in group 'semaphore'

    # optional => see: https://docs.ansible-semaphore.com/administration-guide/security#database-encryption
    cookie_hash: !vault |
      $ANSIBLE_VAULT;1.1;AES256
      ...
    cookie_encryption: !vault |
      $ANSIBLE_VAULT;1.1;AES256
      ...
    access_key_encryption: !vault |
      $ANSIBLE_VAULT;1.1;AES256
      ...

  requirements:  # requirements your execution-environment needs
    pip: ['httpx']  # any python3-modules
    collections: ['community.general']  # any ansible-collections (if persistent_requirements=true)
    roles: []  # any ansible-roles (if persistent_requirements=true)

  ansible_config:  # /home/semaphore/ansible.cfg => if manage.ansible_cfg=true; see: https://docs.ansible.com/ansible/latest/reference_appendices/config.html
    defaults:  # section
      remote_port: 48322
      vault_id_match: 'semaphore'
    diff:
      context: 2

  backup:
    retention: 30  # days

```

Minimal config:

```yaml
semaphore:
  version: '2.8.90'
  
```

You might want to use 'ansible-vault' to encrypt your passwords:
```bash
ansible-vault encrypt_string
```

### Execution

Run the playbook:
```bash
ansible-playbook -K -D -i inventory/hosts.yml playbook.yml
```

There are also some useful **tags** available:
* webserver
* database
* config
* requirements

To debug errors - you can set the 'debug' variable at runtime:
```bash
ansible-playbook -K -D -i inventory/hosts.yml playbook.yml -e debug=yes
```
