from setuptools import setup

install_requires = [
    'Keesung_logging @ git+https://github.com/GNuSeekK/Keesung_logging@v0.0.8#egg=Keesung_logging',
    ]
setup_requires=[
    'Kessung_logging>=0.0.8'
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
    setup_requires=setup_requires
)