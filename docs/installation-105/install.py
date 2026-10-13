#!/usr/bin/env python3
"""Install exact seven-file 1.0.5 bundle on a NEW host. Never updates an instance.
Missing/hash-changed assets, wrong provenance, existing paths or root service
account => STOP before writes. No download, restart, purchase or public publish.
Offline test mode is private loopback HTTP only, not production TLS acceptance.
"""
import argparse,hashlib,json,os,pwd,re,secrets,shutil,subprocess
from pathlib import Path
HERE=Path(__file__).resolve().parent
FILES={'LICENSE':'5f928c68872b3d6d7a0f500747f2dd4efd21ef8e6cf514644e86eba72c54a7d0','NOTICE':'6d6d53f1e80547521cb81d19b4096f0c7f4bc38b91e7ee269829c65eb8523f7d','PROVENANCE.json':'57b8130a295b0178f58d773fe2baa668c49441f4b6ed1f9ff653cb3157821e77','SBOM.cdx.json':'e5ef03f1a5f1ef51da89e5ff36f87f71b41593d549499946fe4037d9f3b798da','THIRD-PARTY-NOTICES.md':'b8dbf5a1be793b237a6fa69f5b08e4cefc3042e4061edda626221e307bc460d6','VERSION.txt':'dc37ed3bdcd2ab689dab149eabf3e9578133480cd5857f31bf543cfa9ac948ab','yggaro-server-linux-amd64':'fd943def65417fa4480df345406652690898a27bcf63387b300fec30e39d86a8'}
MANIFEST='50d979f634f49536aeca10d16a9e7193a2aa59889eecad1bda8744cdc06e4e6c'
def fail(msg):raise SystemExit('STOP: '+msg)
def verify(bundle):
 if bundle.is_symlink() or not bundle.is_dir():fail('bundle must be a real directory')
 for name,pin in {**FILES,'SHA256SUMS':MANIFEST}.items():
  p=bundle/name
  if p.is_symlink() or not p.is_file() or hashlib.sha256(p.read_bytes()).hexdigest()!=pin:fail('asset pin '+name)
 # Exact trusted manifest plus exact per-file pins: no ignore-missing shortcut.
 return True
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--bundle',type=Path,required=True);ap.add_argument('--check',action='store_true');ap.add_argument('--domain');ap.add_argument('--email');ap.add_argument('--offline-loopback-test',action='store_true');a=ap.parse_args()
 verify(a.bundle)
 if a.check:print('PASS: exact manifest + seven assets');return
 if os.geteuid()!=0:fail('root required for installation; runtime will be unprivileged')
 if a.offline_loopback_test:
  if a.domain or a.email:fail('offline mode cannot use public domain')
 elif not a.domain or not a.email or not re.fullmatch(r'[a-z0-9.-]+',a.domain) or '.' not in a.domain or not re.fullmatch(r'[A-Za-z0-9_.+@-]+',a.email) or '@' not in a.email:fail('domain/email required, literal safe characters only')
 paths=['/opt/yggaro','/var/lib/yggaro','/var/lib/yggaro-keys','/etc/yggaro-server.env','/etc/systemd/system/yggaro-server.service','/usr/local/sbin/yggaro-admin']
 if any(os.path.lexists(p) for p in paths):fail('existing install/data/env/unit/helper; use separately accepted upgrade')
 try:
  u=pwd.getpwnam('yggaro')
  if u.pw_uid==0 or u.pw_gid==0:fail('yggaro must be an unprivileged account')
 except KeyError:
  subprocess.run(['useradd','--system','--user-group','--home-dir','/var/lib/yggaro','--no-create-home','--shell','/usr/sbin/nologin','yggaro'],check=True);u=pwd.getpwnam('yggaro')
 for p in ['/var/lib/yggaro','/var/lib/yggaro-keys']:
  Path(p).mkdir(mode=0o700);os.chown(p,u.pw_uid,u.pw_gid)
 Path('/opt/yggaro').mkdir(mode=0o755)
 for name in FILES:
  dest=Path('/opt/yggaro')/('yggaro-server' if name=='yggaro-server-linux-amd64' else name)
  shutil.copyfile(a.bundle/name,dest);dest.chmod(0o755 if name=='yggaro-server-linux-amd64' else 0o644)
 # Never print credentials or place them in argv; exclusive root-only secret file.
 with open('/etc/yggaro-server.env','x',opener=lambda path,flags:os.open(path,flags,0o600)) as f:
  f.write('YGGARO_DB_PASSPHRASE='+secrets.token_hex(32)+'\nYGGARO_BOOTSTRAP_TOKEN='+secrets.token_hex(16)+'\n')
 unit=(HERE/'yggaro-server.service.in').read_text()
 if a.offline_loopback_test:
  unit=unit.replace('-domain @DOMAIN@ -acme-email @EMAIL@','-listen 127.0.0.1:80')
 else:unit=unit.replace('@DOMAIN@',a.domain).replace('@EMAIL@',a.email)
 Path('/etc/systemd/system/yggaro-server.service').write_text(unit)
 shutil.copyfile(HERE/'yggaro-admin','/usr/local/sbin/yggaro-admin');Path('/usr/local/sbin/yggaro-admin').chmod(0o755)
 print('Installed; secrets not displayed. Back up passphrase privately before starting.')
 print('Then: systemctl daemon-reload; systemctl enable --now yggaro-server')
if __name__=='__main__':main()
