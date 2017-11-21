# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect, jsonify

from sourcerer import app, logger, db
from .forms import SearchForm
from sourcerer.tasks import search_task


@app.route('/come_back')
def come_back():
    return render_template('come_back.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    try:
        form = SearchForm()
        logger.info(">>>>>>>> {}".format(form.validate_on_submit()))
        if form.validate_on_submit():
            search_task.apply_async((form.search.data, ))
            return redirect('/come_back')
        return render_template('search.html',
                               form=form)
    except Exception as e:
        logger.exception('traceback')
        return 'Internal Server Error', 500
