from flask import render_template
from project.blueprints import pages_app
from project.models import Page, UploadedImage


def chunks(lst, n):
    """Yield n-sized parts from lst
    ([0,1,2,3,4,5,6,7,8], 3) -> [[0,1,2],[3,4,5],[6,7,8]]"""
    for i in range(0, len(lst), n):
        yield lst[i:i+n]


@pages_app.route("/")
def mainpage():
    page = Page.bl.get(Page.TYPE.MAINPAGE)
    images = (
        UploadedImage.query
        .filter(
            UploadedImage.img_category == UploadedImage.IMG_CATEGORY.gallery
        )
        .all()
    )
    return render_template(
        'pages/mainpage.html',
        blocks=page.blocks,
        images=chunks(images, 4),
        title=page.title,
    )


@pages_app.route('/projects/')
def projects():
    page = Page.bl.get(Page.TYPE.PROJECTS)
    return render_template(
        'pages/projects.html',
        blocks=page.blocks,
        title=page.title,
    )


@pages_app.route('/about/')
def about():
    page = Page.bl.get(Page.TYPE.ABOUT)
    return render_template(
        'pages/about.html',
        blocks=page.blocks,
        title=page.title,
    )


@pages_app.route('/contacts/')
def contacts():
    page = Page.bl.get(Page.TYPE.CONTACTS)
    return render_template(
        'pages/contacts.html',
        blocks=page.blocks,
        title=page.title,
    )
