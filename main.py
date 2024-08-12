import streamlit as sl,sqlite3,base64,os,webbrowser,subprocess
from streamlit_option_menu import option_menu
from st_clickable_images import clickable_images
db=sqlite3.connect('db.db')
db.execute('create table if not exists ARTICULOS(CATEGORIA,NOMBRE,INFO,PRECIO)')
categorias=[categoria[0] for categoria in db.execute('select CATEGORIA from ARTICULOS group by CATEGORIA').fetchall()]
db.close()
contactos = []
sl.set_page_config(page_title='Shambala, Cruz del Sur',page_icon='logo.png')
with open('bg.jpg','rb') as f:bg=base64.b64encode(f.read()).decode()
sl.markdown('<style> [data-testid=stAppViewContainer] {background-image:url("data:image/jpg;base64,%s");background-size:cover;} </style>' % bg,unsafe_allow_html=True)
with sl.container(height=500,border=False):
    col1,col2=sl.columns(2)
    col1.image('logo.png')
    with col2:
        for file in os.listdir('contactos'):
            with open('contactos/' + file, 'rb') as imagen:
                encoded = base64.b64encode(imagen.read()).decode()
                contactos.append(f'data:image/png;base64,{encoded}')
        contacto = clickable_images(contactos, img_style={'height': '100px'})
        if contacto == 0:webbrowser.open_new_tab('https://www.facebook.com/cruzdelsurshambala/?locale=es_ES')
        elif contacto==1:subprocess.run('pbcopy', text=True, input='+34963552732')
        elif contacto == 2:webbrowser.open_new_tab('https://www.instagram.com/cruzdelsurshambala/?hl=es')
        elif contacto == 3:webbrowser.open_new_tab('https://wa.me/34658828285')
    sl.markdown(':orange[Shambala, Cruz del Sur - desde 1995, Cervezas, Arte y Cultura]')
with sl.sidebar:
    sl.header('La carta')
    categoria=option_menu(menu_title='La Carta',options=categorias)
if categoria:
    sl.title(categoria)
    db=sqlite3.connect('db.db')
    for articulo in db.execute('select * from ARTICULOS where CATEGORIA=?',(categoria,)).fetchall():
        with sl.container(height=300,border=True):
            col1,col2,col3=sl.columns(3)
            col1.write(articulo[1])
            try:col1.image('imagenes/'+categoria+'/'+articulo[1]+'.png')
            except:pass
            col2.write('')
            col2.write(articulo[2])
            col3.write('')
            col3.write('€ '+str(articulo[3]))
    db.close()