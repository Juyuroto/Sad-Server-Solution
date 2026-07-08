from flask import Flask, request

app = Flask(__name__)

@app.route('/', methods=['POST'])
def login():
    # Récupère la valeur associée à la clé 'password'
    mot_de_passe = request.form.get('password')
    
    print(f"Mot de passe reçu : {mot_de_passe}")
    return f"Bien reçu ! Valeur : {mot_de_passe}"

if __name__ == '__main__':
    app.run(port=5000)