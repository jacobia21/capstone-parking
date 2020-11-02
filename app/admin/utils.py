import os
import datetime
import dropbox
from app import db
from app.models import SystemLog
from app.enums import LogStatus, LogType
from flask import current_app

def download(dbx, folder, subfolder, name):
    """Download a file.
    Return the bytes of the file, or None if it doesn't exist.
    """
    path = '/%s/%s/%s' % (folder, subfolder.replace(os.path.sep, '/'), name)
    while '//' in path:
        path = path.replace('//', '/')
    
    try:
        md, res = dbx.files_download(path)
    except dropbox.exceptions.HttpError as err:
        print('*** HTTP error', err)
        return None

    data = res.content
    print(len(data), 'bytes; md:', md)
    return data


def log_error_to_database(error):
    current_app.logger.log.error(error)
    db.session.rollback()
    error_message = str(error)
    log = SystemLog(message=error_message, status=LogStatus.OPEN, type=LogType.WEBSITE,
                    created_at=datetime.date.now())
    db.session.add(log)
    db.session.commit()