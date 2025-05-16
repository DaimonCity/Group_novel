from data.chapters import Chapter
from data import db_session
import json
import flask

blueprint = flask.Blueprint(
    'NS_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/chapter_tree/<int:chapter_id>')
def chapter_tree(chapter_id):
    db_sess = db_session.create_session()
    chapter = db_sess.query(Chapter).get(chapter_id)
    if not chapter:
        return None

    tree = {
        'id': chapter.id,
        'title': chapter.title,
        'children': []
    }

    if chapter.next:
        for child_id in json.loads(chapter.next):
            child_tree = chapter_tree(child_id)
            if child_tree:
                tree['children'].append(child_tree)

    return tree


