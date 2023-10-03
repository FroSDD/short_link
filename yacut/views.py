from flask import flash, url_for, render_template, redirect

from . import app, db
from .forms import UrlForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def index_view():
    form = UrlForm()
    if form.validate_on_submit():
        short = form.custom_id.data or URLMap.get_unique_short_id()
        url_map = URLMap(
            original=form.original_link.data,
            short=short,
        )
        db.session.add(url_map)
        db.session.commit()
        flash(url_for('short_link_view', short=short, _external=True))
    return render_template('index.html', form=form)


@app.route('/<string:short>')
def short_link_view(short):
    return redirect(
        URLMap.query.filter_by(short=short).first_or_404().original
    )
