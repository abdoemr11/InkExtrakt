import os
import fitz

from annotationextractor import AnnotationExtractor
from annotationwriter import AnnotationWriter


def process_file(filename):
    if not filename.endswith(".pdf"):
        return

    doc = fitz.open(filename)
    extractor = AnnotationExtractor(doc)
    extracted_annotations = extractor.extract_annotations()

    basename = os.path.splitext(filename)[0]
    foldername = f"Annots - {basename}"
    os.makedirs(foldername, exist_ok=True)
    annot_doc_path = f"./{foldername}/Annots - {basename}.md"

    writer = AnnotationWriter(annot_doc_path, basename)
    writer.write_annotations(extracted_annotations, doc.page_count)

    doc.close()


filelist = os.listdir()
print('filelsit', filelist)
common_tags = "annotations, import, status/pending, type/404"

for filename in filelist:
    process_file(filename)
