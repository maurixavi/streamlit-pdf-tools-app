from email.policy import default
import streamlit as st
from streamlit_option_menu import option_menu

import home, pdf_merger, pdf_splitter

st.set_page_config(
  page_title='PDF Tools', layout="centered", initial_sidebar_state="auto", menu_items=None
)

class MultiApp:
  
  def __init__(self):
    self.apps = []
    
  def add_app(self, title, function):
    self.apps.append({
      "title": title,
      "function": function,
    })

  def run(self):
    # Menú de opciones con estilos aplicados directamente
    with st.sidebar:
      page = option_menu(
        menu_title = None,
        options=['Home', 'Merge PDF', 'Extract Pages PDF'],
        default_index=0,
        styles={
          "nav-link": {
            "font-size": "14px",
          }
        }
      )

    # Renderizar la página correspondiente según la opción seleccionada
    if page == 'Home':
      home.app()
    elif page == 'Merge PDF':
      pdf_merger.app()
    elif page == 'Extract Pages PDF':
      pdf_splitter.app()

# Instanciar y ejecutar la aplicación
app = MultiApp()
app.run()
