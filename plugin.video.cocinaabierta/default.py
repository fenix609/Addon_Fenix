# -*- coding: utf-8 -*-
#------------------------------------------------------------
# Plugin Parser de la sección de Cocina de la web HogarMania.com  by Bad-Max
# Version 0.0.1 (16-12-2021)
#------------------------------------------------------------
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
# Gracias a la librería plugintools de Jesús (www.mimediacenter.info), PlatformCode y Core del Grupo Balandro (https://linktr.ee/balandro)

import os, sys, urllib, re, shutil, zipfile, base64
import xbmc, xbmcgui, xbmcaddon, xbmcplugin, requests
import locale, time, random, plugintools
import resolvers

if sys.version_info[0] < 3:
    import urllib2
else:
    import urllib.error as urllib2

from core import httptools
from core.item import Item
from platformcode.config import WebErrorException


addonName           = xbmcaddon.Addon().getAddonInfo("name")
addonVersion        = xbmcaddon.Addon().getAddonInfo("version")
addonId             = xbmcaddon.Addon().getAddonInfo("id")
addonPath           = xbmcaddon.Addon().getAddonInfo("path")

version="(v0.0.2)"

osAndroid = xbmc.getCondVisibility('system.platform.android')

addonPath           = xbmcaddon.Addon().getAddonInfo("path")
mi_data = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/plugin.video.cocinaabierta/'))
mi_addon = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.cocinaabierta'))

launcher = xbmc.translatePath(os.path.join('special://home/addons/plugin.program.browser.launcher/'))

fondo = xbmc.translatePath(os.path.join(mi_addon,'fanart.jpg'))
logo1 = xbmc.translatePath(os.path.join(mi_addon,'icon.png'))

mislogos = xbmc.translatePath(os.path.join('special://home/addons/plugin.video.cocinaabierta/jpg/'))
logobusca = xbmc.translatePath(os.path.join(mislogos , 'buscar.jpg'))
logo_volver = xbmc.translatePath(os.path.join(mislogos , 'volver.png'))
logo_siguiente = xbmc.translatePath(os.path.join(mislogos , 'siguiente.png'))
logo_finpag = xbmc.translatePath(os.path.join(mislogos , 'final.png'))
logo_salida = xbmc.translatePath(os.path.join(mislogos , 'salida.png'))
logo_transparente = xbmc.translatePath(os.path.join(mislogos , 'transparente.png'))

setting = xbmcaddon.Addon().getSetting
if setting('youtube_usar') == "0":  ##Tiene escogido el plugin Youtube
    usa_duffyou = False
else:  ##Ha escogido usar Duff You
    usa_duffyou = True
    
ver_web_despues = False
if setting('ver_web_despues') == "true":
    ver_web_despues = True

web = "https://www.hogarmania.com"
pag_categoria = "https://www.hogarmania.com/cocina/recetas"
carnes = "https://www.hogarmania.com/cocina/recetas/carnes/"
carnes2 = "https://www.hogarmania.com/cocina/recetas/carnes/pagina/2"
postres = "https://www.hogarmania.com/cocina/recetas/postres/"
verduras = "https://www.hogarmania.com/cocina/recetas/ensaladas-verduras/"
pescados = "https://www.hogarmania.com/cocina/recetas/pescados-mariscos/"
pastas = "https://www.hogarmania.com/cocina/recetas/pastas-pizzas/"
legumbres = "https://www.hogarmania.com/cocina/recetas/legumbres/"
sopas = "https://www.hogarmania.com/cocina/recetas/sopas-cremas/"
arroces = "https://www.hogarmania.com/cocina/recetas/arroces-cereales/"
aperitivos = "https://www.hogarmania.com/cocina/recetas/aperitivos/"
salsas = "https://www.hogarmania.com/cocina/recetas/salsas/"
huevos = "https://www.hogarmania.com/cocina/recetas/huevos/"
setas = "https://www.hogarmania.com/cocina/recetas/setas-hongos/"
cocteles = "https://www.hogarmania.com/cocina/recetas/cocteles/"
panes = "https://www.hogarmania.com/cocina/recetas/recetas-pan/"

atresmedia = "https://ovpapi.atresmedia.com/ovpcms/v1/public/video/player/MI-ID-VIDEO?live=false&categoryId=&themeId="
youtube = "plugin://plugin.video.youtube/play/?video_id=MI-ID-VIDEO"
duffyou = "eydhY3Rpb24nOiAncGxheScsICdhdXRob3JfaWQnOiAnJywgJ2F1dGhvcl9uYW1lJzogJycsICdkdXJhdGlvbic6IDAsICdmYW5hcnQnOiAnJywgJ2ljb24nOiAnJywgJ2lkJzogJ01JLUlELVZJREVPJywgJ2lzUGxheWFibGUnOiBUcnVlLCAnbGFiZWwnOiAnJywgJ3BhZ2UnOiAxLCAncGxvdCc6ICcnLCAndGh1bWInOiAnJywgJ3RpcG8nOiAndmlkZW8nLCAndXJsJzogJyd9"

LanzaWeb = False	
#if xbmc.getCondVisibility('System.HasAddon("plugin.program.browser.launcher")'):  ##Si está instalado Browser Launcher (Lanzador web)
if os.path.exists(launcher):  ##Si está instalado Browser Launcher (Lanzador web)
    LanzaWeb = True
if osAndroid:  ## Si estamos en Android, le pongo el modo de visualizacion en "Kiosko"
    lanzador = "plugin://plugin.program.browser.launcher/?url=MI-URL-RECETA&mode=showSite&stopPlayback=yes&kiosk=yes&custBrowser=2&userAgent="
else:
    lanzador = "plugin://plugin.program.browser.launcher/?url=MI-URL-RECETA&mode=showSite&stopPlayback=yes&kiosk=no&custBrowser=2&userAgent="

ipostres = xbmc.translatePath(os.path.join(mislogos , 'postres.jpg'))
icarnes = xbmc.translatePath(os.path.join(mislogos , 'carnes.jpg'))
iverduras = xbmc.translatePath(os.path.join(mislogos , 'verduras.jpg'))
ipescados = xbmc.translatePath(os.path.join(mislogos , 'pescados.jpg'))
ipastas = xbmc.translatePath(os.path.join(mislogos , 'pastas.jpg'))
ilegumbres = xbmc.translatePath(os.path.join(mislogos , 'legumbres.jpg'))
isopas = xbmc.translatePath(os.path.join(mislogos , 'sopas.jpg'))
iarroces = xbmc.translatePath(os.path.join(mislogos , 'arroces.jpg'))
iaperitivos = xbmc.translatePath(os.path.join(mislogos , 'aperitivos.jpg'))
isalsas = xbmc.translatePath(os.path.join(mislogos , 'salsas.jpg'))
ihuevos = xbmc.translatePath(os.path.join(mislogos , 'huevos.jpg'))
isetas = xbmc.translatePath(os.path.join(mislogos , 'setas.jpg'))
icocteles = xbmc.translatePath(os.path.join(mislogos , 'cocteles.jpg'))
ipanes = xbmc.translatePath(os.path.join(mislogos , 'panes.jpg'))

if not os.path.exists(mi_data):
	os.makedirs(mi_data)  # Si no existe el directorio, lo creo

vistos = xbmc.translatePath(os.path.join('special://home/userdata/addon_data/plugin.video.cocinaabierta/vistos.db'))
if not os.path.exists(vistos):
    crear=open(vistos, "w+")
    crear.close()

cabecera = "[COLOR blue][B]              CocinaAbierta  "+version+" [COLOR red]        ····[COLOR yellow]by Bad-Max[COLOR red]····[/B][/COLOR]"


# Punto de Entrada
def run():
	plugintools.log('[%s %s] Running %s... ' % (addonName, addonVersion, addonName))

	# Obteniendo parámetros...
	params = plugintools.get_params()
    
	
	if params.get("action") is None:
		main_list(params)
	else:
		action = params.get("action")
		#exec action+"(params)" #kodi 18
		exec(action+"(params)") #kodi 19
        

	plugintools.close_item_list()            



# Principal
def main_list(params):

    xbmcplugin.setContent( int(sys.argv[1]) ,"tvshows" )
    
    #Cabecera
    plugintools.add_item(action="",url="",title=cabecera,thumbnail=logo1,fanart=fondo,folder=False,isPlayable=False)
    plugintools.add_item(action="",url="",title="",thumbnail=logo_transparente, fanart=fondo, folder=False, isPlayable=False)
    
    ##Categorias
    plugintools.add_item(action="abre_categoria",url=carnes,title='[COLOR white]Carnes[/COLOR]' ,thumbnail=icarnes, fanart=fondo, folder=True, isPlayable=False)
    plugintools.add_item(action="abre_categoria",url=pescados,title='[COLOR white]Pescados y Mariscos[/COLOR]' ,thumbnail=ipescados, fanart=fondo, folder=True, isPlayable=False)
    plugintools.add_item(action="abre_categoria",url=verduras,title='[COLOR white]Verduras y Ensaladas[/COLOR]' ,thumbnail=iverduras, fanart=fondo, folder=True, isPlayable=False)
    plugintools.add_item(action="abre_categoria",url=legumbres,title='[COLOR white]Legumbres[/COLOR]' ,thumbnail=ilegumbres, fanart=fondo, folder=True, isPlayable=False)
    plugintools.add_item(action="abre_categoria",url=pastas,title='[COLOR white]Pastas y Pizzas[/COLOR]' ,thumbnail=ipastas, fanart=fondo, folder=True, isPlayable=False)
    plugintools.add_item(action="abre_categoria",url=sopas,title='[COLOR white]Sopas y Cremas[/COLOR]' ,thumbnail=isopas, fanart=fondo, folder=True, isPlayable=False)
    plugintools.add_item(action="abre_categoria",url=arroces,title='[COLOR white]Arroces y Cereales[/COLOR]' ,thumbnail=iarroces, fanart=fondo, folder=True, isPlayable=False)
    plugintools.add_item(action="abre_categoria",url=aperitivos,title='[COLOR white]Aperitivos[/COLOR]' ,thumbnail=iaperitivos, fanart=fondo, folder=True, isPlayable=False)
    plugintools.add_item(action="abre_categoria",url=salsas,title='[COLOR white]Salsas[/COLOR]' ,thumbnail=isalsas, fanart=fondo, folder=True, isPlayable=False)
    plugintools.add_item(action="abre_categoria",url=huevos,title='[COLOR white]Huevos[/COLOR]' ,thumbnail=ihuevos, fanart=fondo, folder=True, isPlayable=False)
    plugintools.add_item(action="abre_categoria",url=setas,title='[COLOR white]Setas y Hongos[/COLOR]' ,thumbnail=isetas, fanart=fondo, folder=True, isPlayable=False)
    plugintools.add_item(action="abre_categoria",url=postres,title='[COLOR white]Postres[/COLOR]' ,thumbnail=ipostres, fanart=fondo, folder=True, isPlayable=False)
    plugintools.add_item(action="abre_categoria",url=panes,title='[COLOR white]Recetas de Pan[/COLOR]' ,thumbnail=ipanes, fanart=fondo, folder=True, isPlayable=False)
    plugintools.add_item(action="abre_categoria",url=cocteles,title='[COLOR white]Cócteles[/COLOR]' ,thumbnail=icocteles, fanart=fondo, folder=True, isPlayable=False)
    datamovie = {}
    datamovie["Plot"]="Buscar Recetas por palabras clave."
    plugintools.add_item(action="abre_categoria",url="",title="[COLOR blue]Búsqueda[/COLOR]",extra="busca", thumbnail=logobusca, fanart=fondo, info_labels = datamovie, folder=True, isPlayable=False)

    datamovie = {}
    datamovie["Plot"]="Salir de CocinaAbierta..."
    plugintools.add_item(action="salida",url="",title="[COLOR red]Salir[/COLOR]",thumbnail=logo_salida,extra="", fanart="https://i.imgur.com/Cp1t1lb.png", info_labels = datamovie, folder=False, isPlayable=False)


def abre_categoria(params):
    url = params.get("url")
    titu = params.get("title")
    logo = params.get("thumbnail")
    extra = params.get("extra")
    page = params.get("page")
    
    xbmcplugin.setContent( int(sys.argv[1]) ,"tvshows" )
    
    if extra == "busca":
        busqueda = plugintools.keyboard_input('', 'Introduzca [COLOR red]Texto[/COLOR] a Buscar.')
        if len(busqueda) == 0:
            xbmc.executebuiltin('ActivateWindow(10000,return)')  ##Vuelvo al menú ppal.
            
        titu = "          [B][COLOR blue]·····  BÚSQUEDA:[/COLOR]  " + busqueda + "  [COLOR blue]·····[/COLOR][/B]"
        #https://www.hogarmania.com/cocina/buscador.html?q=pure%20de%20patata&id_autor=&secciones=193
        url = "https://www.hogarmania.com/cocina/buscador.html?q=" + busqueda.replace(" ", "%20") + "&id_autor=&secciones=193"
        extra = "TITU_ORIGEN:" + titu + "LOGO_ORIGEN:" + logo + "<Fin"
        page = "busca"
        
    elif len(extra) != 0: ## Si trae texto y no es "busca" es q viene de llamada recursiva por paginación
        #Entraigo Titulo y logo de 1ª página
        titu = plugintools.find_single_match(extra,'TITU_ORIGEN:(.*?)LOGO_')
        logo = plugintools.find_single_match(extra,'LOGO_ORIGEN:(.*?)<Fin')
        #plugintools.log("*****************Titu: "+titu+"********************")
        
    else:  ##Es 1ª página... guardo en extra el titulo y logo del grupo por si hay mas de una página
        titu = "           [B]" + titu.upper().replace("[COLOR WHITE]" , "[COLOR darkorange]·····  ").replace("[/COLOR]" , "  ·····[/COLOR]") + "[/B]"
        
        #Meto en extra el titulo y el logo por si viene de vuelta en llamada de paginación
        extra = "TITU_ORIGEN:" + titu + "LOGO_ORIGEN:" + logo + "<Fin"
    
    
    if not "https://" in url: ##Viene de paginación, que no incluye la ruta completa
        url = web + url

    pagina = ""
    pagina = httptools.downloadpage(url).data
    #headers = {"User-Agent": 'Mozilla/5.0 (Windows NT 10.0); AppleWebKit/537.36; (KHTML, like Gecko); Chrome/93.0.4577.60; Safari/537.36', "Referer": web, "cookie": "beget=begetok"}
    #pagina = httptools.downloadpage(url , headers = headers).data
    
    acotacion = 'div class="especial listado'
    seccion = plugintools.find_single_match(pagina,acotacion+'(.*?)</section>') #Primero acoto la sección
    acotacion = '<article class="modulo'
    videos = plugintools.find_multiple_matches(seccion,acotacion+'(.*?)</h2') #Cojo cada video
    #Cabecera
    plugintools.add_item(action="",url="",title=titu,thumbnail=logo,fanart=fondo,folder=False,isPlayable=False)
    plugintools.add_item(action="",url="",title="",thumbnail=logo_transparente, fanart=fondo, folder=False, isPlayable=False)

    #Pongo todos los videos de la página... Ojo, como la receta puede ser video de a3media o de youtube... o NO TENER Video, he de abrir cada página y obtener los datos previamente
    for item in videos:
        url_vid = web + plugintools.find_single_match(item,'href="(.*?)"').strip()
        data = ""
        data = httptools.downloadpage(url_vid).data
        acotacion = 'VideoObject"'
        info_vid = plugintools.find_single_match(data,acotacion+'(.*?)"uploadDate')
        
        if len(info_vid) == 0:  ##Si está vacio, es receta sin Video, así que la preparo para Lanzar con el Chrome
            titulo0 = plugintools.find_single_match(data,'<title(.*?)/title').replace(': "' , '').replace(':"' , '').strip().title()
            if " -" in titulo0:
                acotacion = " -"
            else:
                acotacion = '<'
            titulo = plugintools.find_single_match(titulo0,'>(.*?)'+acotacion).strip().title()
            acotacion = 'description" content='
            descrip = plugintools.find_single_match(data,acotacion+'(.*?)/>').replace('"' , '').strip()
            acotacion = 'thumbnail" content='
            logo = plugintools.find_single_match(data,acotacion+'(.*?)/>').replace('"' , '').strip()
            servidor = "    [COLOR mediumseagreen] (Navegador Web)[/COLOR]"
            guion = "[COLOR mediumseagreen]¤ [/COLOR]"
            
            if LanzaWeb:  ##Si está instalado Browser Launcher (Lanzador web)
                accion = "lanza"
                lanzaME = lanzador.replace("MI-URL-RECETA" , url_vid)
                mivideo = lanzaME
            else:
                accion = "mensaje_web"
                mivideo = ""
                
        else:  ## Tiene video, por lo que obtengo lo que me interesa.
            if " -" in info_vid:
                acotacion = " -"
            else:
                acotacion = '",'
            titulo = plugintools.find_single_match(info_vid,'name"(.*?)'+acotacion).replace(': "' , '').replace(':"' , '').strip().title()
            descrip = plugintools.find_single_match(info_vid,'description"(.*?)",').replace(': "' , '').replace(':"' , '').strip()
            logo = plugintools.find_single_match(info_vid,'thumbnailUrl"(.*?)",').replace(': "' , '').replace(':"' , '')
            vid_url = plugintools.find_single_match(info_vid,'contentUrl"(.*?)",').replace(': "' , '').replace(':"' , '').strip()
            if "atresmedia" in vid_url:
                guion = "[COLOR orange]¤ [/COLOR]"
                servidor = "    [COLOR orange] (a3media)[/COLOR]"
                id_vid = plugintools.find_single_match(vid_url,'videoId=(.*?)&')  ## Solo el id, para montarlo como me hace falta
                la_url = atresmedia.replace("MI-ID-VIDEO" , id_vid)
                #ahora leo esa página y extraigo el m3u8 a reproducir
                data = ""
                data = httptools.downloadpage(la_url).data
                acotacion = 'url" : "'
                mivideo = plugintools.find_single_match(data,acotacion+'(.*?)",')  ##https://vod-hogarmania.atresmedia.com/hls/cocinatis/videos/videos01/published/2019/01/04/D349EFEC-FB44-4B70-B17E-07E92E4EDE11/video_,4K,QHD,FHD,HD,FSD,SD,LD,.mp4.urlset/master.m3u8
            elif "youtube" in vid_url:
                guion = "[COLOR red]¤ [/COLOR]"
                servidor = "    [COLOR red] (Youtube)[/COLOR]"
                vid_url = vid_url + '"'
                id_vid = plugintools.find_single_match(vid_url,'embed/(.*?)"')  ## Solo el id, para montarlo como me hace falta
                if usa_duffyou:  ##Usamos plugin Duff You
                    reemplaza = base64.b64decode(duffyou.encode('utf-8')).decode('utf-8').replace("MI-ID-VIDEO" , id_vid)
                    mivideo = "plugin://plugin.video.duffyou/?" + base64.b64encode(reemplaza.encode('utf-8')).decode('utf-8')
                else:  ##Usamos pluin YouTube
                    mivideo = youtube.replace("MI-ID-VIDEO" , id_vid)  ##plugin://plugin.video.youtube/play/?video_id=16rE9HoGT7g
                
            accion = "lanza"    

        titu = guion + '[COLOR white]' + titulo + '[/COLOR]' + servidor
        datamovie = {}
        datamovie["Plot"] = descrip
        plugintools.log("*****************Accion: "+accion+"   La Url: "+url_vid+"********************")
        el_extra = "Titulo="+titulo+"LaWeb="+url_vid+"<<"
        plugintools.add_item(action=accion, url=mivideo, title=titu, extra=el_extra, page=page, genre="NOGESTIONAR", thumbnail=logo, fanart=fondo, info_labels = datamovie, folder=False, isPlayable=False)
      
    #Busco la paginación
    acotacion = 'class="pagination-box'
    bloque2 = plugintools.find_multiple_matches(pagina,acotacion+'(.*?)/ul>')  ## Va a coger 2 resultados... el que me interesa es el segundo

    if len(bloque2) != 0:  ##Si es diferente de 0, hay mas de 1 página... si no, no busco paginación pues no la hay
        #Acoto cada linea
        bloque1 = bloque2[1]  ##Es el 2º
        acotacion = "<li"
        bloquepag = plugintools.find_multiple_matches(bloque1,acotacion+'(.*?)</li')
        
        #La página actual está en la linea con la clase=active y la siguiente página está en la última línea siempre
        acota1 = 'active"><a href="'
        pagactiva1 = plugintools.find_single_match(bloque1,acota1+'(.*?)>')  ## /cocina/recetas/salsas/pagina/1 , /cocina/recetas/salsas/pagina/2 , etc
        bloquesig = bloquepag[-1]  ##El último, q me da la página siguiente
        acota1 = 'href="'
        pagsig1 = plugintools.find_single_match(bloquesig,acota1+'(.*?)>')  ## /cocina/recetas/salsas/pagina/1 , /cocina/recetas/salsas/pagina/2 , etc
                
        ##Ahora saco los NUMEROS de las 2 páginas de sus links
        if page == "busca":  ##Si tiene paginación en una búsqueda, la acotación es diferente.
            acota1 = "&pagina="
        else:
            acota1 = '/pagina/'
            
        pagactiva = plugintools.find_single_match(pagactiva1,acota1+'(.*?)"')  ## 1, 2, 3, etc
        pagsig = plugintools.find_single_match(pagsig1,acota1+'(.*?)"')  ## 2, 3, 4, etc
        
        if pagactiva == pagsig: #Estoy en la última y no doy opción de avanzar página
            texto = "[COLOR mediumaquamarine]Pág: " + pagactiva + " de " + pagsig + "[/COLOR]"
            accion = ""
            url_siguiente = ""
            el_logo = logo_finpag
            plugintools.add_item(action=accion, url=url_siguiente, title=texto, extra=extra, page=page ,thumbnail=el_logo, fanart=fondo, folder=False, isPlayable=False)
        else:
            texto = "[COLOR mediumaquamarine]Pág: " + pagactiva + "[COLOR lime]                  Ir a Siguiente >>>[/COLOR]"
            accion = "abre_categoria" ##Recursividad
            #Como no es la última, paso la url de la siguiente página (que siempre está en la última línea, la -1 en la tabla)
            url_siguiente = pagsig1.replace('"' , '')
            el_logo = logo_siguiente
            plugintools.add_item(action=accion, url=url_siguiente, title=texto, extra=extra, page=page ,thumbnail=el_logo, fanart=fondo, folder=True, isPlayable=False)
        
        
        plugintools.add_item(action="miDefault", url="", title="[COLOR orangered]···· Volver a Menú Principal ····[/COLOR]", extra=extra ,thumbnail=logo_volver, fanart=fondo, folder=True, isPlayable=False)
    
    


def lanza(params):
    url = params.get("url")
    logo = params.get("thumbnail")
    titu = params.get("title")
    titulo2 = params.get("extra")
    
    titulo = plugintools.find_single_match(titulo2,'Titulo=(.*?)LaWeb=')
    pag_web = plugintools.find_single_match(titulo2,'LaWeb=(.*?)<<')
    
    if "plugin://" in url:  ## Es para lanzar con el addon YouTube/Duff-You o browser.launcher
        xbmc.Player().play(url)
    else:
        li = xbmcgui.ListItem(titulo)
        li.setInfo(type='Video', infoLabels="")
        li.setArt({ 'thumb': logo})

        xbmc.Player().play(url,li)

    import time
    time.sleep(10)  # Para darle tiempo a q el .isPlaying pueda detectar que está reproduciendo
    while xbmc.Player().isPlaying():
        time.sleep(1)
    
    if LanzaWeb and ver_web_despues:  ##Si está instalado Browser Launcher (Lanzador web) y quiere que pregunten
        if  not "plugin.program.browser" in url:  #Si viene del browser no tiene sentido preguntar si desea abrirlo de nuevo
            abre_web  = xbmcgui.Dialog().yesno("Abrir la Página", "¿Desea abrir la página web de la Receta para poder ver los ingredientes y explicación detallada?" )
            if abre_web:
                lanzaME = lanzador.replace("MI-URL-RECETA" , pag_web)
                xbmc.Player().play(lanzaME)



def mensaje_web(params):
    url = params.get("url")

    lin1 = "[COLOR blue]Esta receta no contiene Video, solo la explicación e Imágenes que podemos verlos en la Web.[/COLOR]"+"\n"
    lin2 = "[COLOR blue]Para poder visualizar este enlace es necesario tener instalado el Addon:[/COLOR]"+"\n"
    lin3 = "[COLOR orange]plugin.program.browser.launcher   [COLOR blue]que pertenece a Sandmann79"+"[/COLOR] Versión v.2.0.0-Mod\n"
    lin4 = "[COLOR blue]Y tener instalado en su equipo el Navegador Web [COLOR green]Google Chrome.[/COLOR]"
    xbmcgui.Dialog().ok( "[COLOR lime]No Se Pudo Abrir[/COLOR]" , lin1+lin2+lin3+lin4  )


def salida(params):

	xbmc.executebuiltin('ActivateWindow(10000,return)')
	



	

run()

