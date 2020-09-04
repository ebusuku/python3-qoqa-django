import venv
import os
import subprocess
import stat
import shutil

from .build import DATA_DIRECTORY
from colorama import Fore


default_template_zip = os.path.join(DATA_DIRECTORY, "template.zip")


class SingleVenv(venv.EnvBuilder):
    """
    Class to just create a virtualenv on an existing project
    """

    def __init__(self, dj_version, *args, **kwargs):
        self.dj_version = dj_version
        super().__init__(*args, **kwargs)

    def post_setup(self, context):
        """
        install default applications
        """
        os.environ["VIRTUAL_ENV"] = context.env_dir
        pip = os.path.join(context.bin_path, "pip")
        try:
            print(Fore.GREEN + "[qoqa] Installing pip files ")
            print(Fore.GREEN + "[qoqa] Preparing to install django")
            subprocess.run(
                [pip, "install", "django=={}".format(self.dj_version)], check=True
            )
            print(Fore.GREEN + "[qoqa] django package installed")
            print(Fore.GREEN + "[qoqa] Preparing to install whitenoise")
            subprocess.run([pip, "install", "whitenoise"], check=True)
            print(Fore.GREEN + "[qoqa] whitenoise package installed")
            print(Fore.GREEN + "[qoqa] Preparing to " "install django-debug-toolbar")
            subprocess.run([pip, "install", "django-debug-toolbar"], check=True)
            print(Fore.GREEN + "[qoqa] django-debug-toolbar package installed")
            print(Fore.GREEN + "[qoqa] Preparing into install gunicorn")
            subprocess.run([pip, "install", "gunicorn"], check=True)
            print(Fore.GREEN + "[qoqa] gunicorn package installed")
        except subprocess.CalledProcessError as err:
            print(Fore.RED + "[qoqa] Unable to download pip files," "cleaning up")
            print(Fore.RED + "[qoqa] removing incomplete directory")
            os.chdir("..")
            shutil.rmtree(self._project_name)
            exit()
        else:
            self._requirements(context)

    def _requirements(self, context):
        """
        check for requirements file and pull dependencies if needed
        """
        pip = os.path.join(context.bin_path, "pip")
        if os.path.isfile("requirements.txt"):
            try:
                print(Fore.GREEN + "[qoqa] fetching dependencies")
                subprocess.run([pip, "install", "-r", "requirements.txt"], check=True)
            except subprocess.CalledProcessError as error:
                print(Fore.RED + "[qoqa] Unable to download pip files")
                exit()
        else:
            print(
                Fore.BLUE + "[qoqa] Unable to find requirements.txt " "Continuing....."
            )


class ExtendVenv(venv.EnvBuilder):
    def __init__(self, project_name, django_version, template_path, *args, **kwargs):
        self._project_name = project_name
        self._django_version = django_version
        self.template_path = template_path
        super().__init__(*args, **kwargs)

    def post_setup(self, context):
        """
        install default applications
        """
        os.environ["VIRTUAL_ENV"] = context.env_dir
        pip = os.path.join(context.bin_path, "pip")
        try:
            print(Fore.GREEN + "[qoqa] Installing pip files: ")
            print(Fore.GREEN + "[qoqa] Preparing to install django")
            subprocess.run(
                [pip, "install", f"django=={self._django_version}"], check=True
            )
            print(Fore.GREEN + "[qoqa] Preparing to install whitenoise")
            subprocess.run([pip, "install", "whitenoise"], check=True)
            print(Fore.GREEN + "[qoqa] installing django-debug-toolbar")
            subprocess.run([pip, "install", "django-debug-toolbar"], check=True)
            print(Fore.GREEN + "[qoqa] Preparing into install gunicorn")
            subprocess.run([pip, "install", "gunicorn"], check=True)
            print(Fore.GREEN + "[qoqa] installing psycopg2")
            subprocess.run([pip, "install", "psycopg2"], check=True)
        except subprocess.CalledProcessError as error:
            print(
                Fore.RED + f"[qoqa] Unable to download pip files cleaning up: {error}"
            )
            exit()
        else:
            self._startproject(context)

    def _startproject(self, context):
        """
        Create a new django projecte
        """
        if not self.template_path:
            self.template_path = default_template_zip
        dj_admin_script = os.path.join(context.bin_path, "django-admin")
        print(Fore.GREEN + "[qoqa] initializing django project....................")
        try:
            subprocess.run(
                [
                    dj_admin_script,
                    "startproject",
                    "--template=" + self.template_path,
                    self._project_name,
                    ".",
                ],
                check=True,
            )

            print(Fore.GREEN + "[qoqa] django project created")
        except subprocess.CalledProcessError as error:
            print(Fore.RED + f"Unable to use zip template: {error}")
            exit()
        else:
            print(Fore.GREEN + "[qoqa] making manage.py executable")
            os.chmod("manage.py", stat.S_IRWXU)


def create(project_name: str, dj_version: str, template_path):
    """
    create new virtual environment
    """
    env = ExtendVenv(project_name, dj_version, template_path, with_pip=True)
    env.create("env3")
