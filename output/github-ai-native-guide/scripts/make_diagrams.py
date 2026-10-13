from pathlib import Path
import json
import subprocess

ROOT=Path(__file__).resolve().parents[1]
RENDER=Path('/Users/leoguo/.agents/skills/archify/renderers/architecture/render-architecture.mjs')
specs=[]

def n(id,label,sub,x,y,w=250,h=78,type='frontend'):
    return dict(id=id,label=label,sublabel=sub,pos=[x,y],size=[w,h],type=type)

def e(a,b,label=None,**kw):
    d=dict(**{'from':a,'to':b},variant='emphasis',**kw)
    if label: d['label']=label
    return d

def add(name,title,subtitle,nodes,edges,width=1000,height=540,notes=(),headings=()):
    spec={'schema_version':1,'diagram_type':'architecture','meta':{'title':title,'subtitle':subtitle,'viewBox':[width,height]},'components':nodes,'connections':edges,'cards':[]}
    specs.append((name,spec,{'notes':notes,'headings':headings}))

def chain(nodes,ids):
    edges=[]
    byid={x['id']:x for x in nodes}
    for a,b in zip(ids,ids[1:]):
        aa,bb=byid[a],byid[b]
        if aa['pos'][1]==bb['pos'][1]:
            forward=aa['pos'][0]<bb['pos'][0]
            edges.append(e(a,b,fromSide='right' if forward else 'left',toSide='left' if forward else 'right'))
        else: edges.append(e(a,b,fromSide='bottom',toSide='top'))
    return edges

nodes=[n('goal','Describe the result','Goal + location + boundary',50,80),n('inspect','Agent inspects','Files, history, access',375,80,type='backend'),n('act','Agent executes','Only the authorized work',700,80,type='backend'),n('evidence','Observe the result','Diff, checks, real page',700,300,type='security'),n('record','Return an evidence record','Before / after / unknowns',375,300,type='database'),n('decide','Choose the next result','Continue from known state',50,300)]
edges=chain(nodes,['goal','inspect','act','evidence','record','decide'])
edges.append({'from':'decide','to':'goal','fromSide':'left','toSide':'left','via':[[25,339],[25,119]],'variant':'dashed'})
add('02-intent-loop','Intent becomes an observable result','The agent operates the tools; the state changes stay visible.',nodes,edges,height=470,notes=['Authentication and platform-required approvals may need the account owner.','A proposed action is not evidence that the action occurred.'])

nodes=[n('files','Working files','Current edits',50,100,170),n('index','Index','Next snapshot',300,100,170,type='messagebus'),n('local','Local history','Commits + branches',550,100,170,type='database'),n('remote','Remote branch','Shared history',800,100,170,type='cloud'),n('pr','Pull request','Review + integration',800,330,170,type='security'),n('live','Delivered site','Observed at real URL',550,330,170,type='backend')]
edges=[e('files','index','git add'),e('index','local','git commit'),e('local','remote','git push'),{'from':'remote','to':'local','variant':'dashed','fromSide':'bottom','toSide':'bottom','via':[[885,245],[635,245]],'label':'git fetch','labelAt':[760,264]},e('remote','pr',fromSide='right',toSide='right',via=[[995,139],[995,369]]),e('pr','live','deploy + verify',fromSide='left',toSide='right',labelAt=[760,303])]
add('03-state-map','Where an agent moves the work','Each transition establishes a different result.',nodes,edges,width=1030,height=500,notes=['Local commit does not mean remote publication.','A merged PR does not prove a working deployment.'])

nodes=[];edges=[]
rows=[('Tools installed','Git + required runtime','git --version','Runtime version checks','Usable toolchain','A version, not a commit','frontend'),('Commit identity','Name, email, defaults','git config [--global]','Read or change settings','Effective configuration','Local or user-wide scope','database'),('Remote access','Known GitHub account','gh auth / SSH','login, status, ssh -T','Verified authentication','Access, not authorship','security'),('Project folder','Files prepared locally','git init -b main','Initialize repository metadata','Local repository','No first commit or upload yet','database')]
for i,(a,sa,b,sb,c,sc,t) in enumerate(rows):
    y=70+i*160
    nodes.extend([n(f'a{i}',a,sa,50,y),n(f'b{i}',b,sb,375,y,type=t),n(f'c{i}',c,sc,700,y,type='backend')])
    edges.extend([e(f'a{i}',f'b{i}'),e(f'b{i}',f'c{i}')])
add('04-setup','From environment to a local repository','The agent inspects existing state before changing it.',nodes,edges,height=760,notes=['ssh-keygen creates a key pair; it does not authorize a GitHub account by itself.','A package-manager install supplies tools. No project history is created here.'])

nodes=[];edges=[]
rows=[('What is pending?','Files + staging + branch','git status','Including untracked paths','State summary','No file contents changed'),('What differs?','Two snapshots compared','git diff / --staged','Work vs index / index vs HEAD','Content differences','Untracked content is separate'),('Why this line?','History and context','git log / show / blame','Commits, patches, provenance','A reason to investigate','A line is not the whole story'),('What was tested?','The current revision','git rev-parse HEAD','Resolve a commit identity','Exact commit ID','Tie the result to this revision')]
for i,(a,sa,b,sb,c,sc) in enumerate(rows):
    y=70+i*145
    nodes.extend([n(f'a{i}',a,sa,50,y),n(f'b{i}',b,sb,375,y,type='database'),n(f'c{i}',c,sc,700,y,type='backend')])
    edges.extend([e(f'a{i}',f'b{i}'),e(f'b{i}',f'c{i}')])
add('05-inspection','Choose the inspection that answers the question','Read-only Git tools observe different layers.',nodes,edges,height=680,notes=['A check report should name the revision and the content that it actually exercised.'])

nodes=[n('a','Base commit A','Chosen starting revision',50,190,200,type='database'),n('b','main points to B','Main history advances',360,80,240,type='database'),n('c','task points to C','One focused change',360,300,240,type='database'),n('mainfiles','Main checkout','Working files + its index',710,80,240),n('taskfiles','Agent worktree','Separate files + its index',710,300,240,type='backend')]
edges=[e('a','b',fromSide='top',toSide='left',via=[[150,119]]),e('a','c',fromSide='bottom',toSide='left',via=[[150,339]]),e('b','mainfiles'),e('c','taskfiles')]
add('06-branches','A branch names history; a worktree holds files','Separate working areas can share the same repository history.',nodes,edges,height=530,notes=['git switch -c creates and selects a branch; git switch changes the current checkout.','git worktree add creates another checkout. Uncommitted edits are not copied automatically.','Branch creation is not a commit. The chosen starting revision still matters.'])

nodes=[n('head','HEAD: version A','Last recorded snapshot',50,95,220,type='database'),n('index','INDEX: version B','Selected for next commit',400,95,220,type='messagebus'),n('work','FILES: version C','Edited again after staging',750,95,220),n('newhead','NEW HEAD: B','git commit records the index',400,330,220,type='database'),n('stillwork','FILES STILL: C','Later edits remain unstaged',750,330,220)]
edges=[{'from':'head','to':'index','variant':'dashed','label':'git diff --staged'},{'from':'index','to':'work','variant':'dashed','label':'git diff'},e('index','newhead','git commit',fromSide='bottom',toSide='top',labelAt=[440,250]),e('work','stillwork','unchanged',fromSide='bottom',toSide='top',labelAt=[925,250])]
add('07-staging','Staging freezes a selection of content','The staged version and the working version can differ.',nodes,edges,width=1020,height=535,notes=['Dashed arrows compare snapshots without changing them.','git add again would update the index from the later working content.','To verify the commit itself, test the committed snapshot rather than an unrelated working state.'])

nodes=[n('pass','Check valid content','Record revision + result',50,80,type='backend'),n('break','Disposable broken copy','Change one local link',375,80),n('fail','Observe expected failure','Missing target is reported',700,80,type='security'),n('restore','Restore the good link','Do not keep the test damage',700,300),n('recheck','Observe a passing check','Static link/structure scope',375,300,type='backend'),n('browser','Inspect the local page','Follow the link; read the item',50,300,type='cloud')]
add('08-validation','Make the check demonstrate what it detects','A deliberate failure is useful evidence for a small checker.',nodes,chain(nodes,['pass','break','fail','restore','recheck','browser']),height=495,notes=['python check_site.py checks local content. An HTTP preview serves files to this computer.','Neither operation creates a commit, opens a PR, or proves a public deployment.'])

nodes=[n('upstream','Original repository','Remote name: upstream',60,100,type='cloud'),n('fork','Your GitHub fork','Remote name: origin',690,100,type='cloud'),n('local','Local repository','Commits + working checkout',375,370,type='database'),n('config','git remote add / -v','Register / inspect destinations',375,560,type='external')]
edges=[e('upstream','fork','Fork on GitHub',labelAt=[500,125]),{'from':'fork','to':'upstream','variant':'security','fromSide':'top','toSide':'top','via':[[815,40],[185,40]],'label':'PR: fork head into upstream base','labelAt':[500,25]},e('fork','local','git clone / fetch origin',fromSide='bottom',toSide='top',via=[[815,260],[500,260]],labelAt=[650,245]),e('upstream','local','git fetch upstream',fromSide='bottom',toSide='left',via=[[185,409]],labelAt=[185,295]),e('local','fork','git push -u origin',fromSide='right',toSide='right',via=[[980,409],[980,139]],labelAt=[922,310]),{'from':'config','to':'local','variant':'dashed','fromSide':'top','toSide':'bottom'}]
add('09-remotes','Follow the direction of the data','Fork, clone, fetch, push, and PR target different places.',nodes,edges,height=730,notes=['origin and upstream are conventions, not special servers. Inspect the actual URLs.','The -u option establishes a branch tracking relationship after a successful push.'])

nodes=[n('a','A','Shared base',50,180,110,64,type='database'),n('b','B on main','Existing commit',325,80,195,64,type='database'),n('c','C on task','Existing commit',325,280,195,64,type='database'),n('m','M: merge commit','Parents are B and C',720,180,230,64,type='backend'),n('a2','A','Shared base',50,485,110,64,type='database'),n('b2','B on main','New base for task',325,485,195,64,type='database'),n('cprime','Replayed commit C′','New commit identity',720,485,230,64,type='backend')]
edges=[e('a','b',fromSide='top',toSide='left',via=[[105,112]]),e('a','c',fromSide='bottom',toSide='left',via=[[105,312]]),e('b','m',fromSide='right',toSide='top',via=[[835,112]]),e('c','m',fromSide='right',toSide='bottom',via=[[835,312]]),e('a2','b2'),e('b2','cprime','git rebase',labelAt=[620,506])]
add('10-integration','Two ways to integrate another line of work','Illustrative commit identities; arrows follow history toward newer commits.',nodes,edges,height=690,notes=['--ff-only advances a reference only when it can fast-forward; it refuses divergent history.','git merge --abort attempts to return to the pre-merge state. Preserve unfinished work first.'],headings=[['MERGE / git merge joins both histories',50,28],['REBASE / replay the task on the current main',50,435]])

nodes=[n('push','Push branch','Remote head matches intent',50,80,type='cloud'),n('pr','Open pull request','Correct base + head',375,80,type='security'),n('review','Review + checks','Evidence for this revision',700,80,type='security'),n('merge','Merge approved revision','Observed base-branch result',700,300,type='database'),n('deploy','Publish the artifact','Deployment run + revision',375,300,type='cloud'),n('verify','Open the actual URL','Observe content + links',50,300,type='backend')]
add('11-delivery','The agent follows the change all the way through','Each stage returns a distinct piece of evidence.',nodes,chain(nodes,['push','pr','review','merge','deploy','verify']),height=520,notes=['Only the first stage here is git push. PRs, hosting settings, and browser checks use other tools.','Pages serves static files. A project subpath can change how internal URLs resolve.'])

nodes=[];edges=[]
rows=[('Staged edit','Working file should survive','git restore --staged','Reset selected index content','Edit remains in files','Removed from next commit','messagebus'),('Unfinished local work','Pause, then resume','git stash push -u / apply','Save, then restore changes','Work restored locally','Apply keeps the saved entry','database'),('A → B → C','History already shared','git revert B','Apply the inverse as a commit','A → B → C → R','Earlier commits remain','backend'),('Content to replace','Explicit target and scope','restore / reset --hard','Can overwrite local content','Selected state replaces it','Preserve needed work first','security')]
for i,(a,sa,b,sb,c,sc,t) in enumerate(rows):
    y=75+i*155
    nodes.extend([n(f'a{i}',a,sa,50,y),n(f'b{i}',b,sb,375,y,type=t),n(f'c{i}',c,sc,700,y,type=t)])
    edges.extend([e(f'a{i}',f'b{i}'),e(f'b{i}',f'c{i}')])
add('12-recovery','Recover the layer that contains the mistake','The desired remaining state determines the operation.',nodes,edges,height=765,notes=['stash list inspects saved entries. -u includes untracked files, but not ignored files.','restore changes selected content; reset can also reposition the current branch.','Revert preserves history. It does not remove a leaked secret from older commits.'])

for name,spec,extra in specs:
    src=ROOT/'diagrams'/f'{name}.architecture.json'
    src.write_text(json.dumps(spec,indent=2)+'\n')
    (ROOT/'diagrams'/f'{name}.notes.json').write_text(json.dumps(extra,indent=2)+'\n')
    result=subprocess.run(['node',str(RENDER),str(src),str(ROOT/'diagrams'/f'{name}.html')],text=True,capture_output=True)
    if result.returncode:
        raise RuntimeError(name+'\n'+result.stdout+result.stderr)
    print(name+' rendered')
