from setuptools import setup, find_packages

setup(
    name='pkan_flask',
    version='',
    packages=find_packages('src', exclude=['ez_setup']),
    namespace_packages=['pkan',
                        'pkan.flask',
                        ],
    package_dir={'': 'src'},
    url='',
    license='',
    author='sandra',
    author_email='',
    description='',
    install_requires = [
        'Flask',
        'flask-socketio',
        'eventlet',
        'gunicorn',
        'simplejson',
        'colorlog',
        'rdflib',
    ],
)
