# ---------------------------------------------------------------------------------------------------
# librerias
import os
from dash import Dash
from src.layout import create_layout
# ---------------------------------------------------------------------------------------------------
# asignacion de variables
app = Dash(__name__)

# ---------------------------------------------------------------------------------------------------
# layout
app.layout = create_layout(app)

# ---------------------------------------------------------------------------------------------------
# callback

# ---------------------------------------------------------------------------------------------------
# llamado de funcion principal
if __name__ == '__main__':
    port =  int(os.environ.get("PORT", 8050))
    app.run(debug=True,host='0.0.0.0', port=port)


# Exponer el servidor para Render
server = app.server
