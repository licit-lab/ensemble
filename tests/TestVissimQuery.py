import os
from click.testing import CliRunner
#from ensemble import ensemble
from ensemble import cli

runner = CliRunner()
file_name = "TestNetwork.inpx"
file_layx="TestNetwork.layx"
file_path = ("tests", "mocks", "bottlenecks", file_name)
file_layx_path = ("tests", "mocks", "bottlenecks", file_layx)
mocks_path = os.path.join(os.getcwd(), *file_path)
mocks_path_layx = os.path.join(os.getcwd(), *file_layx_path )
runner.invoke(cli.main,["launch", "-s", mocks_path,"-s",mocks_path_layx])