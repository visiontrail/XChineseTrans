"""Verify the guide's state diagrams in disposable local repositories."""
from pathlib import Path
import json, os, subprocess, tempfile

ROOT=Path(__file__).resolve().parents[1]
env=dict(os.environ, GIT_CONFIG_GLOBAL=os.devnull, GIT_CONFIG_NOSYSTEM='1',
         GIT_TERMINAL_PROMPT='0', GIT_EDITOR='true', GIT_SEQUENCE_EDITOR='true',
         GIT_AUTHOR_NAME='Guide QA',GIT_AUTHOR_EMAIL='qa@example.invalid',
         GIT_COMMITTER_NAME='Guide QA',GIT_COMMITTER_EMAIL='qa@example.invalid')
records=[]
findings=[]

with tempfile.TemporaryDirectory(prefix='git-ai-native-qa-') as scratch:
    base=Path(scratch)
    def run(where,*args,expected=0):
        r=subprocess.run(args,cwd=where,env=env,text=True,capture_output=True)
        records.append({'cwd':str(where).replace(scratch,'<TEMP>'),
                        'command':' '.join(args).replace(scratch,'<TEMP>'),
                        'exit':r.returncode,'stdout':r.stdout.strip().replace(scratch,'<TEMP>'),
                        'stderr':r.stderr.strip().replace(scratch,'<TEMP>')})
        assert r.returncode==expected,records[-1]
        return r.stdout.strip()
    def git(where,*args,expected=0): return run(where,'git',*args,expected=expected)
    def init(name):
        repo=base/name;repo.mkdir()
        git(repo,'init','-b','main')
        git(repo,'config','commit.gpgsign','false')
        git(repo,'config','core.hooksPath',str(base/'empty-hooks'))
        return repo
    def commit(repo,message,*files):
        git(repo,'add',*files);git(repo,'commit','-m',message)
        return git(repo,'rev-parse','HEAD')

    repo=init('staging')
    f=repo/'state.txt';f.write_text('A\n')
    (repo/'.gitignore').write_text('ignored.txt\n')
    a=commit(repo,'Record A','state.txt','.gitignore')
    f.write_text('B\n');git(repo,'add','state.txt');f.write_text('C\n')
    staged=git(repo,'diff','--staged');working=git(repo,'diff')
    assert '+B' in staged and '+C' not in staged
    assert '+C' in working and '-B' in working
    git(repo,'commit','-m','Record staged B')
    b=git(repo,'rev-parse','HEAD')
    assert git(repo,'show','HEAD:state.txt')=='B' and f.read_text()=='C\n'
    findings.append({'case':'staging_snapshot','result':'HEAD records B; working files remain C; diff comparisons separate both changes.'})

    isolated=base/'isolated'
    git(repo,'worktree','add','-b','task/isolated',str(isolated),'HEAD')
    assert (isolated/'state.txt').read_text()=='B\n'
    assert f.read_text()=='C\n'
    (isolated/'task.txt').write_text('Agent-only work\n')
    isolated_head=commit(isolated,'Record isolated work','task.txt')
    assert git(repo,'rev-parse','HEAD')==b and isolated_head!=b
    assert not (repo/'task.txt').exists()
    findings.append({'case':'worktree_isolation','result':'Separate branch/files/index; original uncommitted C and original HEAD preserved.'})

    (repo/'untracked.txt').write_text('Keep this\n')
    (repo/'ignored.txt').write_text('Local ignored content\n')
    git(repo,'stash','push','-u','-m','Pause experiment')
    assert f.read_text()=='B\n' and not (repo/'untracked.txt').exists()
    assert (repo/'ignored.txt').exists()
    stash_before=git(repo,'stash','list')
    git(repo,'stash','apply')
    assert f.read_text()=='C\n' and (repo/'untracked.txt').exists()
    assert git(repo,'stash','list')==stash_before
    findings.append({'case':'stash_scope','result':'-u saved untracked content; ignored file remained; apply restored work and kept the stash entry.'})

    seed=init('seed');(seed/'base.txt').write_text('Base\n')
    origin_a=commit(seed,'Base','base.txt')
    remote=base/'origin.git';git(base,'init','--bare','--initial-branch=main',str(remote))
    git(seed,'remote','add','origin',str(remote));git(seed,'push','-u','origin','main')
    learner=base/'learner';writer=base/'writer'
    git(base,'clone',str(remote),str(learner));git(base,'clone',str(remote),str(writer))
    for r in (learner,writer):
        git(r,'config','commit.gpgsign','false');git(r,'config','core.hooksPath',str(base/'empty-hooks'))
    git(learner,'switch','-c','task/change')
    (learner/'task.txt').write_text('Task\n');c=commit(learner,'Task C','task.txt')
    (writer/'remote.txt').write_text('Remote update\n');remote_b=commit(writer,'Remote B','remote.txt')
    git(writer,'push','origin','main');git(learner,'fetch','origin')
    assert git(learner,'rev-parse','HEAD')==c
    assert git(learner,'rev-parse','origin/main')==remote_b
    assert not (learner/'remote.txt').exists()
    git(learner,'merge','--ff-only','origin/main',expected=128)
    assert git(learner,'rev-parse','HEAD')==c
    findings.append({'case':'fetch_and_ff_only','result':'Fetch updated origin/main but not HEAD or working files; ff-only refused divergence without discarding either side.'})
    git(learner,'merge','--no-edit','origin/main')
    parents=git(learner,'show','-s','--format=%P','HEAD').split()
    assert parents==[c,remote_b]
    assert (learner/'task.txt').exists() and (learner/'remote.txt').exists()
    findings.append({'case':'merge_parents','result':'Merge commit preserved C and B as its two parents and contained both nonconflicting changes.'})
    git(learner,'switch','-c','task/replay',c)
    git(learner,'rebase','origin/main')
    replay=git(learner,'rev-parse','HEAD')
    assert replay!=c and git(learner,'rev-parse','HEAD^')==remote_b
    assert (learner/'task.txt').read_text()=='Task\n'
    findings.append({'case':'rebase_identity','result':'Task change replayed onto B with a new commit ID and preserved intended task content.'})

    conflict=init('conflict');(conflict/'line.txt').write_text('Base\n')
    commit(conflict,'Base','line.txt');git(conflict,'switch','-c','task/conflict')
    (conflict/'line.txt').write_text('Task\n');commit(conflict,'Task version','line.txt')
    git(conflict,'switch','main');(conflict/'line.txt').write_text('Main\n')
    main_tip=commit(conflict,'Main version','line.txt')
    git(conflict,'merge','task/conflict',expected=1)
    assert '<<<<<<<' in (conflict/'line.txt').read_text()
    git(conflict,'merge','--abort')
    assert git(conflict,'rev-parse','HEAD')==main_tip
    assert (conflict/'line.txt').read_text()=='Main\n' and git(conflict,'status','--porcelain')==''
    findings.append({'case':'merge_abort','result':'A real content conflict occurred; abort restored the clean pre-merge branch and file content.'})
    (conflict/'extra.txt').write_text('Undo this ordinary addition\n')
    added=commit(conflict,'Add extra','extra.txt')
    git(conflict,'revert','--no-edit',added)
    assert not (conflict/'extra.txt').exists()
    assert git(conflict,'rev-parse','HEAD')!=added
    git(conflict,'merge-base','--is-ancestor',added,'HEAD')
    findings.append({'case':'revert_history','result':'An inverse commit removed the addition while the original commit remained an ancestor.'})

report={'status':'passed','scope':'Disposable local repositories and local bare remote only',
        'cases':findings,'command_count':len(records),'records':records,
        'not_tested':['Model compliance with every prompt','GitHub account setup','GitHub-hosted Actions','Public deployment']}
(ROOT/'research/git-state-verification.json').write_text(json.dumps(report,indent=2)+'\n')
print(f'PASS: {len(findings)} Git state scenarios, {len(records)} local command checks.')
for x in findings: print(x['case']+': '+x['result'])
