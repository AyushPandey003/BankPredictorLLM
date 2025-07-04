from pypdf import PdfReader, PdfWriter

input_pdf = r"D:\BankLLM\data\xxxxx.pdf"
output_pdf = "unlocked_statement.pdf"
password = "yourpass"

reader = PdfReader(input_pdf)
reader.decrypt(password)
writer = PdfWriter()

for page in reader.pages:
    writer.add_page(page)

with open(output_pdf, "wb") as f:
    writer.write(f)

print("Password removed successfully!")
