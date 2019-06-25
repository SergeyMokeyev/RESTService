import setuptools


with open('README.md', 'r') as fh:
    long_description = fh.read()


with open('requirements.txt', 'r') as fr:
    requirements = fr.read().split('\n')


setuptools.setup(
    name='restservice',
    version='0.1.0',
    author='Sergey Mokeyev',
    author_email='sergey.mokeyev@gmail.com',
    description='A small JSON API service template',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/SergeyMokeyev/RESTService',
    packages=setuptools.find_packages(exclude=['tests', 'examples']),
    classifiers=[
        'Programming Language :: Python :: 3.7',
        'License :: OSI Approved :: GPL3',
        'Operating System :: POSIX',
    ],
    install_requires=requirements
)
