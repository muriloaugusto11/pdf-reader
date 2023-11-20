from PyPDF2 import PdfReader
import PyPDF2
import re
from pytesseract import pytesseract
import cv2
import sqlite3
import unidecode
import os
import shutil
from PIL import Image
from pdf2image import convert_from_path


# uma classe para encontrar os arquivos
class FileFinder:
    def __init__(self):
        self.local = "/Users/9002874/fred/auto/arquivos/"
        self.trash = "/Users/9002874/fred/auto/lixeira/"
        self.list_pdfs = []

    def get_local(self):
        return self.local

    def set_local(self, local):
        self.local = local

    def get_list_pdfs(self):
        return self.list_pdfs

    def set_list_pdfs(self):
        self.list_pdfs = os.listdir(FileFinder.get_local(self))

    def get_trash(self):
        return self.trash

    def set_trash(self, trash):
        self.trash = trash

    # pega apenas o nome dos pdfs OK
    def get_pdfs_names(self):
        pdfs = FileFinder.get_list_pdfs(self)
        lista_nomes = []
        for pdf in pdfs:
            if pdf.endswith(".pdf"):
                pdf = pdf.replace(".pdf", '')
                lista_nomes.append(pdf)
        return lista_nomes

    # pega a lista local de pdfs OK
    def get_local_pdfs(self):
        self.set_list_pdfs()
        lista_local_pdfs = []
        for pdf in self.get_list_pdfs():
            full_path = os.path.join(self.get_local(), pdf)
            lista_local_pdfs.append(full_path)
        return lista_local_pdfs

    # retorna o nome de 1 pdf de acordo com o seu endereço
    def get_pdf_name(self, arquivo):
        pdf = arquivo
        if pdf.endswith(".pdf"):
            # pdf = pdf.replace(".pdf", '')
            pdf = pdf.replace(self.local, '')
        return pdf

    # cria a lista com os arquivos e retorna a lista com eles OK
    def take_files(self):
        self.set_list_pdfs()
        return self.get_local_pdfs()


# uma classe para converter os arquivos
class FileConverter(FileFinder):
    def __init__(self):
        super().__init__()
        super().get_local_pdfs()
        super().set_list_pdfs()
        super().take_files()

    # converte pdfs para imgs OK
    def pdfs_to_img(self, arquivo):
        # for arquivo in self.take_files():
        pdf_pages = convert_from_path(arquivo)
        replace_pdf = arquivo.replace(".pdf", "")

        count = 0
        for page in pdf_pages:
            if int(count) > 9 < 100:
                jpeg_file = replace_pdf + "-" + "z" + str(count) + ".jpg"
                page.save(jpeg_file, 'JPEG')
                count += 1

            if int(count) > 99:
                jpeg_file = replace_pdf + "-" + "zz" + str(count) + ".jpg"
                page.save(jpeg_file, 'JPEG')
                count += 1

            else:
                jpeg_file = replace_pdf + "-" + str(count) + ".jpg"
                page.save(jpeg_file, 'JPEG')
                count += 1

    # move o arquivo e o manda para algo semelhante a uma "lixeira" OK
    def move_file(self, arquivo):
        origem = self.local
        destino = self.trash
        arq = self.get_pdf_name(arquivo)
        shutil.move(origem + arq, destino)
        try:
            return 'Arquivo movido com sucesso!'

        except:
            return 'Erro ao mover arquivo!'


# uma classe para ler, extrair informações e trabalhar com essas informações
class FileContent(FileConverter):
    def __init__(self):
        super().__init__()
        super().get_local_pdfs()
        super().set_list_pdfs()

    # lê um pdf que não seja originário de uma imagem
    def read_pdfs(self, pdf):
        self.get_local_pdfs()

        pdf_file = open(pdf, 'rb')
        read = PyPDF2.PdfFileReader(pdf_file)
        total = read.numPages
        dic = {}
        for pg in range(total):
            page = read.getPage(pg)
            page_content = page.extractText()
            #print(page_content)
            pg += 1
            dicio = {'Página': pg, 'Conteúdo': page_content}
            dic[pg] = dicio
        return dic

    # lê todas imagens de um diretório OK
    def read_all_imgs(self):
        myconfig = r'--psm 1 --oem 3'

        for arq in os.listdir(self.get_local()):
            if arq.endswith(".jpg"):
                full_path = os.path.join(self.get_local(), arq)
                print(pytesseract.image_to_string(Image.open(full_path), config=myconfig, lang='por'))

    # mostra se as páginas de 1 pdf são img ou txt OK
    def pdf_content_img_or_txt(self, arquivo):
        read = PdfReader(arquivo)
        total_pages = read.numPages
        lenght_letters_pdf = 0

        for pg in range(total_pages):
            pdf_page = read.getPage(pg)
            page_content = pdf_page.extractText()
            lenght_letters_page_pdf = len(page_content)

            if lenght_letters_page_pdf < 0:
                print("Arquivo " + arquivo + " página " + str(pg + 1) + " é de imagem, possui " + str(
                    lenght_letters_page_pdf) + " Letras")

            else:
                print("Arquivo " + arquivo + " página " + str(pg + 1) + " é de texto, possui " + str(
                    lenght_letters_page_pdf) + " Letras")
                lenght_letters_pdf += len(page_content)

            pg += 1

            if pg == total_pages:
                print("O PDF " + arquivo + " tem " + str(lenght_letters_pdf) + " Letras")

    # mostra se o pdf é img ou txt e chama as funções de leitura de arquivos OK
    def type_pdf(self, arquivo):
        read = PdfReader(arquivo)
        total_pages = read.numPages
        total_let = 0

        for pg in range(total_pages):
            pdf_page = read.getPage(pg)
            page_content = pdf_page.extractText()
            lenght_pg = len(page_content)
            # print("pg " + str(pg + 1) + " tem " + str(lenght_pg) + " Letras")
            total_let += lenght_pg
            pg += 1

        if total_let < 1:
            # print(str(arquivo) + " é img, com " + str(total_let) + " Letras")
            self.pdfs_to_img(arquivo)
            #self.move_file(arquivo)
            # self.pdf_content_img_or_txt(arquivo)
            self.read_all_imgs()

        else:
            print(str(arquivo) + " é txt, com " + str(total_pages) + " páginas e " + str(total_let) + " Letras totais")
            print(self.read_pdfs(arquivo))
            #self.move_file(arquivo)

    # trata o texto
    def padroniza_texto(self, arquivo):
        pdf_file = open(arquivo, 'rb')
        read = PyPDF2.PdfFileReader(pdf_file)
        total = read.numPages
        text = []

        for pg in range(total):
            page = read.getPage(pg)
            page_content = page.extractText()
            pg += 1
            page_content = unidecode.unidecode(str(page_content))
            page_content = page_content.lower()
            page_content = page_content.replace(',', '')
            text.append(page_content)
        return text

    # classifica e retorna as páginas do início, meio e fim
    def zona_txt(self, arquivo):
        paginas = self.padroniza_texto(arquivo)
        contador = 0
        total = len(paginas)

        for pagina in paginas:
            if contador == 1:
                print("\n" + str(contador) + "  Conteúdo do início \n s")
                print(pagina)
                contador += 1

            if contador == total:
                print("\n" + str(contador) + "  Conteúdo do fim \n ")
                print(pagina)
                break

            else:
                print("\n" + str(contador) + "  conteudo do meio \n ")
                print(pagina)
                contador += 1


class FileData(FileContent):
    def __init__(self):
        super().__init__()
        self.conexao = sqlite3.connect('meu_bsancozsswwwzpss.db')
        self.criar_tabela()

    def criar_tabela(self):
        c = self.conexao.cursor()

        c.execute("""create table if not exists arquivos (
                          nome_arquivo text
                          )""")
        self.conexao.commit()
        c.close()

    def inserir_dados(self):
        ff = FileFinder()
        ff.set_list_pdfs()
        arquivos = ff.get_pdfs_names()
        c = self.conexao.cursor()
        for nome_arquivos in arquivos:
            c.execute("""insert into arquivos (nome_arquivo)
                          values (?)""", (nome_arquivos))
            self.conexao.commit()
            c.close()

    def selecionar_dados(self):
        c = self.conexao.cursor()

        c.execute(""" select * from arquivos """)
        for linha in c:
            print(linha)

        c.close()


aa = FileConverter()
bb = FileContent()
bb.read_pdfs()
