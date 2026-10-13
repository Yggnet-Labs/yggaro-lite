#!/usr/bin/env python3
"""Remove installed 1.0.5 service/program, preserve all data/keys/env/backups/account.
No recursive deletion, purge, package removal or external DNS/certificate action.
"""
import hashlib,os,subprocess
from pathlib import Path
from install import FILES,HERE,fail
if os.geteuid()!=0:fail('root required')
paths={'/opt/yggaro/yggaro-server':FILES['yggaro-server-linux-amd64'],'/usr/local/sbin/yggaro-admin':hashlib.sha256((HERE/'yggaro-admin').read_bytes()).hexdigest()}
for name,pin in paths.items():
 p=Path(name)
 if p.is_symlink() or not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=pin:fail('installed file drift; no stop/remove '+name)
unit=Path('/etc/systemd/system/yggaro-server.service')
if unit.is_symlink() or not unit.is_file() or '\nUser=yggaro\n' not in unit.read_text():fail('unrecognized service unit; no stop/remove')
subprocess.run(['systemctl','disable','--now','yggaro-server'],check=True,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
for name in [*paths,str(unit)]:Path(name).unlink()
subprocess.run(['systemctl','daemon-reload'],check=True)
print('Removed service/program/helper only. Data, env/passphrase, keys, backup, notices and service account retained.')
