from pypdf import PdfReader, PdfWriter

input_pdf = r"D:\BankLLM\data\4699202402016703286648.pdf"
output_pdf = "unlocked_statement.pdf"
password = "ayus1212"

reader = PdfReader(input_pdf)
reader.decrypt(password)
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

with open(output_pdf, "wb") as f:
    writer.write(f)

print("Password removed successfully!")
