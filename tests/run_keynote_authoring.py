"""Private synthetic native-authoring check. No research input or source document is used."""
import sys,json,traceback
from pathlib import Path
from datetime import datetime
import argparse
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'scripts'))
import keynote_author as author
import keynote_native as native
parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--output',required=True)
out=Path(parser.parse_args().output).resolve()
if out==ROOT or ROOT in out.parents: raise ValueError('Keep native output outside the repository')
out.mkdir(parents=True)
result={'status':'running','output':str(out),'checks':{}}
def save(): (out/'result.json').write_text(json.dumps(result,indent=2))
def title(slide):
 return next(item['text'] for item in slide['text_items'] if item['text'])
def run(name,spec,source=None):
 try:
  r=author.author(spec,out/(name+'.key'),out/(name+'.json'),out/(name+'.pdf'),source)
  inv=r['inventory'];slides=inv['slides']
  if name=='create':
   assert len(slides)==4 and [s['skipped'] for s in slides]==[False,False,False,True]
   assert slides[0]['counts']['tables']==1 and slides[0]['counts']['charts']==1
   assert [title(s) for s in slides]==['Synthetic evidence','Summary','Thank you · Questions','Technical appendix']
   assert slides[0]['tables'][0]['cells'][4]['value']=='12'
   for slide in slides:
    item=next(x for x in slide['text_items'] if x['text'])
    assert item['style']['color']=='182C32', item['style']
    assert item['style']['font_size_pt']==40, item['style']
    assert item['bounds_points'][:3]==[64,50,1100] and 0 < item['bounds_points'][3] <= 80, item['bounds_points']
    assert not any(x['bounds_points'][2]>0 and not x['text'] for x in slide['shapes']), 'Unexpected placeholder'
  if name=='text': assert title(slides[2])=='Thank you · Discussion'
  if name=='table': assert slides[0]['tables'][0]['cells'][4]['value']=='13'
  if name=='duplicate': assert len(slides)==5
  if name=='move': assert [title(s) for s in slides]==['Synthetic evidence','Technical appendix','Summary','Thank you · Questions']
  if name=='delete': assert len(slides)==3
  if name=='notes_visibility': assert slides[3]['notes']=='Updated synthetic appendix' and slides[3]['skipped'] is False
  result['checks'][name]={'status':'passed','save_reopen':r['save_reopen_status'],'slide_count':len(r['inventory']['slides'])}
  save();return out/(name+'.key')
 except Exception as e:
  result['checks'][name]={'status':'failed','error_type':type(e).__name__,'error':str(e),'traceback':traceback.format_exc()};save();return None
save()
ops=[{'action':'set_canvas','width':1280,'height':720}]
for i in range(4):
 ops += [{'action':'add_slide','notes':'Synthetic fixture slide '+str(i+1),'skipped':i==3}, {'action':'add_text','slide':i+1,'text':['Synthetic evidence','Summary','Thank you · Questions','Technical appendix'][i],'bounds':[64,50,1100,80],'height_mode':'fit','font':'Helvetica','size':40,'color':'182C32'}]
ops += [{'action':'add_table','slide':1,'cells':[['Series','A','B'],['Observed',12,18],['Generated',11,17]],'bounds':[64,180,480,240]}, {'action':'add_chart','slide':1,'rows':['Observed','Generated'],'columns':['A','B'],'data':[[12,18],[11,17]],'chart_type':'vertical_bar_2d','bounds':[620,180,550,300]}, {'action':'add_shape','slide':2,'text':'Synthetic takeaway','bounds':[150,220,900,150],'size':30}]
spec={'schema_version':1,'mode':'create','source_sha256':None,'operations':ops,'content_ledger':'Synthetic data only. Evidence, summary, separate closing, skipped appendix.'}
created=run('create',spec)
if created:
 inventory=json.loads((out/'create.json').read_text())['inventory']
 closing_index=next(item['index'] for item in inventory['slides'][2]['text_items'] if item['text']=='Thank you · Questions')
 edits=[('text',[{'action':'set_text','slide':3,'kind':'text_item','index':closing_index,'text':'Thank you · Discussion','size':42}]),('table',[{'action':'set_cell','slide':1,'index':1,'row':2,'column':2,'value':13}]),('duplicate',[{'action':'duplicate_slide','slide':2}]),('move',[{'action':'move_slide','slide':4,'before':2}]),('delete',[{'action':'delete_slide','slide':4}]),('notes_visibility',[{'action':'set_slide','slide':4,'notes':'Updated synthetic appendix','skipped':False}])]
 for name,operations in edits:
  run(name,{'schema_version':1,'mode':'edit','source_sha256':native.source_identity(created)[1],'operations':operations,'content_ledger':'Synthetic isolated '+name+' operation; original is immutable.'},created)
result['status']='passed' if all(c['status']=='passed' for c in result['checks'].values()) else 'failed'
result['review']='Native visual, chart-data editability and playback review pending; this script does not certify them.'
save();print(json.dumps(result,indent=2))
