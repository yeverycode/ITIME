import os
import glob

for migration_file in glob.glob('**/migrations/*.py', recursive=True):
    if os.path.basename(migration_file) != '__init__.py':
        os.remove(migration_file)

for migration_file in glob.glob('**/migrations/*.pyc', recursive=True):
    os.remove(migration_file)
