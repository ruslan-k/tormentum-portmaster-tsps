#!/usr/bin/env python3
"""Apply compatibility edits to the owner's GOG 1.4.1 SWF using FFDec 26.3.0."""
import argparse,hashlib,json,subprocess
from pathlib import Path
p=argparse.ArgumentParser();p.add_argument('input',type=Path);p.add_argument('output',type=Path);p.add_argument('--ffdec',required=True,type=Path);p.add_argument('--work',required=True,type=Path);a=p.parse_args()
assert a.input.resolve()!=a.output.resolve(), 'Never overwrite the original'
a.work.mkdir(parents=True,exist_ok=True);a.output.parent.mkdir(parents=True,exist_ok=True)
def run(args):
 with (a.work/'ffdec.log').open('a') as log: subprocess.run(['java','-jar',str(a.ffdec.resolve())]+args,check=True,stdout=log,stderr=subprocess.STDOUT)
run(['-export','script',str(a.work/'export'),str(a.input.resolve())])
edits=json.loads(Path(__file__).with_name('game-edits.json').read_text());classes=[]
for rel,record in edits.items():
 text=(a.work/'export/scripts'/rel).read_text()
 assert hashlib.sha256(text.encode()).hexdigest()==record['sha256'],f'Unexpected FFDec source/version: {rel}'
 lines=text.splitlines(keepends=True)
 for edit in reversed(record['edits']): lines[edit['start']:edit['end']]=[edit['replacement']]
 dst=a.work/'patched'/rel;dst.parent.mkdir(parents=True,exist_ok=True);dst.write_text(''.join(lines));classes.append((rel[:-3].replace('/','.'),str(dst.resolve())))
first=a.work/'sharedobject.swf';run(['-air','-replace',str(a.input.resolve()),str(first.resolve()),*classes[0]])
args=['-air','-replace',str(first.resolve()),str(a.output.resolve())]
for item in classes[1:]: args.extend(item)
run(args)
print('Patched',a.output,'SHA256',hashlib.sha256(a.output.read_bytes()).hexdigest())
