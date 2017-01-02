from distutils.core import setup
setup(
    name='ezlog',
    packages=[
        'ezlog',
    ],
    package_dir={
        'ezlog': 'ezlog',
    },
    version='0.4',
    description='Helpful wrappers for logging',
    author='Eugene Ivanchenko',
    author_email='ez@eiva.info',
    url='https://github.com/eiva/ezlog',
    download_url='https://github.com/ezlog/todo',
    keywords=['logging', 'wrapper', 'performance'],  # arbitrary keywords
    classifiers=[],
)
