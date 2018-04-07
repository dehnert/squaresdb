#!/usr/bin/env python

from __future__ import print_function
from __future__ import unicode_literals

import argparse
import os.path
import random
import subprocess
import sys

BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true',
        help="Report planned changes but don't make them")
    parser.add_argument('--scripts', action='store_true',
        help="Set up web_scripts index.fcgi and media symlinks")
    parser.add_argument('--locker', type=str, default=os.environ["LOGNAME"],
        help="Locker name to use on scripts")
    parser.add_argument('--instance', type=str,
        help="Name of install instance to use. Used to name web_scripts "
             "subdir and sql.mit.edu database")
    parser.add_argument('--email', type=str, required=True,
        help="Set the forced recipient address to use")
    args = parser.parse_args()
    
    if args.scripts and not args.instance:
        pre, dj, post = BASE_DIR.partition('/Scripts/django/')
        if not dj:
            parser.error("in scripts.mit.edu mode, but instance was not "
                         "provided and path doesn't include /Scripts/django/ "
                         "so couldn't guess")

        instance, slash, post = post.partition('/')
        if slash:
            args.instance = instance
        else:
            parser.error("could not autodetect instance")

    if '@' not in args.email:
        parser.error("email must contain local part and domain")

    return args


def write_file(dry_run, filename, contents):
    if dry_run:
        print("Would write file '%s':" % (filename, ))
        print('"""')
        print(contents)
        print('"""')
        print("\n\n")
    else:
        with open(filename, 'wt') as fd:
            fd.write(contents)


def check_call(dry_run, cmd_args):
    if dry_run:
        print("Would call %s" % (cmd_args, ))
    else:
        subprocess.check_call(cmd_args)


SCRIPTS_SETTINGS = """
DATABASES = {{
    'default': {{
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '{locker}+{instance}',
        'OPTIONS': {{
            'read_default_file' : os.path.expanduser('~/.my.cnf'),
        }},
    }}
}}

ALLOWED_HOSTS = [
  'tech-squares.mit.edu', '{locker}.scripts.mit.edu',
  's-a.mit.edu',
]

SITE_SERVER = 'https://{locker}.scripts.mit.edu' # XXX: FIXME
SITE_WEB_PATH = '/{instance}'    # XXX: FIXME
SITE_URL_BASE = SITE_SERVER

COOKIES_PREFIX = "{instance}_"   # XXX: FIXME

ADMIN_MEDIA_PREFIX = '/__scripts/django/media/'
STATIC_URL = '/__scripts/django/static/'

"""


def init_settings(args):
    settings_dir = os.path.join(BASE_DIR, "squaresdb", "settings")
    tmpl_file = os.path.join(settings_dir, 'local.dev-template.py')
    tmpl_text = open(tmpl_file, 'rt').read()

    choices = 'abcdefghijklmnopqrstuvwxyz0123456789@#%-_=+'
    rand = random.SystemRandom()
    key = ''.join([rand.choice(choices) for i in range(50)])
    text = tmpl_text.replace("#SECRET_KEY = something", 'SECRET_KEY = "%s"' % key)
    
    text = text.replace("squares-db-forced-recipient@mit.edu", args.email)

    if args.scripts:
        scripts_db = SCRIPTS_SETTINGS.format(
            locker=args.locker,
            instance=args.instance,
        )
        insert_after = "import os\n\n"
        text = text.replace(insert_after, insert_after+scripts_db)

    local_file = os.path.join(settings_dir, 'local.py')
    write_file(args.dry_run, local_file, text)


def init_fcgi(args):
    util_dir = os.path.join(BASE_DIR, "squaresdb", "utils")
    tmpl_file = os.path.join(util_dir, 'scripts.tmpl.fcgi')
    tmpl_text = open(tmpl_file, 'rt').read()
    text = tmpl_text.format(executable=sys.executable, base=BASE_DIR)
    web_scripts = os.path.expanduser("~/web_scripts")
    instance_dir = os.path.join(web_scripts, args.instance)
    if not args.dry_run:
        os.mkdir(instance_dir)
    index_file = os.path.join(instance_dir, "index.fcgi")
    write_file(args.dry_run, index_file, text)


SCRIPTS_HTACCESS = """RewriteEngine On

RewriteRule ^$ index.fcgi/ [QSA,L]

RewriteCond %{REQUEST_FILENAME} !-f
RewriteCond %{REQUEST_FILENAME} !-d
RewriteRule ^(.*)$ index.fcgi/$1 [QSA,L]
"""

def init_htaccess(args):
    web_scripts = os.path.expanduser("~/web_scripts")
    htaccess_file = os.path.join(web_scripts, args.instance, ".htaccess")
    write_file(args.dry_run, htaccess_file, SCRIPTS_HTACCESS)


def init_db(args):
    def call(cmd_args):
        check_call(args.dry_run, cmd_args)
    # TODO: the DATABASES setting in settings/__init__.py is after the
    # "from .local import *" so Scripts doesn't actually use a non-local
    # DB. That should be fixed, and then these lines uncommented.
    #if args.scripts:
    #    call(['/mit/scripts/sql/bin/create-database', args.instance])
    manage = os.path.join(BASE_DIR, "manage.py")
    call([manage, "migrate"])
    call([manage, "createinitialrevisions",
          "--comment=Initial revision (in setup script)", "membership"])


NEXT_STEPS = """
Possible next steps:
- Clone the membership database (on Athena: /mit/tech-squares/club-private/signin/git/) and import it:
  membership/parsedb.py csv2django --csv membership/club-db/club.csv
- Create a superuser account:
  ../manage.py createsuperuser --email {email} --username $USER
"""

def write_instructions(args):
    if args.scripts:
        tmpl = "Visit the server at https://{locker}.scripts.mit.edu/{instance}/"
        msg = tmpl.format(locker=args.locker, instance=args.instance)
    else:
        msg = "Run the server with\n./manage.py runserver 8007\nor similar"
    print("\nDone! " + msg)
    print(NEXT_STEPS.format(email=args.email))
    

def init():
    args = parse_args()
    init_settings(args)
    if args.scripts:
        init_fcgi(args)
        init_htaccess(args)
    init_db(args)
    write_instructions(args)

if __name__ == '__main__':
    init()
