import datetime


class AnnotationWriter:
    def __init__(self, annot_doc_path, basename):
        self.annot_doc_path = annot_doc_path
        self.basename = basename

    def write_annotations(self, annotations, page_count):
        with open(self.annot_doc_path, "w", encoding="utf-8") as annot_doc:
            self.write_annotation_header(annot_doc, page_count)
            self.write_extracted_annotations(
                annot_doc, annotations)

    def write_annotation_header(self, annot_doc, page_count):
        now = datetime.datetime.now()
        today = now.strftime("%Y-%m-%d %H:%M")
        today_long_form = now.strftime("%dth %B %Y, %A")
        time = now.strftime("%H:%M")

        annot_doc.write("#source/annotes\n")
        annot_doc.write(f"# Annots - {self.basename}\n\n")
        annot_doc.write("> ![info: Details]\n")
        annot_doc.write(f"> Title:: {self.basename}\n")
        annot_doc.write(f"> Pages:: {page_count}\n")
        annot_doc.write(f"> PDF:: [[{self.basename}.pdf]]\n")

    def write_extracted_annotations(self, annot_doc, annotations):
        for annotation in annotations:
            annot_doc.write(f"- {annotation['type']}")
            annot_doc.write(f"\t&mdash;*({annotation['page_number']})*\n")

            extracted_text = ' '.join(annotation['text'])
            annot_doc.write(f"{extracted_text}\n")
