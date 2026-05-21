#!/bin/bash

# Activar venv
source venv/bin/activate

# Iniciar backend en segundo plano
python app.py &

# Ir al frontend
cd Comparador_instagram

# Iniciar Angular
ng serve