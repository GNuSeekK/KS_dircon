from setuptools import setup

install_requires = [
    'Keesung-logging==v0.0.8',
    ]

dependency_links = [
    'git+https://github.com/GNuSeekK/Keesung_logging.git@v0.0.8',
    ]

setup(
    name = 'KS_dircon',
    version='0.0.1',
    description='Custom KS_dircon',
    url='https://github.com/GNuSeekK/KS_dircon.git',
    author='Keesung',
    author_email='dlrltjdwkd@naver.com',
    license='keesung',
    packages=['KS_dircon'],
    install_requires=install_requires,
    dependency_links=dependency_links
)