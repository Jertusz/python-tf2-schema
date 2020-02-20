from setuptools import setup


version = '0.1'

setup(
    name='tf2schema',
    packages=['tf2schema'],
    version=version,
    description='Python lib for various tf2 schema related tasks',
    author='Jędrzej Szadejko',
    author_email='shadyprywatny@gmail.com',
    license='MIT',
    url='https://github.com/Jertusz/python-tf2-schema',
    download_url='https://github.com/Jertusz/python-tf2-schema/releases',
    keywords=['steam', 'trade', 'tf2', 'teamfortress2', 'schema'],
    classifiers=[
        'Development Status :: 3 - Alpha',
    ],
    install_requires=['requests', 'vdf'],
)
