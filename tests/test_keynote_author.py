"""Authoring request rejection tests; these do not establish Keynote execution."""
import copy,sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'scripts'))
import keynote_author as a
class KeynoteAuthorTests(unittest.TestCase):
 def spec(self):return {'schema_version':1,'mode':'create','source_sha256':None,'content_ledger':'Synthetic fixture','operations':[{'action':'add_slide'},{'action':'add_text','slide':1,'text':'Synthetic','bounds':[20,20,500,60]}]}
 def test_supported_spec(self):a.validate_spec(self.spec())
 def test_unknown_action_and_extra_code_rejected(self):
  for op in [{'action':'eval','code':'arbitrary'},dict(self.spec()['operations'][1],code='arbitrary')]:
   s=self.spec();s['operations']=[op]
   with self.assertRaises(ValueError):a.validate_spec(s)
 def test_invalid_geometry_and_selectors_rejected(self):
  for field,value in [('bounds',[0,0,float('nan'),100]),('bounds',[0,0,100,0]),('slide',True),('slide',0),('size',-1),('color','red')]:
   s=self.spec();s['operations'][1][field]=value
   with self.assertRaises(ValueError):a.validate_spec(s)
 def test_chart_dimensions_rejected(self):
  s=self.spec();s['operations']=[{'action':'add_slide'},dict(action='add_chart',slide=1,rows=['X'],columns=['A','B'],data=[[1]],chart_type='vertical_bar_2d',bounds=[0,0,100,100])]
  with self.assertRaises(ValueError):a.validate_spec(s)
 def test_missing_source_hash_or_ledger_rejected(self):
  for field,value in [('mode','edit'),('content_ledger','')]:
   s=self.spec();s[field]=value
   with self.assertRaises(ValueError):a.validate_spec(s)
 def test_ragged_table_and_formula_rejected(self):
  for cells in [[[1,2],[3]], [['=1+2']]]:
   s=self.spec();s['operations']=[{'action':'add_slide'},dict(action='add_table',slide=1,cells=cells,bounds=[0,0,100,100])]
   with self.assertRaises(ValueError):a.validate_spec(s)
if __name__=='__main__':unittest.main()
