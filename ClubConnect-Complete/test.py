from flask import Flask, render_template_string

app = Flask(__name__)

@app.route('/')
def home():
    return render_template_string('''
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>ClubConnect - Test</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <div class="jumbotron bg-primary text-white p-5 rounded">
            <h1 class="display-4">🎉 ClubConnect funktioniert!</h1>
            <p class="lead">Das Vereinsmanagement-System ist erfolgreich gestartet.</p>
            <hr class="my-4">
            <p>Der Flask-Server läuft korrekt auf Port 5000.</p>
            <a class="btn btn-light btn-lg" href="/admin" role="button">Zum Admin-Bereich</a>
        </div>
        
        <div class="row mt-4">
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5>✅ System Status</h5>
                    </div>
                    <div class="card-body">
                        <ul class="list-group list-group-flush">
                            <li class="list-group-item">✅ Flask-Server läuft</li>
                            <li class="list-group-item">✅ Bootstrap CSS geladen</li>
                            <li class="list-group-item">✅ Responsive Design aktiv</li>
                            <li class="list-group-item">✅ Port 5000 erreichbar</li>
                        </ul>
                    </div>
                </div>
            </div>
            <div class="col-md-6">
                <div class="card">
                    <div class="card-header">
                        <h5>🚀 Nächste Schritte</h5>
                    </div>
                    <div class="card-body">
                        <p>Das ClubConnect-System ist bereit!</p>
                        <p><strong>Login-Daten:</strong></p>
                        <ul>
                            <li>Benutzername: admin</li>
                            <li>Passwort: admin123</li>
                        </ul>
                    </div>
                </div>
            </div>
        </div>
    </div>
</body>
</html>
    ''')

@app.route('/admin')
def admin():
    return render_template_string('''
<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Admin - ClubConnect</title>
    <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.3.0/dist/css/bootstrap.min.css" rel="stylesheet">
</head>
<body>
    <div class="container mt-5">
        <h1>🔧 Admin-Bereich</h1>
        <div class="alert alert-success">
            <h4>Erfolgreich!</h4>
            <p>Der Admin-Bereich ist erreichbar. Das ClubConnect-System funktioniert korrekt.</p>
        </div>
        <a href="/" class="btn btn-primary">Zurück zur Startseite</a>
    </div>
</body>
</html>
    ''')

if __name__ == '__main__':
    print("🚀 Starte ClubConnect Test-Server...")
    print("📍 URL: http://localhost:5000")
    print("🔑 Login: admin / admin123")
    print("⏹️  Stoppen mit Ctrl+C")
    app.run(host='0.0.0.0', port=5000, debug=True)
