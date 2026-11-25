"""Build a reviewable character-level OCR suggestion anchored to Gemini.

The sources remain authoritative. A missing character is represented by None,
not an empty string; low-confidence disagreements are returned to the caller.
"""
from difflib import SequenceMatcher


def _align(reference, candidate):
    """Map candidate characters and insertions to positions in the reference."""
    chars = [None] * len(reference)
    insertions = [''] * (len(reference) + 1)
    for op, a0, a1, b0, b1 in SequenceMatcher(None, reference, candidate, autojunk=False).get_opcodes():
        if op == 'equal':
            chars[a0:a1] = candidate[b0:b1]
        elif op == 'replace':
            common = min(a1 - a0, b1 - b0)
            chars[a0:a0 + common] = candidate[b0:b0 + common]
            insertions[a0 + common] += candidate[b0 + common:b1]
        elif op == 'insert':
            insertions[a0] += candidate[b0:b1]
    return chars, insertions


def vote_ocr(gemini, tesseract, kimhannom):
    """Return a suggested transcription and disagreements, without altering inputs.

    Insertions absent from Gemini are proposed only when both other engines agree.
    All other insertions are marked as unresolved, including one-engine results.
    """
    sources = {'gemini': gemini, 'tesseract': tesseract, 'kimhannom': kimhannom}
    if any(not isinstance(value, str) or not value.strip() for value in sources.values()):
        raise ValueError('Voting cần kết quả không rỗng từ cả ba engine.')
    t_chars, t_insertions = _align(gemini, tesseract)
    k_chars, k_insertions = _align(gemini, kimhannom)
    output, disagreements = [], []
    for i in range(len(gemini) + 1):
        t_ins, k_ins = t_insertions[i], k_insertions[i]
        if t_ins or k_ins:
            chosen = t_ins if t_ins and t_ins == k_ins else ''
            disagreements.append({'reference_offset': i, 'kind': 'insertion',
                                  'gemini': '', 'tesseract': t_ins,
                                  'kimhannom': k_ins, 'chosen': chosen})
            output.append(chosen)
        if i == len(gemini):
            break
        g, t, k = gemini[i], t_chars[i], k_chars[i]
        chosen = t if t == k and t is not None else g
        if t is None and k is None:
            chosen = ''
        if not (g == t == k):
            disagreements.append({'reference_offset': i, 'kind': 'character',
                                  'gemini': g, 'tesseract': t,
                                  'kimhannom': k, 'chosen': chosen})
        output.append(chosen)
    return {'text': ''.join(output), 'disagreements': disagreements, 'sources': sources}
