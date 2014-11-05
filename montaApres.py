# -*- coding:UTF-8 -*-

"""

Titulo :montaApres.py 

Descrição : Prepara uma página em HTML 5, CSS3 e 
           JQuery para realizar uma apresentação.
           
Resumo : Usando as tags no início da página :
         Simbolo  Significado 
         -------  -----------
         #        Capítulo         <cap>
         -        SubItem (<ul>)   <ite>
         [#       Imagem           <ima> || imagem_dir ou imagem_esq ou imagem_full
         {#       Video            <vid>
         **       Comentários      <com>

Nas primeras linhas do arquivo texti devemo ter :
    linha 1 = titulo
    linha 2 = Subtitulo1 
    linha 3 = Subtitulo2
    linha 4 = autor 
    linha 5 = Empresa

Ver : 5 [12.06.14 - LGFA]


TODO :
    - [bugfix] As linhas ficam desordenadas quando intercaladas com outros tipos 
    - Criar uma instalação total ambiente com os templates( imagens, css, html) no primeiro
    - Alterar o template para utilizar uma área maior da tela
    - Incluir JS para permitir a visualização de imagem em modo full
    - Incluir indice automático a partir das páginas levantadas ( e habilitadas para participar no indice)
    - Integração com uma ferramenta de template (kid, genshi, ...)
    - Incluir nova tag para navegação por Hiperlink relacionado a uma palavra ou texto 
       Ex: <nova_tag> texto texto </fechtag>
    - opção de hide/show para anotações e observações
    - Integração com o Django/Flask/...
    - melhorar a animação da transição dos slides
    - permitir uma navegação diferente com a ajuda dos hyperlinks



"""


"""
Tabela com o codigo de teclas utilizadas no JQuery:
  seta para baixo = 40
  seta para lado direito = 39
  page down = 34
  seta para cima = 38
  seta para lado esquerdo = 37
  page up = 33
  tecla s = 83
  barra de espaco = 32 
  enter = 13
  tecla 1 = 49
  tecla 2 = 50
  tecla 3 = 51
  tecla 4 = 52
  tecla 5 = 53
  esc 27
  home = 36
  end = 35
  tab = 9
"""

import sys
import os
import jinja2

from odf.opendocument import OpenDocumentText
from odf.text import P
from odf.text import H

import os,sys,getopt,struct
from cStringIO import StringIO
from odf.opendocument import OpenDocumentPresentation
from odf.style import Style, MasterPage, PageLayout, PageLayoutProperties, \
TextProperties, GraphicProperties, ParagraphProperties, DrawingPageProperties
from odf.draw  import Page, Frame, TextBox, Image
  
def getImageInfo(data):
    size = len(data)
    height = -1
    width = -1
    w = -1
    h = -1
    content_type = ''
  
    # handle GIFs
    if (size >= 10) and data[:6] in ('GIF87a', 'GIF89a'):
        # Check to see if content_type is correct
        content_type = 'image/gif'
        w, h = struct.unpack("<HH", data[6:10])
        width = int(w)
        height = int(h)
  
    # See PNG v1.2 spec (http://www.cdrom.com/pub/png/spec/)
    # Bytes 0-7 are below, 4-byte chunk length, then 'IHDR'
    # and finally the 4-byte width, height
    elif ((size >= 24) and (data[:8] == '\211PNG\r\n\032\n')
          and (data[12:16] == 'IHDR')):
        content_type = 'image/png'
        w, h = struct.unpack(">LL", data[16:24])
        width = int(w)
        height = int(h)
  
    # Maybe this is for an older PNG version.
    elif (size >= 16) and (data[:8] == '\211PNG\r\n\032\n'):
        # Check to see if we have the right content type
        content_type = 'image/png'
        w, h = struct.unpack(">LL", data[8:16])
        width = int(w)
        height = int(h)
  
    # handle JPEGs
    elif (size >= 2) and (data[:2] == '\377\330'):
        content_type = 'image/jpeg'
        jpeg = StringIO(data)
        jpeg.read(2)
        b = jpeg.read(1)
        try:
            while (b and ord(b) != 0xDA):
                while (ord(b) != 0xFF): b = jpeg.read(1)
                while (ord(b) == 0xFF): b = jpeg.read(1)
                if (ord(b) >= 0xC0 and ord(b) <= 0xC3):
                    jpeg.read(3)
                    h, w = struct.unpack(">HH", jpeg.read(4))
                    break
                else:
                    jpeg.read(int(struct.unpack(">H", jpeg.read(2))[0])-2)
                b = jpeg.read(1)
            width = int(w)
            height = int(h)
        except: pass
  
    return content_type, width, height
 

def install(nomeDir):
    """
    install
    Testa se ambiente já está instalado.
    Em caso negativo, gera um diretório para guardar a apresentação HTML5 
    """
    #nome_dir = raw_input("Entre com o nome da apresentação :")
    if cria_dir(nomeDir):
        return True
    else:
        return False

def cria_dir(nome_dir):
    """
    cria_dir
    cria os diretório da aplicação
    """
    textoPattern = """TituloPag
    Titulo1
    SubTitulo
    Nome
    Empresa
    # Capitulo 1
    bla bla bla
    # Captulo 2 
    bla bla bla
    """

    if os.path.exists("./%s" % nome_dir):
        print "Projeto com nome: %s já  existe" % nome_dir
        return False
    
    os.popen("mkdir %s" % nome_dir).readlines()
    os.popen("touch %s/%s.txt" %  (nome_dir, nome_dir)).readlines()
    os.popen("echo '%s' >> %s/%s.txt" % (textoPattern, nome_dir, nome_dir))
    os.popen("mkdir %s/css" % nome_dir).readlines()
    os.popen("cp -rf /home/01083429728/novo_montaApresHTML5/css %s/" % nome_dir).readlines()
    os.popen("mkdir %s/img" % nome_dir).readlines()
    os.popen("mkdir %s/js" % nome_dir).readlines()
    os.popen("cp -rf /home/01083429728/novo_montaApresHTML5/js %s/" % nome_dir).readlines()
    os.popen("cp -rf /home/01083429728/novo_montaApresHTML5/img %s/" % nome_dir).readlines()
    return True
    
    
def carrega_txt(nomeArq):
    """
    carrega_txt
    
    Carrega arquivo com a aparesentação e devolve um dicionário
    
    """
    listaArq = open(nomeArq, "r").readlines()
    titulo = listaArq[0]
    titulo1 = listaArq[1]
    titulo2 = listaArq[2]
    autor = listaArq[3]
    setor = listaArq[4]

    dicCapa = { "titulo" :  titulo.decode('utf-8'), 
                 "titulo1": titulo1.decode('utf-8'), 
                 "titulo2": titulo2.decode('utf-8'), 
                 "slides" : "",
                 "autor" : autor.decode('utf-8'),
                 "setor" : setor.decode('utf-8'), 
                 "num" : ""}


    dicSlides = {}
    
    listaPaginas = []
    pagina = 1
    num_linha = 0
    for linha in listaArq[5:]:
        linha = linha.strip()
        if len(linha) >= 1 :
            if linha.startswith("#"):
                titulo = linha[1:]
                num_linha = 0
                pagina = pagina + 1
                dicSlides[pagina] = {'titulo': titulo.decode('utf-8'),
                                     'conteudo': {}, 
                                     'coluna' : 'grid_12' }
            else:                
                num_linha = num_linha + 1
                dic_linha = {}
                if linha.startswith("-"):
                    tipo = "ite"
                    valor = linha[1:]
                    estilo = ""
                
                elif linha.startswith("[#"):
                    tipo = "img"
                    dadosImg = linha[2:]
                    valor = dadosImg.split("||")[0]
                    estilo = dadosImg.split("||")[1]
                    if estilo in ['imagem_dir', 'imagem_esq']:
                        dicSlides[pagina]['coluna'] = 'grid_12'
                elif linha.startswith("{#"):
                    tipo = "vid"
                    valor = linha[2:]
                    estilo = ""
                    dicSlides[titulo]["video"] = linha[2:].strip()
                elif linha.startswith("**"):
                    tipo = "com"
                    valor = linha[1:]
                    estilo = ""
                else:
                    tipo = "par"
                    valor = linha
                    estilo = ""

                dic_linha = {"tipo": tipo.decode('utf-8'),
                              "valor": valor.strip().decode('utf-8'),
                              "classe" : estilo.decode('utf-8'),
                              "estilo" : estilo.decode('utf-8'),
                              }
                dicSlides[pagina]['conteudo'][num_linha] = dic_linha
    dicCapa['num'] = pagina + 1
    dicSlides[0] = dicCapa
    #print dicSlides[0]['num']
    #print dicSlides
    return dicSlides
        

def odfRender(dic_slides_odf, nomePrj):
    lista_slides = dic_slides_odf.keys()
    lista_slides.sort()

    
    manualODF = OpenDocumentText()

    outline = {'outlinelevel': 1}
    
    
    
    for x in lista_slides[1:]:
        titulo = dic_slides_odf[x]["titulo"]
        h = H( text=titulo, attributes=outline)
        manualODF.text.addElement(h)
        lista_conteudo = dic_slides_odf[x]['conteudo'].keys()
        lista_conteudo.sort()
        for num in lista_conteudo:
           if dic_slides_odf[x]['conteudo'][num]['tipo'] == 'par':
               texto_capitulo = dic_slides_odf[x]['conteudo'][num]['valor'] 

           if dic_slides_odf[x]['conteudo'][num]['tipo'] == 'ite':
               texto_capitulo = "     - " + dic_slides_odf[x]['conteudo'][num]['valor'] 

           if dic_slides_odf[x]['conteudo'][num]['tipo'] == 'img':
               texto_capitulo = "Figura: " + dic_slides_odf[x]['conteudo'][num]['valor'] 

           p = P(text=texto_capitulo)

           manualODF.text.addElement(p)


    manualODF.save("%s/%s" % (nomePrj,nomePrj),  True)


    return "ok"


def odpRender(dic_slides_odp, nomePrj):
    lista_slides = dic_slides_odp.keys()
    lista_slides.sort()
    
    manualODP = OpenDocumentPresentation()

    # We must describe the dimensions of the page
    pagelayout = PageLayout(name="MyLayout")
    manualODP.automaticstyles.addElement(pagelayout)
    pagelayout.addElement(PageLayoutProperties(margin="0pt", pagewidth="800pt",
        pageheight="600pt", printorientation="landscape"))
  
    # Style for the title frame of the page
    # We set a centered 34pt font with yellowish background
    titlestyle = Style(name="MyMaster-title", family="presentation")
    titlestyle.addElement(ParagraphProperties(textalign="center"))
    titlestyle.addElement(TextProperties(fontsize="42pt"))
    titlestyle.addElement(GraphicProperties(fillcolor="#ffffff", stroke="none"))
    manualODP.styles.addElement(titlestyle)

    # Style for the text frame of the page
    textostyle = Style(name="standard", family="graphic")
    textostyle.addElement(ParagraphProperties(textalign="left"))
    textostyle.addElement(TextProperties(attributes={"fontsize":"24pt" }))
    textostyle.addElement(GraphicProperties(fillcolor="#ffffff", stroke="none"))
    manualODP.styles.addElement(textostyle)

    # Style for the photo frame
    photostyle = Style(name="MyMaster-photo", family="presentation")
    manualODP.styles.addElement(photostyle)
  
    # Create automatic transition
    dpstyle = Style(name="dp1", family="drawing-page")
    dpstyle.addElement(DrawingPageProperties(transitiontype="automatic",
       transitionstyle="move-from-top", duration="PT2S"))
    manualODP.automaticstyles.addElement(dpstyle)
  
    # Every drawing page must have a master page assigned to it.
    masterpage = MasterPage(name="MyMaster", pagelayoutname=pagelayout)
    manualODP.masterstyles.addElement(masterpage)

    pict_dir = "./%s/img" % nomePrj
    altura_h = 540
    largura_w = 720
    base_X = 40
    base_Y = 70
    corr_Y = 60
 
    for x in lista_slides[1:]:
        titulo = dic_slides_odp[x]["titulo"]
        lista_conteudo = dic_slides_odp[x]['conteudo'].keys()
        lista_conteudo.sort()
        page = Page(stylename=dpstyle, masterpagename=masterpage)
        manualODP.presentation.addElement(page)

        titleframe = Frame(stylename=titlestyle, width="720pt", height="80pt", x="40pt", y="10pt")
        page.addElement(titleframe)
        textbox = TextBox()
        titleframe.addElement(textbox)
        textbox.addElement(P(text=titulo))

        
        w = largura_w
        h = altura_h - base_Y  
        offsetx = base_X
        offsety = base_Y 
        espacamento_lin = 20

        for num in lista_conteudo:
           if dic_slides_odp[x]['conteudo'][num]['tipo'] == 'par':
               if w == 355:
                   offsety =  offsety + espacamento_lin


               texto_capitulo = dic_slides_odp[x]['conteudo'][num]['valor']
               textoSlide = Frame(stylename=textostyle, width="%fpt" % w, height="%fpt" % h , x="%fpt" % offsetx,   y="%fpt" % offsety)
               page.addElement(textoSlide)
               textbox = TextBox()
               textoSlide.addElement(textbox)
               textbox.addElement(P(text=texto_capitulo))

               offsety = base_Y + offsety

           if dic_slides_odp[x]['conteudo'][num]['tipo'] == 'ite':
               texto_capitulo = "  - " + dic_slides_odp[x]['conteudo'][num]['valor']
               if w == 355:
                   offsety =  offsety + espacamento_lin

               textoSlide = Frame(stylename=textostyle, width="%fpt" % w, height="%fpt" % h, x="%fpt" % offsetx, y="%fpt" % offsety)
               page.addElement(textoSlide)
               textbox = TextBox()
               textoSlide.addElement(textbox)
               textbox.addElement(P(text=texto_capitulo))
               offsety = base_Y + offsety

           if dic_slides_odp[x]['conteudo'][num]['tipo'] == 'img':
               picture = dic_slides_odp[x]['conteudo'][num]['valor'] 
               estilo_picture = dic_slides_odp[x]['conteudo'][num]['estilo'] 
               pictdata = open(pict_dir+'/'+picture).read()
               ct,w,h = getImageInfo(pictdata) # Get dimensions in pixels
               offsetx = base_X
               w = largura_w
               h = altura_h - offsety 
               if estilo_picture == 'imagem_dir':
                   offsetx = 400
                   w = 355
               if estilo_picture == 'imagem_esq':
                   offsetx = 40
                   w = 355

               if estilo_picture == 'imagem_base':
                   offsety = offsety + 10


               photoframe = Frame(stylename=photostyle, width="%fpt" % w, height="%fpt" % h, x="%fpt" % offsetx, y="%fpt" % offsety)
               page.addElement(photoframe)
               href = manualODP.addPicture(pict_dir + "/" + picture)
               photoframe.addElement(Image(href=href))
               # corrige para posicionar o texto que existe na página
               # observando se imagem_full ou não
               if estilo_picture <> 'imagem_base':
                   if offsetx == 40 :
                       offsetx = 400
                   else:
                       offsetx = 40
               offsety = base_Y + offsety

    manualODP.save("%s/t%s" % (nomePrj,nomePrj),  True)





    return

def update(nomePrj):
    """
    update 
    Atualiza a apresentação
    """
    # Carrega arquivo txt
    
    #
    
    JINJA_ENV = jinja2.Environment(loader=jinja2.FileSystemLoader('./templates'))
    template = JINJA_ENV.get_template('slides.html')
    nomeArq = "%s/%s.txt" % (nomePrj, nomePrj)
    nomeHTML = "%s/%s.html" % (nomePrj, nomePrj)
    dic_slides = carrega_txt(nomeArq)
    odpRender(dic_slides, nomePrj)
    #html = template.render(dic_slides = dic_slides)
    #print html
    #arq = open(nomeHTML, "w")
    #arq.write(html.encode('utf-8'))
    return "ok"




if __name__ == "__main__" :
    usage =  """ 
    ##############################################################
           
           montaApresHTML - Versão 5.0 [12/06/03]
           Usage: 
                python montaApresHTML.py <comando> <nomeApres>
           - comando pode ser :
              install
              update
           - nomeApres é o nome do projeto a ser processado.

           
    ##############################################################
           """
    if len(sys.argv) <= 2 or sys.argv[1] == '--help' :
        #or sys.argv[2][-4:] != '.txt' :
        print usage 
        exit()
    else:
        nomeApres = sys.argv[2]
        #nomeSaida = nomeArqIn + ".html"
        #nomePDF = nomeArqIn + ".pdf"
        #nomeSaida = nomeArqIn.replace(".txt", ".html")
        #nomePDF = nomeArqIn.replace(".txt", ".pdf")
    
    if "install" in sys.argv:
        if install(nomeApres):
            update(nomeApres)
    if "update" in sys.argv:
        update(nomeApres)
        
    """
    lista_show = carrega_txt(nomeArqIn)
    
    print lista_show[0]
    for elem in lista_show:
        if elem <> 0:
            print elem
            print lista_show[elem]['titulo']
            for ll in lista_show[elem]['conteudo']:
                print lista_show[elem]['conteudo'][ll]
    """        




    #print "HTML %s Atualizado" % nomeApres

    #pdfConv = os.popen("wkhtmltopdf -s a4 -O Landscape %s/%s.html %s/%s.pdf" % (nomeApres, nomeApres))


