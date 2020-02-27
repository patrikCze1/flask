from fl import createApp, db
from fl.models import Role

app = createApp()

with app.app_context():
    db.create_all()
    '''
    admin = Role(name='admin', value=0)
    user = Role(name='user', value=100)
    db.session.add(admin)
    db.session.add(user)
    db.session.commit()
    '''

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0')