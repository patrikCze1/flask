from flask import Blueprint, render_template, url_for, request, redirect, flash, abort
from flask_login import current_user, login_required
from fl import db
from fl.models import User, Block, Group, Role, Category
from fl.admin.forms import BlockUser, SearchForm, CreateGroupForm, CreateRoleForm, CreateCategoryForm, UpdateRoleForm, UpdateGroupForm, AddUserIntoGroup

admin = Blueprint('admin', __name__)

#todo check user role
@admin.route('/admin/')
@login_required
def index():
    return render_template('./admin/admin.html', title='Admin page')


@admin.route('/admin/users', methods=['GET', 'POST'])
@login_required
def userAdmin():#Administration page
    form = SearchForm()
    users = User.query.order_by(User.created_at).all()
    if request.args.get('email', None):
        #users = User.query.join(Block, User.id==Block.user_id)
        email = request.args.get('email', '*', type=str)
        users = User.query.filter_by(email=email)
    return render_template('./admin/user.html', title='User administration', form=form, users=users)


@admin.route('/admin/block/<int:id>', methods=['GET', 'POST'])
@login_required
def blockUser(id):
    if current_user.role == 0:#permission
        abort(403)

    form = BlockUser()
    if request.method == 'POST' and form.validate_on_submit():
        block = Block(reason=form.reason.data, created_by=current_user.id, until=form.until.data, user_id=id)
        db.session.add(block)
        db.session.commit()
        flash('User is blocked', 'success')
        return redirect(url_for('main.home'))
    else:
        return render_template('./account/block.html', title='New block', form=form)


@admin.route('/admin/group')
@login_required
def groups():
    groups = Group.query.all()
    return render_template('./group/all.html', title='Groups', groups=groups)


@admin.route('/admin/group/<int:id>', methods=['GET', 'POST'])
@login_required
def showGroup(id):
    group = Group.query.get_or_404(id)
    addForm = AddUserIntoGroup()
    if addForm.validate_on_submit():
        user = User.query.get(addForm.user.data.id)
        user.group_id = id
        db.session.commit()#save
        flash('User was assigned', 'success')
        return redirect(url_for('admin.showGroup', id=id))

    if group.role_id:
        role = Role.query.get(group.role_id)
    else:
        role = 0

    users = User.query.all()
    return render_template('./group/show.html', title=f'Group - {group.name}', group=group, role=role, users=users, addForm=addForm)


@admin.route('/admin/group/create', methods=['GET', 'POST'])
@login_required
def createGroup():
    form = CreateGroupForm()
    if request.method == 'POST' and form.validate_on_submit():
        group = Group(name=form.name.data, active=form.active.data, description=form.description.data, role_id=form.role.data.id)
        db.session.add(group)
        db.session.commit()
        flash('New group has been created', 'success')
        return redirect(url_for('admin.index'))
    return render_template('./group/create.html', title='New group', form=form)


@admin.route('/admin/group/update/<int:id>', methods=['GET', 'POST'])
@login_required
def updateGroup(id):
    form = UpdateGroupForm()
    group = Group.query.get_or_404(id)
    if request.method == 'POST' and form.validate_on_submit():
        group.name = form.name.data
        group.active = form.active.data
        group.description = form.description.data
        group.role_id = form.role.data.id
        db.session.commit()#save
        flash('Group has been updated', 'success')
        return redirect(url_for('admin.groups'))

    form.name.data = group.name
    form.active.data = group.active
    form.description.data = group.description

    if group.role_id is not None:
        form.role = group.role_id

    return render_template('./group/update.html', title='Update group', form=form)


@admin.route('/admin/group/delete/<int:id>')
@login_required
def deleteGroup(id):
    group = Group.query.get_or_404(id)
    '''admin...
    if current_user.id == post.author.id:
        db.session.delete(group)
        db.session.commit()
        flash('Group has been deleted', 'success')
        return redirect(url_for('admin.groups'))
    else:
        abort(403)
    '''


@admin.route('/admin/role')
@login_required
def roles():
    roles = Role.query.all()
    return render_template('./role/all.html', title='Roles', roles=roles)


@admin.route('/admin/role/create', methods=['GET', 'POST'])
@login_required
def createRole():
    form = CreateRoleForm()
    if request.method == 'POST' and form.validate_on_submit():
        role = Role(name=form.name.data, value=form.value.data, active=form.active.data, description=form.description.data)
        db.session.add(role)
        db.session.commit()
        flash('New role has been created', 'success')
        return redirect(url_for('admin.index'))
    return render_template('./role/create.html', title='New role', form=form)


@admin.route('/admin/role/<int:id>')
@login_required
def showRole(id):
    role = Role.query.get(id)
    return render_template('./role/show.html', title=f'Role - {role.name}', role=role)


@admin.route('/admin/role/update/<int:id>', methods=['GET', 'POST'])
@login_required
def updateRole(id):
    form = UpdateRoleForm()
    role = Role.query.get_or_404(id)
    if request.method == 'POST' and form.validate_on_submit():
        role.name = form.name.data
        role.active = form.active.data
        role.value = form.value.data
        role.description = form.description.data
        db.session.commit()#save
        flash('Role has been updated', 'success')
        return redirect(url_for('admin.roles'))

    form.name.data = role.name
    form.active.data = role.active
    form.value.data = role.value
    form.description.data = role.description
    return render_template('./role/update.html', title='Update role', form=form)


@admin.route('/admin/role/delete/<int:id>')
@login_required
def deleteRole(id):
    role = Role.query.get_or_404(id)
    '''admin...
    if current_user.id == post.author.id:
        db.session.delete(role)
        db.session.commit()
        flash('Role has been deleted', 'success')
        return redirect(url_for('admin.roles'))
    else:
        abort(403)
    '''


@admin.route('/admin/category/create', methods=['GET', 'POST'])
@login_required
def createCategory():
    form = CreateCategoryForm()
    if request.method == 'POST' and form.validate_on_submit():
        category = Category(name=form.name.data)
        db.session.add(category)
        db.session.commit()
        flash('New category has been created', 'success')
        return redirect(url_for('admin.index'))
    return render_template('./category/create.html', title='New category', form=form)