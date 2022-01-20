import PyPDF2
import pdfminer
print(dir(pdfminer))

with open("challengers2.pdf", "rb") as binstream:
    file = PyPDF2.PdfFileReader(binstream)
    i = 2
    ob = (file.getPage(i).extractText())
    print(ob)

# k = pdfminer.high_level.extract_text("challengers2.pdf", page_numbers=[2, 3, 4])
# print(k)
