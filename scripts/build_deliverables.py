"""Build proposal DOCX/HTML and editable PPTX plus a PDF preview, without Office."""
from pathlib import Path
import re, json, html, zipfile
from xml.sax.saxutils import escape as X
import fitz

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT/'deliverables'; OUT.mkdir(exist_ok=True)
W,H=960,540
NS='http://schemas.openxmlformats.org'
PKG='http://schemas.openxmlformats.org/package/2006/relationships'

def rels(entries):
    return '<?xml version="1.0" encoding="UTF-8" standalone="yes"?><Relationships xmlns="'+PKG+'">'+''.join(f'<Relationship Id="rId{i}" Type="{NS}/officeDocument/2006/relationships/{typ}" Target="{target}"/>' for i,typ,target in entries)+'</Relationships>'

def rect(x,y,w,h,text='',size=20,fill='FFFFFF',color='172D43',line=None):
    return dict(x=x,y=y,w=w,h=h,text=text,size=size,fill=fill,color=color,line=line)

def shape(o,i):
    x,y,w,h=[int(o[k]*12700) for k in ['x','y','w','h']]
    fill=f'<a:solidFill><a:srgbClr val="{o["fill"]}"/></a:solidFill>' if o['fill'] else '<a:noFill/>'
    ln=f'<a:ln w="12700"><a:solidFill><a:srgbClr val="{o["line"]}"/></a:solidFill></a:ln>' if o['line'] else '<a:ln><a:noFill/></a:ln>'
    paras=''.join('<a:p><a:pPr marL="0" marR="0"><a:lnSpc><a:spcPct val="115000"/></a:lnSpc></a:pPr><a:r><a:rPr lang="zh-TW" sz="'+str(int(o['size']*100))+'"><a:solidFill><a:srgbClr val="'+o['color']+'"/></a:solidFill><a:latin typeface="Microsoft JhengHei"/><a:ea typeface="Microsoft JhengHei"/></a:rPr><a:t>'+X(t)+'</a:t></a:r><a:endParaRPr lang="zh-TW"/></a:p>' for t in o['text'].split('\n'))
    if o['text'] in ['→','↓','←']:
        x-=76200; w+=152400
    return f'<p:sp><p:nvSpPr><p:cNvPr id="{i}" name="Text {i}"/><p:cNvSpPr/><p:nvPr/></p:nvSpPr><p:spPr><a:xfrm><a:off x="{x}" y="{y}"/><a:ext cx="{w}" cy="{h}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom>{fill}{ln}</p:spPr><p:txBody><a:bodyPr wrap="square" lIns="76200" tIns="50800" rIns="76200" bIns="50800"/><a:lstStyle/>{paras}</p:txBody></p:sp>'

EMPTY='<p:nvGrpSpPr><p:cNvPr id="1" name=""/><p:cNvGrpSpPr/><p:nvPr/></p:nvGrpSpPr><p:grpSpPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="0" cy="0"/><a:chOff x="0" y="0"/><a:chExt cx="0" cy="0"/></a:xfrm></p:grpSpPr>'
PNS=f'xmlns:a="{NS}/drawingml/2006/main" xmlns:r="{NS}/officeDocument/2006/relationships" xmlns:p="{NS}/presentationml/2006/main"'

def deck(slides):
    pdf=fitz.open(); overflows=[]
    with zipfile.ZipFile(OUT/'Proposal.pptx','w',zipfile.ZIP_DEFLATED) as z:
        overrides=[('/ppt/presentation.xml','presentationml.presentation.main'),('/ppt/slideMasters/slideMaster1.xml','presentationml.slideMaster'),('/ppt/slideLayouts/slideLayout1.xml','presentationml.slideLayout'),('/ppt/theme/theme1.xml','theme')]
        overrides += [(f'/ppt/slides/slide{i}.xml','presentationml.slide') for i in range(1,len(slides)+1)]
        z.writestr('[Content_Types].xml','<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/>'+''.join(f'<Override PartName="{p}" ContentType="application/vnd.openxmlformats-officedocument.{t}+xml"/>' for p,t in overrides)+'</Types>')
        z.writestr('_rels/.rels',rels([(1,'officeDocument','ppt/presentation.xml')]))
        z.writestr('ppt/presentation.xml',f'<p:presentation {PNS}><p:sldMasterIdLst><p:sldMasterId id="2147483648" r:id="rId1"/></p:sldMasterIdLst><p:sldIdLst>'+''.join(f'<p:sldId id="{255+i}" r:id="rId{i+1}"/>' for i in range(1,len(slides)+1))+f'</p:sldIdLst><p:sldSz cx="{W*12700}" cy="{H*12700}" type="screen16x9"/><p:notesSz cx="6858000" cy="9144000"/></p:presentation>')
        z.writestr('ppt/_rels/presentation.xml.rels',rels([(1,'slideMaster','slideMasters/slideMaster1.xml')]+[(i+1,'slide',f'slides/slide{i}.xml') for i in range(1,len(slides)+1)]))
        clr='<p:clrMap accent1="accent1" accent2="accent2" accent3="accent3" accent4="accent4" accent5="accent5" accent6="accent6" bg1="lt1" bg2="lt2" folHlink="folHlink" hlink="hlink" tx1="dk1" tx2="dk2"/>'
        z.writestr('ppt/slideMasters/slideMaster1.xml',f'<p:sldMaster {PNS}><p:cSld><p:spTree>{EMPTY}</p:spTree></p:cSld>{clr}<p:sldLayoutIdLst><p:sldLayoutId id="2147483649" r:id="rId1"/></p:sldLayoutIdLst><p:txStyles><p:titleStyle/><p:bodyStyle/><p:otherStyle/></p:txStyles></p:sldMaster>')
        z.writestr('ppt/slideMasters/_rels/slideMaster1.xml.rels',rels([(1,'slideLayout','../slideLayouts/slideLayout1.xml'),(2,'theme','../theme/theme1.xml')]))
        z.writestr('ppt/slideLayouts/slideLayout1.xml',f'<p:sldLayout {PNS} type="blank" preserve="1"><p:cSld name="Blank"><p:spTree>{EMPTY}</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sldLayout>')
        z.writestr('ppt/slideLayouts/_rels/slideLayout1.xml.rels',rels([(1,'slideMaster','../slideMasters/slideMaster1.xml')]))
        colors={'dk1':'000000','lt1':'FFFFFF','dk2':'172D43','lt2':'F3F6FA','accent1':'087E8B','accent2':'EAAD47','accent3':'3274A1','accent4':'8A6496','accent5':'59866C','accent6':'B66B5B','hlink':'0563C1','folHlink':'954F72'}
        theme='<a:theme xmlns:a="'+NS+'/drawingml/2006/main" name="Energy"><a:themeElements><a:clrScheme name="Energy">'+''.join(f'<a:{k}><a:srgbClr val="{v}"/></a:{k}>' for k,v in colors.items())+'</a:clrScheme><a:fontScheme name="Energy"><a:majorFont><a:latin typeface="Microsoft JhengHei"/><a:ea typeface="Microsoft JhengHei"/><a:cs typeface="Arial"/></a:majorFont><a:minorFont><a:latin typeface="Microsoft JhengHei"/><a:ea typeface="Microsoft JhengHei"/><a:cs typeface="Arial"/></a:minorFont></a:fontScheme><a:fmtScheme name="Energy"><a:fillStyleLst>'+('<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'*3)+'</a:fillStyleLst><a:lnStyleLst>'+('<a:ln w="12700"><a:solidFill><a:schemeClr val="phClr"/></a:solidFill><a:prstDash val="solid"/></a:ln>'*3)+'</a:lnStyleLst><a:effectStyleLst>'+('<a:effectStyle><a:effectLst/></a:effectStyle>'*3)+'</a:effectStyleLst><a:bgFillStyleLst>'+('<a:solidFill><a:schemeClr val="phClr"/></a:solidFill>'*3)+'</a:bgFillStyleLst></a:fmtScheme></a:themeElements></a:theme>'
        z.writestr('ppt/theme/theme1.xml',theme)
        for i,s in enumerate(slides,1):
            objects=[rect(0,0,W,H,fill='F3F6FA'),rect(0,0,12,H,fill='087E8B'),rect(34,22,892,60,s['title'],28,fill=None)]+s['objects']+[rect(36,508,880,24,f'ENERGY DETECTIVE  |  PROPOSAL    {i:02d} / {len(slides):02d}    '+s.get('source',''),9,fill=None,color='536579')]
            z.writestr(f'ppt/slides/slide{i}.xml',f'<p:sld {PNS}><p:cSld><p:spTree>{EMPTY}'+''.join(shape(o,j+2) for j,o in enumerate(objects))+'</p:spTree></p:cSld><p:clrMapOvr><a:masterClrMapping/></p:clrMapOvr></p:sld>')
            z.writestr(f'ppt/slides/_rels/slide{i}.xml.rels',rels([(1,'slideLayout','../slideLayouts/slideLayout1.xml')]))
            page=pdf.new_page(width=W,height=H)
            for o in objects:
                rr=fitz.Rect(o['x'],o['y'],o['x']+o['w'],o['y']+o['h'])
                rgb=lambda c: tuple(int(c[k:k+2],16)/255 for k in (0,2,4))
                if o['fill'] or o['line']: page.draw_rect(rr,color=rgb(o['line']) if o['line'] else None,fill=rgb(o['fill']) if o['fill'] else None)
                if o['text']:
                    page.insert_font(fontname='mj',fontfile='C:/Windows/Fonts/msjh.ttc')
                    inset=(0,0,0,0) if o['text'] in ['→','↓','←'] else (6,4,-6,-4)
                    avail=page.insert_textbox(rr+inset,o['text'],fontname='mj',fontsize=o['size'],color=rgb(o['color']),lineheight=1.15)
                    if avail<0: overflows.append((i,o['text'][:45],avail))
    pdf.subset_fonts()
    pdf.save(OUT/'Proposal-slides.pdf',garbage=4,deflate=True)
    for i in range(len(slides)):
        if slides[i].get('diagram'):
            p=pdf[i]; clip=fitz.Rect(28,85,932,496)
            p.get_pixmap(matrix=fitz.Matrix(2,2),clip=clip).save(ROOT/'assets'/f'{slides[i]["diagram"]}.png')
    pdf.close()
    if overflows: raise RuntimeError('Text overflow: '+repr(overflows))

def clean(s):
    s=re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'\1 (\2)',s)
    return s.replace('**','').replace('`','')

def blocks(md):
    lines=md.splitlines(); i=0
    while i<len(lines):
        t=lines[i]
        if t.startswith('```'):
            lang=t[3:].strip(); content=[]; i+=1
            while i<len(lines) and not lines[i].startswith('```'): content.append(lines[i]); i+=1
            yield ('code',lang,'\n'.join(content))
        elif t.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].startswith('|'):
                cells=[clean(re.sub(r'\[([^\]]+)\]\(([^)]+)\)',r'\1',x.strip())) for x in lines[i].strip('|').split('|')]
                if not all(re.fullmatch(r'[:\- ]+',c) for c in cells): rows.append(cells)
                i+=1
            yield ('table',rows); continue
        elif t.strip():
            m=re.match(r'^(#{1,6})\s+(.*)',t)
            yield ('heading',len(m[1]),clean(m[2])) if m else ('p',clean(t))
        i+=1

def document(md):
    body=[]; web=[]; imgs=[]; diagram_count=0
    def para(t,size=22,bold=False):
        return '<w:p><w:pPr><w:spacing w:after="100"/></w:pPr><w:r><w:rPr><w:rFonts w:ascii="Calibri" w:eastAsia="Microsoft JhengHei"/><w:sz w:val="'+str(size)+'"/>'+('<w:b/>' if bold else '')+'</w:rPr><w:t xml:space="preserve">'+X(t)+'</w:t></w:r></w:p>'
    for b in blocks(md):
        if b[0]=='heading':
            body.append(para(b[2],max(23,36-3*b[1]),True)); web.append(f'<h{min(b[1],6)}>{html.escape(b[2])}</h{min(b[1],6)}>')
        elif b[0]=='p': body.append(para(b[1])); web.append('<p>'+html.escape(b[1])+'</p>')
        elif b[0]=='table':
            rows=b[1]; body.append('<w:tbl><w:tblPr><w:tblW w:w="0" w:type="auto"/><w:tblBorders>'+''.join(f'<w:{x} w:val="single" w:sz="4" w:color="CBD5E1"/>' for x in ['top','left','bottom','right','insideH','insideV'])+'</w:tblBorders></w:tblPr>'+''.join('<w:tr>'+''.join('<w:tc><w:tcPr><w:tcW w:w="'+str(9500//len(row))+'" w:type="dxa"/></w:tcPr>'+para(cell,16,j==0)+'</w:tc>' for cell in row)+'</w:tr>' for j,row in enumerate(rows))+'</w:tbl>')
            web.append('<table>'+''.join('<tr>'+''.join(('<th>' if j==0 else '<td>')+html.escape(c)+('</th>' if j==0 else '</td>') for c in row)+'</tr>' for j,row in enumerate(rows))+'</table>')
        elif b[0]=='code' and b[1]=='mermaid':
            name=['architecture','flowchart'][min(diagram_count,1)]; diagram_count+=1
            imgs.append(name); idx=len(imgs); cx,cy=5800000,2637000
            body.append(f'<w:p><w:r><w:drawing><wp:inline distT="0" distB="0" distL="0" distR="0"><wp:extent cx="{cx}" cy="{cy}"/><wp:docPr id="{idx}" name="{name}"/><a:graphic><a:graphicData uri="{NS}/drawingml/2006/picture"><pic:pic><pic:nvPicPr><pic:cNvPr id="{idx}" name="{name}.png"/><pic:cNvPicPr/></pic:nvPicPr><pic:blipFill><a:blip r:embed="rId{idx}"/><a:stretch><a:fillRect/></a:stretch></pic:blipFill><pic:spPr><a:xfrm><a:off x="0" y="0"/><a:ext cx="{cx}" cy="{cy}"/></a:xfrm><a:prstGeom prst="rect"><a:avLst/></a:prstGeom></pic:spPr></pic:pic></a:graphicData></a:graphic></wp:inline></w:drawing></w:r></w:p>')
            web.append(f'<img src="../assets/{name}.png" alt="{name}">')
        else:
            for line in b[2].splitlines(): body.append(para(line,18))
            web.append('<pre>'+html.escape(b[2])+'</pre>')
    css='body{font:15px/1.75 "Microsoft JhengHei",sans-serif;max-width:1100px;margin:40px auto;color:#172d43;padding:0 24px}h1,h2,h3{color:#087e8b}table{border-collapse:collapse;width:100%;font-size:12px;margin:16px 0}td,th{border:1px solid #cbd5e1;padding:7px;vertical-align:top;overflow-wrap:anywhere}th{background:#e6f1f2}pre{white-space:pre-wrap;background:#f3f6fa;padding:16px}img{width:100%}p{overflow-wrap:anywhere}@media print{body{margin:0;font-size:11pt}h2,h3{break-after:avoid}tr,img{break-inside:avoid}}'
    (OUT/'Proposal.html').write_text('<!doctype html><html lang="zh-Hant"><meta charset="utf-8"><title>Energy Detective 專題提案</title><style>'+css+'</style><body>'+''.join(web)+'</body></html>',encoding='utf-8')
    with zipfile.ZipFile(OUT/'Proposal.docx','w',zipfile.ZIP_DEFLATED) as z:
        z.writestr('[Content_Types].xml','<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types"><Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/><Default Extension="xml" ContentType="application/xml"/><Default Extension="png" ContentType="image/png"/><Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/></Types>')
        z.writestr('_rels/.rels',rels([(1,'officeDocument','word/document.xml')]))
        z.writestr('word/document.xml',f'<w:document xmlns:w="{NS}/wordprocessingml/2006/main" xmlns:r="{NS}/officeDocument/2006/relationships" xmlns:wp="{NS}/drawingml/2006/wordprocessingDrawing" xmlns:a="{NS}/drawingml/2006/main" xmlns:pic="{NS}/drawingml/2006/picture"><w:body>'+''.join(body)+'<w:sectPr><w:pgSz w:w="11906" w:h="16838"/><w:pgMar w:top="1000" w:right="1000" w:bottom="1000" w:left="1000"/></w:sectPr></w:body></w:document>')
        z.writestr('word/_rels/document.xml.rels',rels([(i,'image',f'media/{n}.png') for i,n in enumerate(imgs,1)]))
        for n in set(imgs): z.write(ROOT/'assets'/f'{n}.png',f'word/media/{n}.png')

if __name__=='__main__':
    slides=json.loads((ROOT/'scripts/slides.json').read_text(encoding='utf-8'))
    deck(slides)
    document((ROOT/'research/proposal_source.md').read_text(encoding='utf-8'))
    print('Created DOCX, HTML, PPTX, PDF; no PDF text box overflows.')
