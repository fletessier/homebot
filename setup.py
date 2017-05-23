
from setuptools import setup, find_packages


with open('README.rst') as f:
    readme = f.read()

with open('LICENSE') as f:
    license = f.read()

setup(
    name='homebot',
    version='0.0.1',
    description='Chatbot app',
    long_description=readme,
    author='fletessier',
    author_email='',
    url='https://github.com/fletessier/homebot',
    license=license,
    packages=find_packages(exclude=('tests', 'docs'))
)
