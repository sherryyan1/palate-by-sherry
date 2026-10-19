"""Declarative native Keynote authoring on owned scratch copies; never convert PPTX.

Outputs are candidates until the shared native delivery review passes. Operations
are sequential; slide and object selectors refer to the state after prior edits.
"""
import argparse
import hashlib
import json
import math
from pathlib import Path
import shutil
import tempfile
import keynote_native as native

ACTIONS = {
 'add_slide': ({'action'}, {'layout', 'notes', 'skipped'}),
 'delete_slide': ({'action','slide'}, set()),
 'duplicate_slide': ({'action','slide'}, set()),
 'move_slide': ({'action','slide','before'}, set()),
 'set_slide': ({'action','slide'}, {'layout','notes','skipped'}),
 'set_canvas': ({'action','width','height'}, set()),
 'set_text': ({'action','slide','kind','index','text'}, {'font','size','color'}),
 'add_text': ({'action','slide','text','bounds'}, {'font','size','color','height_mode'}),
 'add_shape': ({'action','slide','text','bounds'}, {'font','size','color'}),
 'add_table': ({'action','slide','cells','bounds'}, set()),
 'set_cell': ({'action','slide','index','row','column','value'}, set()),
 'add_chart': ({'action','slide','rows','columns','data','chart_type','bounds'}, set()),
 'add_image': ({'action','slide','path','sha256','bounds'}, set()),
}
CHARTS = {'vertical_bar_2d','stacked_vertical_bar_2d','horizontal_bar_2d','line_2d','pie_2d'}


def number(v, positive=False):
    if type(v) not in (int,float) or not math.isfinite(v) or positive and v <= 0:
        raise ValueError('Use finite numeric values and positive dimensions')


def scalar(v):
    if v is not None and type(v) not in (str,int,float,bool): raise ValueError('Invalid cell value')
    if type(v) is float: number(v)
    if isinstance(v,str) and (len(v)>100000 or v.startswith('=')):
        raise ValueError('Formula creation requires a separately reviewed native workflow')


def validate_spec(spec):
    if not isinstance(spec,dict) or set(spec)!={'schema_version','mode','source_sha256','operations','content_ledger'} or type(spec['schema_version']) is not int or spec['schema_version']!=1:
        raise ValueError('Invalid authoring schema')
    if spec['mode'] not in ('create','edit'): raise ValueError('Invalid authoring mode')
    digest=spec['source_sha256']
    if spec['mode']=='create' and digest is not None: raise ValueError('New decks have no source hash')
    if spec['mode']=='edit' and (not isinstance(digest,str) or len(digest)!=64 or any(c not in '0123456789abcdef' for c in digest)):
        raise ValueError('Editing requires a source SHA-256')
    if not isinstance(spec['content_ledger'],str) or not spec['content_ledger'].strip(): raise ValueError('Record the source-to-output mapping')
    ops=spec['operations']
    if not isinstance(ops,list) or not 1<=len(ops)<=1000: raise ValueError('Bound the operation list')
    if spec['mode']=='create':
        first=next((i for i,o in enumerate(ops) if isinstance(o,dict) and o.get('action')=='add_slide'),None)
        if first is None or any(not isinstance(o,dict) or o.get('action')!='set_canvas' for o in ops[:first]):
            raise ValueError('New decks must add a slide before slide/object operations')
    for op in ops:
        if not isinstance(op,dict) or op.get('action') not in ACTIONS: raise ValueError('Unsupported authoring action')
        required,optional=ACTIONS[op['action']]
        if not required<=set(op) or set(op)-required-optional: raise ValueError('Missing or unknown operation fields')
        for k in ('slide','index','row','column','before'):
            if k in op and (type(op[k]) is not int or op[k]<1): raise ValueError('Use one-based sequential selectors')
        for k in ('text','notes','layout','font','path'):
            if k in op and (not isinstance(op[k],str) or len(op[k])>100000): raise ValueError('Invalid text field')
        if 'height_mode' in op and op['height_mode'] not in ('fixed','fit'): raise ValueError('Invalid text height mode')
        if 'skipped' in op and type(op['skipped']) is not bool: raise ValueError('Use boolean skipped state')
        if 'kind' in op and op['kind'] not in ('text_item','shape'): raise ValueError('Unsupported text selector')
        for k in ('size','width','height'):
            if k in op: number(op[k],True)
        if 'color' in op and (not isinstance(op['color'],str) or len(op['color'])!=6 or any(c not in '0123456789abcdefABCDEF' for c in op['color'])): raise ValueError('Use RGB hex color')
        if 'bounds' in op:
            b=op['bounds']
            if not isinstance(b,list) or len(b)!=4: raise ValueError('Use x,y,width,height bounds')
            for i,v in enumerate(b):
                number(v,i>1)
                if v<0: raise ValueError('Negative geometry')
        if op['action']=='add_table':
            rows=op['cells']
            if not isinstance(rows,list) or not rows or len(rows)>100 or not isinstance(rows[0],list) or not 1<=len(rows[0])<=100: raise ValueError('Bounded table required')
            for row in rows:
                if not isinstance(row,list) or len(row)!=len(rows[0]): raise ValueError('Rectangular table required')
                for value in row: scalar(value)
        if op['action']=='set_cell': scalar(op['value'])
        if op['action']=='add_chart':
            if op['chart_type'] not in CHARTS: raise ValueError('Unsupported chart type')
            for k in ('rows','columns'):
                if not isinstance(op[k],list) or not 1<=len(op[k])<=100 or any(not isinstance(v,str) for v in op[k]): raise ValueError('Chart labels required')
            if not isinstance(op['data'],list) or len(op['data'])!=len(op['rows']): raise ValueError('Chart row mismatch')
            for row in op['data']:
                if not isinstance(row,list) or len(row)!=len(op['columns']): raise ValueError('Chart column mismatch')
                for value in row: number(value)
        if op['action']=='add_image':
            p=native.checked_path(op['path'])
            if not p.is_absolute() or p.is_symlink() or not p.is_file() or p.suffix.lower() not in ('.png','.jpg','.jpeg') or p.stat().st_size>50*1024*1024: raise ValueError('Use a local bounded PNG/JPEG asset')
            if hashlib.sha256(p.read_bytes()).hexdigest()!=op['sha256']: raise ValueError('Image hash mismatch')
    return spec


def author(spec, output, receipt, pdf, source=None):
    validate_spec(spec)
    native.fresh_paths(output,receipt,pdf)
    if Path(output).suffix.lower()!='.key': raise ValueError('Deliver a native .key candidate')
    if (source is None)!=(spec['mode']=='create'): raise ValueError('Source and mode disagree')
    if source:
        source,digest=native.source_identity(source)
        if digest!=spec['source_sha256']: raise ValueError('Stale source')
        native.outputs_outside_sources([source],[output,receipt,pdf])
    native.require_native_environment()
    work=Path(tempfile.mkdtemp(prefix='palate-author-')).resolve()
    candidate=work/'candidate.key'
    if source: native.copy_new(source,candidate)
    ops=json.loads(json.dumps(spec['operations']))
    for i,op in enumerate(ops):
        if op['action']=='add_image':
            asset=work/('asset-'+str(i)+Path(op['path']).suffix.lower());shutil.copyfile(op['path'],asset)
            if hashlib.sha256(asset.read_bytes()).hexdigest()!=op['sha256']: raise ValueError('Asset changed during staging')
            op['path']=str(asset)
    result=native.invoke_native({'command':'author','document':str(candidate),'pdf':str(work/'preview.pdf'),'mode':spec['mode'],'operations':ops},work)
    actual=native.validate_inventory(result['inventory'])
    native.source_identity(candidate)
    reopened=native.inspect_native(candidate)['inventory']
    if native.compare_inventory(actual,reopened): raise ValueError('Authoring save/reopen inventory mismatch; scratch retained')
    native.check_pdf(work/'preview.pdf')
    if source and native.source_identity(source)[1]!=digest: raise ValueError('Source changed during authoring')
    record={'schema_version':1,'status':'candidate','candidate_sha256':native.source_identity(candidate)[1],'native_application':'Keynote','keynote_version':result['keynote_version'],'content_ledger':spec['content_ledger'],'inventory':reopened,'save_reopen_status':'passed','native_review':'pending','limitations':['Chart internals, equations, layout inheritance and playback require native application review.']}
    created=[]
    try:
        native.copy_new(candidate,output,created);native.copy_new(work/'preview.pdf',pdf,created);native.save_json(receipt,record,created)
    except Exception:
        native.remove_created(created);raise
    shutil.rmtree(work)
    return record



def finalize_authored(candidate, review, output, report):
    candidate, digest = native.source_identity(candidate)
    native.fresh_paths(output, report)
    native.outputs_outside_sources([candidate], [output, report])
    if Path(output).suffix.lower() != '.key': raise ValueError('Final output must be .key')
    inspection = native.inspect_native(candidate)
    native.validate_review(review, digest, 'Keynote', [s['skipped'] for s in inspection['inventory']['slides']])
    if native.source_identity(candidate)[1] != digest: raise ValueError('Candidate changed during final review')
    created=[]
    try:
        native.copy_new(candidate, output, created)
        native.save_json(report, {'status':'finalized-as-reviewed','candidate_sha256':digest,'review':review,'limitations':['Recorded native judgments are not automatic scientific certification.']}, created)
    except Exception:
        native.remove_created(created); raise
    return {'status':'finalized-as-reviewed'}


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--spec');p.add_argument('--finalize');p.add_argument('--review');p.add_argument('--source');p.add_argument('--output',required=True);p.add_argument('--receipt',required=True);p.add_argument('--pdf')
    a=p.parse_args()
    if a.finalize:
        if not a.review or a.spec or a.source: p.error('Finalization needs --finalize and --review only, plus output/receipt')
        result=finalize_authored(a.finalize,native.load_json(a.review),a.output,a.receipt)
    else:
        if not a.spec or not a.pdf or a.review: p.error('Authoring needs --spec and --pdf')
        result=author(native.load_json(a.spec),a.output,a.receipt,a.pdf,a.source)
    print(json.dumps({'status':result['status']}))

if __name__=='__main__': main()
