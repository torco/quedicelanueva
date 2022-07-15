import cherrypy, os, pathlib, sqlite3, pandas as pd, re

cherrypy.config.update({'server.socket_port': 8001})
cherrypy.config.update({'tools.sessions.on': True})

dir_path = str(pathlib.Path(__file__).parent.resolve())
os.chdir(dir_path)

from toolbox import consultar, format_response

class App(object):
    @cherrypy.expose
    def index(self):
        #basic login page
        body = """
        <h3> Qué dice la nueva constitución </h3>
        <form method='get', action='ver'>
            sobre: 
            <input type="text" placeholder="ingrese un tema" name="query" required>
            <input type="submit" class="button-primary" value="??"> 
        </form>
        """
        boiler = open('boilerplaye.html','r', encoding='utf-8').read().replace('{title}','Qué dice la nueva constitución')
        body = body + """  </div></div></div><div style="position: absolute; bottom: 0; right: 0; width: 300px; margin:10px; text-align:right;">
                        ...creado por Tomás Boncompte  </div>"""
        f = boiler.replace('{body_itself}',body).replace(': 5%',': 15%')
        return f
    
    @cherrypy.expose
    def ver(self, query):
        #basic login page
        body = """
        <h3> Sobre '%%%%', la nueva constitución dice: </h3>
        """.replace('%%%%',query)
        boiler = open('boilerplaye.html','r', encoding='utf-8').read().replace('{title}','Qué dice la nueva constitución')
        bo = format_response(consultar(query),query)
        body = '<div class="three columns"><a href="javascript:history.back()">Consultar otra cosa</a></div><br>'
        body = body + bo
        f = boiler.replace('{body_itself}',body)
        return f
        
# CherryPy stuff. 

if __name__ == '__main__':
    conf = {
        '/': {
            'tools.sessions.on': True,
            'tools.staticdir.root': os.path.abspath(os.getcwd())
        },
        '/static': {
            'tools.staticdir.on': True,
            'tools.staticdir.dir': './public'
        }
    }
    cherrypy.quickstart(App(), '/', conf)
