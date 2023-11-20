import os
import shutil
import PyPDF2


# move o arquivo e o manda para algo semelhante a uma "lixeira"
def move_files(arquivo):
    diretorio = Arquivo.get_diretorio()
    lixo = lixeira()
    selected_file = os.path.join(diretorio, replace_file(arquivo))
    shutil.move(selected_file, os.path.join(lixo, replace_file(arquivo)))


# main projeto
def main():
    lista = list_pdfs()
    for arquivo in lista:
        type_pdf(arquivo)


# separa cada palavra e procura uma palavra específica
def locate_words(arquivo):
     padroniza_texto(arquivo)
     page_content = padroniza_texto(arquivo)
     for palavra in page_content.split():
         print(palavra)


# add as páginas para o dicionário
def add_dicio():
    conteudo = padroniza_texto('/Users/9002874/fred/testef/ctxt.pdf')
    my_dict = {"pdf": 1, "conteudo": conteudo}
    print(my_dict)


def read_pdfs():
    pdf_file = open("/Users/9002874/downloads/boleto.pdf", 'rb')
    read = PyPDF2.PdfFileReader(pdf_file)
    total = read.numPages
    for pg in range(total):
        page = read.getPage(pg)
        page_content = page.extract_text()
        if "SF0001" in page_content:
            key = "SF0001"
        pg += 1
    return key


read_pdfs()
