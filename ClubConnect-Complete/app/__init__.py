"""
ClubConnect App Factory
"""

from flask import Flask
from flask_wtf.csrf import CSRFProtect
from config import config

# Extensions
csrf = CSRFProtect()

def create_app(config_name=None):
    """App Factory Pattern"""
    app = Flask(__name__)
    
    # Konfiguration laden
    config_class = config.get(config_name, config['default'])
    app.config.from_object(config_class)
    
    # Extensions initialisieren
    csrf.init_app(app)
    
    # Blueprints importieren und registrieren
    from app.main import bp as main_bp
    from app.auth import bp as auth_bp
    from app.admin import bp as admin_bp
    
    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Error Handler
    @app.errorhandler(404)
    def not_found_error(error):
        from flask import render_template
        return render_template('errors/404.html'), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        from flask import render_template
        return render_template('errors/500.html'), 500
    
    @app.errorhandler(403)
    def forbidden_error(error):
        from flask import render_template
        return render_template('errors/403.html'), 403
    
    # Template-Kontext-Prozessoren
    @app.context_processor
    def inject_config():
        return dict(CLUB_NAME=app.config.get('CLUB_NAME', 'ClubConnect'))
    
    return app
