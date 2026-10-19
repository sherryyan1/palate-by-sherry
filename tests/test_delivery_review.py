"""Both native formats use the same evidence and ending gate."""
import copy
import importlib.util
from pathlib import Path
import unittest
spec=importlib.util.spec_from_file_location('delivery_review',Path(__file__).resolve().parents[1]/'scripts/delivery_review.py')
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
class DeliveryReviewTests(unittest.TestCase):
 def record(self,application):
  return dict(candidate_sha256='a'*64,native_application=application,reviewed_slides=[1,2,3,4],reviewer='Synthetic reviewer',evidence=['Synthetic gate test, not native review'],remaining_issues=[],**{k:'passed' for k in m.REVIEW_FIELDS},ending_review=dict(policy='required',summary_slide=2,closing_slide=3,appendix_start_slide=4,separate_page_status='passed',native_render_status='passed',playback_status='passed',skipped_appendix_status='passed',evidence='Synthetic review record'))
 def test_same_gate_for_both_applications(self):
  for app in ['PowerPoint','Keynote']:
   m.validate_review(self.record(app),'a'*64,app,[False,False,False,True])
 def test_pending_or_absent_native_checks_fail_for_both(self):
  for app in ['PowerPoint','Keynote']:
   for key in m.REVIEW_FIELDS:
    r=self.record(app);r[key]='pending'
    with self.assertRaises(ValueError):m.validate_review(r,'a'*64,app,[False]*4)
 def test_wrong_application_hash_or_duplicate_coverage_fails(self):
  for key,value in [('native_application','Other'),('candidate_sha256','b'*64),('reviewed_slides',[1,2,3,3,4]),('evidence',[]),('remaining_issues',['unreviewed'])]:
   r=self.record('Keynote');r[key]=value
   with self.assertRaises(ValueError):m.validate_review(r,'a'*64,'Keynote',[False]*4)
 def test_ending_failure_cases(self):
  for change in [dict(closing_slide=2),dict(closing_slide=4,appendix_start_slide=3),dict(closing_slide=None),dict(playback_status='pending'),dict(native_render_status='pending'),dict(evidence=''),dict(policy='unknown')]:
   r=self.record('Keynote');r['ending_review'].update(change)
   with self.assertRaises(ValueError):m.validate_review(r,'a'*64,'Keynote',[False,False,False,True])
 def test_hidden_closing_fails(self):
  with self.assertRaises(ValueError):m.validate_review(self.record('PowerPoint'),'a'*64,'PowerPoint',[False,False,True,True])
 def test_explicit_scope_exception_needs_reason(self):
  r=self.record('Keynote');r['ending_review']={'policy':'explicitly_omitted'}
  with self.assertRaises(ValueError):m.validate_review(r,'a'*64,'Keynote',[False]*4)
  r['ending_review']['reason']='User requested no closing page';m.validate_review(r,'a'*64,'Keynote',[False]*4)
if __name__=='__main__':unittest.main()
