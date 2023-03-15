import PyPDF2
import csv
import re


def txt_to_csv():
    # Define the regular expression for matching the date pattern
    date_regex = r'(\w{3}, \d{1,2} \w{3} at \d{1,2}:\d{2} [ap]m)'

    # Load the sample text from a file
    with open('text.txt', 'r') as f:
        text = f.read()

    # Split the text into a list of strings whenever there is a date
    parts = re.split(date_regex, text)

    # Remove any empty parts and group the date and message together
    parts = [(parts[i].strip(), parts[i + 1].strip()) for i in range(0, len(parts) - 1, 2) if parts[i]]

    # Write the parts to a CSV file
    with open('output.csv', 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Date', 'Message'])
        for part in parts:
            writer.writerow([part[1], part[0]])


def pdf_to_txt(file: str):
    pdf = PyPDF2.PdfReader(file)

    txt_file = open('text.txt', 'w+')
    txt_file.write("")
    txt_file.close()

    txt_file = open('text.txt', 'a')

    for page in pdf.pages:
        text = page.extract_text()
        txt_file.write(text)
        txt_file.write('\n')

    txt_file.close()


if __name__ == '__main__':
    pdf_to_txt('sms.pdf')
    txt_to_csv()
