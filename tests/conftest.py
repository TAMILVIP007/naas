import pytest  # noqa: F401
import black  # noqa: F401  # FIX for https://github.com/psf/black/issues/1143
import os
import getpass
import logging
from naas.runner import Runner, n_env  # noqa: E402

user_folder_name = "pytest_tmp"
path_srv_root = os.path.join(os.getcwd(), user_folder_name)
n_env.server_root = str(path_srv_root)


@pytest.fixture
def runner(caplog, tmp_path):
    caplog.set_level(logging.INFO)
    user = getpass.getuser()
    path_srv = os.path.join(tmp_path, user_folder_name)
    n_env.user = user
    n_env.server_root = str(path_srv)
    n_env.scheduler_interval = "1"
    n_env.scheduler_job_max = "3"
    n_env.hub_api = "http://localhost:5000"
    n_env.proxy_api = "http://localhost:5001"
    n_env.notif_api = "http://localhost:5002"

    yield Runner().init_app()


@pytest.fixture
def test_cli(loop, runner, sanic_client):
    yield loop.run_until_complete(sanic_client(runner))
