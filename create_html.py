#!/usr/bin/env python

# imports
import glob
import os

# constants
f_study = 'study/'
f_thumbs = 'thumbs/'
thumb_size = 360
im_parts = [
    'CASE{0:d}.jpg',
    'CASE{0:d}A.jpg',
    'CASE{0:d}B.jpg',
    'CASE{0:d}NP.jpg',
    'CASE{0:d}P.jpg',
]
last_case = 294
surveylink = '<iframe id="JotFormIFrame-222076621564151" title="Blue White Veil v2" onload="window.parent.scrollTo(0,0)" allowtransparency="true" allowfullscreen="false" allow="geolocation; microphone; camera" src="https://form.jotform.com/222076621564151" frameborder="0" style=" min-width: 100%; min-height:100%; border:none;" scrolling="yes" > </iframe>'
# function for labeling
def file_label(f):
    l = 'Non-Polarized'
    if 'P' in f:
        if 'N' not in f:
            l = 'Polarized'
    return l

# load templates
with open('templates/case.html') as f:
    t_case = f.read()
with open('templates/cases.html') as f:
    t_cases = f.read()

# find JPGs for each case
casefiles = [[]] * last_case
for c in range(1, last_case+1):
    files = []
    for p in im_parts:
        files += glob.glob(f_study + p.format(c))
    if len(files) > 0:
        casefiles[c-1] = [c] + files

# remove missing
casefiles = list(filter(lambda v: len(v) > 0, casefiles))
lastci = len(casefiles) - 1

# generate case links
caselist = "\n\t\t\t".join(
    ['<div><a href="./study/case_{0:d}.html">Case {0:d}</a></div>'.format(v[0]) for v in casefiles])

# set in template and write
f_cases = t_cases.replace('$CASELIST$', caselist)
with open(f_study + 'cases.html', 'w') as f:
    f.write(f_cases)

# iterate over cases
for ci, case in enumerate(casefiles):
    num = case[0]
    if ci < lastci:
        nextnum = casefiles[ci+1][0]
    else:
        nextnum = casefiles[0][0]
    files = case[1:]
    thumbs = [v.replace(f_study, f_thumbs) for v in files]
    labels = [file_label(v) for v in files]
    caseimages = "".join(
        ['<td style="vertical-align: top; "width="{0:d}" height="{0:d}"><a href="./{1:s}" target="_blank"><img src="./{2:s}" border="0" /><br />{3:s}</td>'.format(
            thumb_size, imf, tf, il
        ) for imf, tf, il in zip(files, thumbs, labels)]
    )
    f_case = t_case.replace('$CASEIMAGES$', caseimages)
    f_case = f_case.replace('$CASENUMBER$', str(num))
    f_case = f_case.replace('$NEXTCASE$', str(nextnum))
    f_case = f_case.replace('$SURVEYLINK$', surveylink)
    with open(f_study + 'case_{0:d}.html'.format(num), 'w') as f:
        f.write(f_case)
