from flask import Blueprint, render_template, url_for, request, flash
from flask_login import login_required
from fl.models import Post
from fl.main.forms import ContactForm
from fl.main.utils import sendEmail

main = Blueprint('main', __name__)


@main.route('/')
def index():
    return render_template('./index.html', title='Index page')


@main.route('/home')
@login_required
def home():
    page = request.args.get('page', 1, type=int)
    order = request.args.get('order', 'created_at', type=str)
    posts = Post.query.filter_by(active=True).filter_by(approved=True).order_by(order).paginate(page=page, per_page=5)
    return render_template('./home.html', title='Home page', posts=posts)


@main.route('/about', methods=['POST', 'GET'])
def about():
    form = ContactForm()
    if request.method == 'POST' and form.validate():
        sendEmail(form.email.data, form.title.data, form.text.data)
        flash('Your message was send.')
        return render_template('./about.html', title='About')
    else:
        form = ContactForm(request.form)
        return render_template('./about.html', title='About', form=form)