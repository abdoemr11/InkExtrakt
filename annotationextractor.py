import fitz


class AnnotationExtractor:
    def __init__(self, doc):
        self.doc = doc
        self.line_height = 50

    def extract_annotations(self):
        extracted_annotations = []

        for page in self.doc:
            wordlist = page.get_text("words")

            for annot in page.annots():
                annot_type = annot.type[0]

                if annot_type == 15:  # Freehand annotation
                    extracted_annotation = self.extract_freehand_annotation(
                        annot, page, wordlist)
                    extracted_annotations.append(extracted_annotation)

        return extracted_annotations

    def extract_freehand_annotation(self, annot, page, wordlist):
        points = annot.vertices

        if points is None:
            return None

        extracted_text = []
        for point in points:
            if len(point) >= 2:
                first_point = min(point, key=lambda p: p[0])
                last_point = max(point, key=lambda p: p[0])
                max_y = max(point, key=lambda p: p[1])
                x0, y0 = first_point[:2]
                x1, y1 = last_point[:2]
                line_rect = fitz.Rect(x0, max_y[1], x1, max_y[1])

                text_above_line = self.get_text_above_line(wordlist, line_rect)
                extracted_text.extend(text_above_line)

        return {
            'type': 'Freehand Annotation',
            'page_number': page.number + 1,
            'text': extracted_text
        }

    def get_text_above_line(self, wordlist, line_rect):
        text_above_line = [
            w[4] for w in wordlist if self.check_conditions(w, line_rect)
        ]
        return text_above_line

    def check_conditions(self, w, line_rect):
        return (w[1] <= line_rect.y0 and w[1] >= line_rect.y0 - self.line_height
                and w[3] <= line_rect.y1 and w[3] >= line_rect.y1 - self.line_height
                and w[0] >= line_rect.x0
                and w[2] <= line_rect.x1)
