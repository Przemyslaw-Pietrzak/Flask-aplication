from functools import wraps
from flask import request, redirect, url_for, flash
from flask_login import current_user

#własny dekorator admin_required - dostęp tylko dla admina
def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            flash('Musisz być zalogowany, aby uzyskać dostęp do panelu administratora!', 'danger')
            return redirect(url_for('login', next=request.url))
        
        if not getattr(current_user, 'is_admin', False):
            flash('Nie masz uprawnień administratora.', 'warning')
            return redirect(url_for('index'))  # np. do strony głównej
        
        return f(*args, **kwargs)
    return decorated_function