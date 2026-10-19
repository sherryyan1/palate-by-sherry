"""Shared native delivery gate. Recorded judgments are evidence, not automatic certification."""
REVIEW_FIELDS = ('visual_status', 'scientific_status', 'editability_status',
                 'playback_status', 'protected_content_status')


def validate_review(review, digest, application, hidden):
    if review.get('candidate_sha256') != digest or review.get('native_application') != application:
        raise ValueError('Review must bind this candidate and its native delivery application')
    if not isinstance(hidden, list) or not hidden or any(type(v) is not bool for v in hidden):
        raise ValueError('Actual native slide visibility inventory is required')
    count = len(hidden)
    coverage = review.get('reviewed_slides')
    if not isinstance(coverage, list) or any(type(i) is not int for i in coverage) or sorted(coverage) != list(range(1, count + 1)):
        raise ValueError('Review every slide exactly once, including hidden/skipped backup slides')
    for field in REVIEW_FIELDS:
        if review.get(field) != 'passed':
            raise ValueError('Unresolved native review: ' + field)
    if not isinstance(review.get('reviewer'), str) or not review['reviewer'].strip():
        raise ValueError('Record the actual reviewer')
    evidence = review.get('evidence')
    if not isinstance(evidence, list) or not evidence or any(not isinstance(e, str) or not e.strip() for e in evidence):
        raise ValueError('Record actual native review evidence')
    if review.get('remaining_issues') != []:
        raise ValueError('Resolve remaining issues before final delivery')
    ending = review.get('ending_review', {})
    policy = ending.get('policy')
    if policy in ('explicitly_omitted', 'out_of_scope'):
        if not isinstance(ending.get('reason'), str) or not ending['reason'].strip():
            raise ValueError('Record the user omission or selected-slide scope reason')
        return
    if policy != 'required':
        raise ValueError('Record the ending requirement; do not infer an omission')
    summary, closing, appendix = (ending.get(k) for k in ('summary_slide', 'closing_slide', 'appendix_start_slide'))
    if any(type(i) is not int or not 1 <= i <= count for i in (summary, closing)) or summary >= closing:
        raise ValueError('Summary and closing must be distinct, ordered actual slides')
    if appendix is not None and (type(appendix) is not int or not closing < appendix <= count):
        raise ValueError('Closing must precede the first appendix')
    if hidden[closing - 1] or hidden[summary - 1]:
        raise ValueError('Required summary and closing must be visible in normal playback')
    visible = [i for i in range(summary + 1, count + 1) if not hidden[i - 1]]
    if not visible or visible[0] != closing:
        raise ValueError('Closing must follow the summary in the main playback sequence')
    for field in ('separate_page_status', 'native_render_status', 'playback_status', 'skipped_appendix_status'):
        if ending.get(field) != 'passed':
            raise ValueError('Ending review pending: ' + field)
    if not isinstance(ending.get('evidence'), str) or not ending['evidence'].strip():
        raise ValueError('Record actual ending render and playback observations')
