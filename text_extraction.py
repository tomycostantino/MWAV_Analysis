import fitz


def extract_text(filename: str):
    # Open the PDF file and read its contents
    pdf_doc = fitz.open(filename)
    pdf_text = ''

    for page in pdf_doc:
        pdf_text += page.get_text()

    # split sms by each \n
    messages = pdf_text.splitlines()

    # Open the text file containing the messages
    file = open('messages.txt', 'w')

    # append messages line by line to then move into csv
    for message in messages:
        file.write(message + '\n')

    file.close()


if __name__ == '__main__':
    extract_text('sms.pdf')
