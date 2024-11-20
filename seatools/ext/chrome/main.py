import os

import click
from typing import Optional
from seatools.ext.chrome import list_chrome, common_download_chrome
from loguru import logger
from .utils import find_project_dir, find_package_dir

__allow_system__ = ["linux64", "mac-arm64", "mac-x64", "win64", "win32"]
__allow_type__ = ['chrome', 'chromedriver', 'all']

def _extract_project_package_dir(project_dir, package_dir):
    project_dir = project_dir or find_project_dir(os.getcwd())
    if not project_dir:
        logger.error('无法找到项目目录')
        exit(1)
    package_dir = package_dir or find_package_dir(project_dir)
    if not package_dir:
        logger.error('无法找到包目录')
        exit(1)
    logger.info("项目目录: {}", project_dir)
    logger.info("包目录: {}", package_dir)
    return project_dir, package_dir


@click.group()
@click.version_option(version="1.0.0", help='查看命令版本')
@click.help_option('-h', '--help', help='查看命令帮助')
def main() -> None:
    """谷歌工具"""
    return None


@main.command()
@click.option('--project_dir', default=None, help='项目目录, 默认从项目内的任意位置执行能够自动检索, 不传也可')
@click.option('--package_dir', default=None, help='包目录, 若不传则基于项目目录自动检索')
@click.version_option(version="1.0.0", help='查看命令版本')
@click.option('--grep', default=None, help='筛选查询')
@click.help_option('-h', '--help', help='查询所有chrome/chromedriver版本, 仅支持114以上版本')
def list(project_dir: Optional[str] = None,
         package_dir: Optional[str] = None,
         grep: Optional[str] = None):
    project_dir, package_dir = _extract_project_package_dir(project_dir, package_dir)
    logger.success('\n'.join([item for item in list_chrome(project_dir=project_dir, package_dir=package_dir) if not grep or grep in item]))


@main.command()
@click.option('--project_dir', default=None, help='项目目录, 默认从项目内的任意位置执行能够自动检索, 不传也可')
@click.option('--package_dir', default=None, help='包目录, 若不传则基于项目目录自动检索')
@click.option('--installer_dir', default=None, help='下载安装目录, 默认为{project_dir}/extensions')
@click.option('-v', '--version', default=None, help='下载的chrome版本, 该参数不能为空')
@click.option('-s', '--system', default='win64', help='下载的chrome系统, 支持: linux64, mac-arm64, mac-x64, win64, win32, 默认: win64')
@click.option('-t', '--type', default='chromedriver',
              help='下载的chrome类型, 支持: chrome, chromedriver, all(同时下载chrome和chromedriver) 默认: chromedriver')
@click.help_option('-h', '--help', help='下载chrome, 并保存至项目extensions目录')
def download(project_dir: Optional[str] = None,
             package_dir: Optional[str] = None,
             installer_dir: Optional[str] = None,
             version: Optional[str] = None,
             system: Optional[str] = 'win64',
             type: Optional[str] = 'chromedriver'):
    project_dir, package_dir = _extract_project_package_dir(project_dir, package_dir)
    installer_dir = installer_dir or (project_dir + os.sep + 'extensions')
    if not version:
        logger.error('版本不能为空')
        exit(1)
    if system not in __allow_system__:
        logger.error('系统[{}]不支持, 请使用-h参数查看支持的系统类型'.format(system))
        exit(1)
    if type not in __allow_type__:
        logger.error('类型[{}]不支持, 请使用-h参数查看支持的系统类型'.format(type))
        exit(1)

    if type in ('chrome', 'all'):
        common_download_chrome(project_dir=project_dir, package_dir=package_dir,
                               version=version, system=system, type_='chrome',
                               installer_dir=installer_dir)
    if type in ('chromedriver', 'all'):
        common_download_chrome(project_dir=project_dir, package_dir=package_dir,
                               version=version, system=system, type_='chromedriver',
                               installer_dir=installer_dir)
