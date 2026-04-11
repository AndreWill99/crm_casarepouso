from app import create_app

# Cria a App via factory
app = create_app()

if __name__ == '__main__':
    # Roda a App no modo de Desenvolvimento
    app.run(debug=True)
