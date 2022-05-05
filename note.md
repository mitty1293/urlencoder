# poetry manual
https://python-poetry.org/docs/master/configuration/#virtualenvspath
> virtualenvs.path
>
> Type: string
>
> Directory where virtual environments will be created. Defaults to {cache-dir}/virtualenvs ({cache-dir}\virtualenvs on Windows).

https://python-poetry.org/docs/master/configuration/#virtualenvsin-project
> Type: boolean
>
> Create the virtualenv inside the project’s root directory. Defaults to None.
>
> If set to true, the virtualenv will be created and expected in a folder named .venv within the root directory of the project.
>
> If not set explicitly (default), poetry will use the virtualenv from the .venv directory when one is available. If set to false, poetry will ignore any existing .venv directory.

# POETRY_VIRTUALENVS_CREATE=true, POETRY_VIRTUALENVS_IN_PROJECT=null, dev
```
ls /usr/local/lib/python3.10/site-packages
README.txt  _distutils_hack  distutils-precedence.pth  pip  pip-22.0.4.dist-info  pkg_resources  setuptools  setuptools-58.1.0.dist-info  wheel  wheel-0.37.1.dist-info

poetry config --list
cache-dir = "/root/.cache/pypoetry"
experimental.new-installer = true
installer.parallel = true
virtualenvs.create = true
virtualenvs.in-project = null
virtualenvs.path = "{cache-dir}/virtualenvs"  # /root/.cache/pypoetry/virtualenvs

ls -l /root/.cache/pypoetry/virtualenvs
total 4
drwxr-xr-x 4 root root 4096 May  5 06:04 urlencoder-18LGIMdV-py3.10

ls -a /opt/pysetup
.  ..  poetry.lock  pyproject.toml

cd /opt/pysetup
poetry shell
Spawning shell within /root/.cache/pypoetry/virtualenvs/urlencoder-18LGIMdV-py3.10
root@c65cdf5d91ab:/opt/pysetup# . /root/.cache/pypoetry/virtualenvs/urlencoder-18LGIMdV-py3.10/bin/activate

(urlencoder-18LGIMdV-py3.10) root@c65cdf5d91ab:/opt/pysetup# which flask
/root/.cache/pypoetry/virtualenvs/urlencoder-18LGIMdV-py3.10/bin/flask

(urlencoder-18LGIMdV-py3.10) root@c65cdf5d91ab:/opt/pysetup# ls -l /root/.cache/pypoetry/virtualenvs/urlencoder-18LGIMdV-py3.10/lib/python3.10/site-packages/
drwxr-xr-x 8 root root    4096 May  5 06:04 flake8
drwxr-xr-x 4 root root    4096 May  5 06:04 flask
...
```
# POETRY_VIRTUALENVS_CREATE=true, POETRY_VIRTUALENVS_IN_PROJECT=true, dev
```
ls /usr/local/lib/python3.10/site-packages
README.txt  _distutils_hack  distutils-precedence.pth  pip  pip-22.0.4.dist-info  pkg_resources  setuptools  setuptools-58.1.0.dist-info  wheel  wheel-0.37.1.dist-info

poetry config --list
cache-dir = "/root/.cache/pypoetry"
experimental.new-installer = true
installer.parallel = true
virtualenvs.create = true
virtualenvs.in-project = true
virtualenvs.path = "{cache-dir}/virtualenvs"  # /root/.cache/pypoetry/virtualenvs

ls -l /root/.cache/pypoetry/virtualenvs
ls: cannot access '/root/.cache/pypoetry/virtualenvs': No such file or directory

ls -a /opt/pysetup
.  ..  .venv  poetry.lock  pyproject.toml

poetry shell
Spawning shell within /opt/pysetup/.venv
root@15f03625c7f2:/opt/pysetup# . /opt/pysetup/.venv/bin/activate

(.venv) root@15f03625c7f2:/opt/pysetup# which flask
/opt/pysetup/.venv/bin/flask

(.venv) root@15f03625c7f2:/opt/pysetup# ls -l .venv/lib/python3.10/site-packages/
drwxr-xr-x 8 root root    4096 May  5 05:13 flake8
drwxr-xr-x 4 root root    4096 May  5 05:13 flask
```
# POETRY_VIRTUALENVS_CREATE=false, dev
```
ls /usr/local/lib/python3.10/site-packages
drwxr-xr-x 8 root root    4096 May  5 04:44 flake8
drwxr-xr-x 4 root root    4096 May  5 04:44 flask
drwxr-xr-x 7 root root    4096 May  5 04:44 gunicorn

ls /opt/pysetup
poetry.lock  pyproject.toml

poetry config --list
cache-dir = "/root/.cache/pypoetry"
experimental.new-installer = true
installer.parallel = true
virtualenvs.create = false
virtualenvs.in-project = null
virtualenvs.path = "{cache-dir}/virtualenvs"  # /root/.cache/pypoetry/virtualenvs

ls -l /root/.cache/pypoetry/virtualenvs
ls: cannot access '/root/.cache/pypoetry/virtualenvs': No such file or directory

which flask
/usr/local/bin/flask
```


https://note.nkmk.me/python-import-module-search-path/  
import文で標準ライブラリやpipでインストールしたパッケージ、自作のパッケージなどをインポートするときに探索されるパス（ディレクトリ）をモジュール検索パスと呼ぶが、site-packagesはその中の1つ。  
つまりpythonコード内で呼び出す際に役立つが、linux shell上から呼び出せるわけではない。