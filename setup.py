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
        'flask-cors',
        'eventlet',
        'gunicorn',
        'simplejson',
        'colorlog',
        'rdflib',
    ],

    dependency_links = [
            'https://github.com/BB-Open/pkan.blazegraph.git#egg=pkan.blazegraph-0.1.dev0'
                ],
)
