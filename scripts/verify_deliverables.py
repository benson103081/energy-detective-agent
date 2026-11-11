"""Check deliverable structure, source coverage, references and local links.

This verifies proposal artifacts, not the future Agent or research hypotheses.
"""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import zipfile
import xml.etree.ElementTree as ET

import fitz
from docx import Document
from pptx import Presentation

ROOT = Path(__file__).resolve().parents[1]


def check(condition, message):
    if not condition:
        raise AssertionError(message)


class Links(HTMLParser):
    def __init__(self):
        super().__init__()
        self.targets = []

    def handle_starttag(self, tag, attrs):
        for key, value in attrs:
            if key in ("href", "src"):
                self.targets.append(value)


for name in ("Proposal.docx", "Proposal.pptx"):
    with zipfile.ZipFile(ROOT / "deliverables" / name) as archive:
        check(archive.testzip() is None, f"Invalid ZIP: {name}")
        for entry in archive.namelist():
            if entry.endswith((".xml", ".rels")):
                ET.fromstring(archive.read(entry))

slides = json.loads((ROOT / "scripts/slides.json").read_text())
ppt = Presentation(ROOT / "deliverables/Proposal.pptx")
pdf = fitz.open(ROOT / "deliverables/Proposal-slides.pdf")
check(len(ppt.slides) == len(pdf) == len(slides), "PPT/PDF/source slide count differs")
check(len(slides) >= 21, "Expected at least 21 slides in this proposal edition")
for index, page in enumerate(pdf):
    check(len(page.get_text().strip()) > 20, f"Empty PDF page: {index + 1}")
    for x0, y0, x1, y1, *_ in page.get_text("blocks"):
        check(x0 >= 0 and y0 >= 0 and x1 <= page.rect.width + 1 and y1 <= page.rect.height + 1,
              f"Text outside PDF page {index + 1}")
pdf.close()

doc = Document(ROOT / "deliverables/Proposal.docx")
check(len(doc.inline_shapes) == 2, "Expected architecture and flowchart in DOCX")
text = "\n".join(p.text for p in doc.paragraphs)
for heading in ("Abstract", "Introduction", "Related Work", "Deep Research", "Proposed Scheme", "References"):
    check(heading in text, f"Missing section: {heading}")
for marker in ("RQ1", "RQ2", "RQ3", "C01", "C10"):
    check(marker in text or any(marker in cell.text for t in doc.tables for row in t.rows for cell in row.cells),
          f"Missing evaluation marker: {marker}")

source = (ROOT / "research/proposal_source.md").read_text()
check(len(re.findall(r"^\| \[A[1-5]\]\(", source, re.M)) == 5, "AI article table must have 5 studies")
check(len(re.findall(r"^\| \[D\d+\] [^|]+ \|", source, re.M)) == 5,
      "Domain article table must have 5 studies")
check(len(re.findall(r"^\d+\. .*", source.split("### Q3.", 1)[1].split("### 十題", 1)[0], re.M)) == 10,
      "Expected ten deep research questions")
code = re.search(r"```text\n(.*?)\n```", source, re.S)[1]
numbers = [int(line.split()[0]) for line in code.splitlines()]
check(numbers == list(range(1, len(numbers) + 1)), "Pseudocode line numbers are not continuous")

html_path = ROOT / "deliverables/Proposal.html"
links = Links()
links.feed(html_path.read_text())
for target in links.targets:
    if target.startswith(("http:", "https:", "mailto:", "#")):
        continue
    check((html_path.parent / target.split("#")[0]).exists(), f"Broken HTML local link: {target}")
check(any("arxiv.org/html/2506.00630v1" in target for target in links.targets), "D9 reference is not linked")
for path in (ROOT / "README.md", ROOT / "DESIGN.md"):
    for target in re.findall(r"\]\(([^)]+)\)", path.read_text()):
        if not target.startswith(("http:", "https:", "#")):
            check((path.parent / target.split("#")[0]).exists(), f"Broken link in {path.name}: {target}")

print(f"PASS: {len(slides)} slides; DOCX/PPTX XML; PDF bounds; 5+5 articles; 10 questions; numbered algorithm; local links.")
print("Not evaluated: Agent execution, energy experiments, actual Word/PowerPoint rendering or YouTube video.")
