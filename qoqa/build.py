import os
import subprocess
import shutil

DATA_DIRECTORY = os.path.join(os.path.dirname(__file__), 'data')


def create_changelog():
    """
    Create initial changelog file
    """
    try:
        subprocess.run([
            'dch',
            '--create',
            '--package', os.path.basename(os.getcwd()),
            '--newversion', '0.1.0-1'
        ])
    except subprocess.CalledProcessError as error:
        print("[qoqa] Unable to create changelog file")
        print("[qoqa] {}".format(error))
        exit()


def debian():
    """
    Create debian directory with required files
    """
    os.mkdir('debian')
    debian_data = os.path.join(DATA_DIRECTORY, 'debian')
    rules_file = os.path.join(debian_data, 'rules.example')
    control_file = os.path.join(debian_data, 'control.example')
    compat_file = os.path.join(debian_data, 'compat.example')
    postint_file = os.path.join(debian_data, 'postinst.example')
    postrm_file = os.path.join(debian_data, 'postrm.example')
    service_file = os.path.join(debian_data, 'gunicorn.example')
    try:
        project_name = os.path.basename(os.getcwd())
        shutil.copyfile(rules_file, os.path.join('debian', 'rules'))
        shutil.copyfile(compat_file, os.path.join('debian', 'compat'))
        shutil.copyfile(postint_file, os.path.join('debian', 'postinst'))
        shutil.copyfile(control_file, os.path.join('debian', 'control'))
        shutil.copyfile(postrm_file, os.path.join('debian', 'postrm'))
        shutil.copyfile(service_file, os.path.join('debian',
                                                   project_name+'.service'))
        create_changelog()
    except OSError as error:
        print("[qoqa] {}".format(error))
        exit()
    except FileNotFoundError as error:
        print("[qoqa] {}".format(error))
        exit()
    else:
        template_files()


def template_files():
    """
    Read in files in debian directory and replace variables.
    """
    parent_directory = os.path.basename(os.getcwd())
    for filename in os.listdir('debian'):
        with open(os.path.join('debian', filename), 'r+') as f:
            text = f.read().replace('$projectname', parent_directory)
            f.seek(0)
            f.truncate()
            f.write(text)
    print("[qoqa] debian directory setup")


def python_setup_file():
    """
    Create setup.py file from template and copy to project directory
    """
    setuppy_file = os.path.join(DATA_DIRECTORY, 'setup.py.example')
    with open(setuppy_file, 'r') as f:
        text = f.read().replace('$projectname', os.path.basename(os.getcwd()))
        with open(os.path.join(os.getcwd(), 'setup.py'), 'w') as setup_file:
            setup_file.write(text)
    print('[qoqa] setup.py file created')


def requirements():
    """
    Check whether requirements file exists
    """
    print(
          "[qoqa] create one by activating the relevant virtual environment "
          "and typing the command "
          "pip freeze > requirements.txt")
    exit()


def manifest():
    """
    Create manifest file
    """
    data_directory = os.path.join(os.path.dirname(__file__), 'data')
    manifest_file = os.path.join(data_directory, 'MANIFEST.in.example')
    with open(manifest_file, 'r') as f:
        text = f.read().replace('$projectname', os.path.basename(os.getcwd()))
        with open(os.path.join(os.getcwd(), 'MANIFEST.in'), 'w') as manifest:
            manifest.write(text)
    print('[qoqa] MANIFEST.in file created')


def dpkg():
    """
    Start the build process
    """
    try:
        subprocess.run([
            'dpkg-buildpackage',
            '-us',
            '-uc'
        ])
    except subprocess.CalledProcessError as error:
        print("[qoqa] unable to build project")
        print(['[qoqa] {}'.format(error)])
        exit()
    print("[qoqa] django project built")
