# -*- coding: utf-8 -*-
from flask import render_template, flash, redirect

from sourcerer import app
from sourcerer.views.forms import SearchForm
from sourcerer import logger
from sourcerer.tasks import cse_search_task


@app.route('/come_back')
def come_back():
    return render_template('come_back.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    try:
        form = SearchForm()
        logger.info(">>>>>>>> {}".format(form.validate_on_submit()))
        if form.validate_on_submit():
            cse_search_task.apply_async((form.search.data, ))
            return redirect('/come_back')
        return render_template('search.html',
                               title='Sign In',
                               form=form)
    except Exception as e:
        logger.exception('traceback')
        return 'Internal Server Error', 500
