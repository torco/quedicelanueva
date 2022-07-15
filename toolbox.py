import cherrypy, os, pathlib, sqlite3, pandas as pd, re

dir_path = str(pathlib.Path(__file__).parent.resolve())
os.chdir(dir_path)


def consultar(consu):
    text = open('CONVENCION.txt','r', encoding='utf-8').read()
    text = text.replace('Artículo ','%art%').replace('  ',' ')
    text2 = re.sub(r'(CAPÍTULO.*?\d\n)','',text)
    text3 = re.sub(r'(\d* CONSTITUCIÓN POLÍTICA DE LA REPÚBLICA.*?\d*)','',text2)
    text4 = re.sub(r'(CAPÍTUL.*?\d*1\.)','',text3)
    text5 = text4.replace('\n', '')
    articulos = text4.split('%art%')
    li=[]

    for each in articulos:
        x = each.split(' ',1)
        li.append([x[0],x[1]])

    df_articulos=pd.DataFrame(data=li,columns=['num articulo','cuerpo'])
    for index, row in df_articulos.iterrows():
        body = row[1]
        body2 = re.split(r'\d. ', body)
        df_articulos.at[index,'artlist']=body2
        
    for index, articulo in df_articulos.iterrows():
        x = articulo['cuerpo'].lower().count(consu.lower())
        x = x / len(articulo['cuerpo'])
        df_articulos.at[index,'score']=x
    
    response = df_articulos.sort_values(by=['score'], ascending=False)
    response = response.loc[response['score']>0]
    reponse = response.drop_duplicates
    return response

def format_response(response, consu):
    html = ''
    html2 = ''
    for index, each in response.iterrows():
        html += '<h4>Artículo {}</h4>'.format(each['num articulo'])
        html += '<p>'+each['cuerpo']+'</p>'
    for each in html:
        #print(each,ord(each))
        if ord(each) == 10:
            html2+='<br>'
        else:
            html2+=each
    if html2=='': 
        html2 = 'SIN RESULTADOS, esa palabra no aparece en la NC'
    #return response
    consu = consu.lower()
    return html2.replace(consu,'<mark>'+consu+'</mark>')
    return html2

z = consultar('Derechos')
zz = format_response(z, 'derechos')

