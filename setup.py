from setuptools import setup, find_packages
 
setup(
    name='pySigfox',
    version='0.1.0.dev1',
    description='Connect to Sigfox REST API from Python. This is absolutely NOT OFFICIAL package!!',
    url='http://www.github.com/hecko/pySigfox',
    author='Marcel Hecko',
    author_email='maco@blava.net',
    classifiers=[
                  'Development Status :: 3 - Alpha',
                  'Programming Language :: Python :: 2.7',
                ],
    packages=find_packages(),
    install_requires=['requests'],
)
