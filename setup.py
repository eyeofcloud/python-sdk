import os

from setuptools import setup
from setuptools import find_packages

here = os.path.join(os.path.dirname(__file__))


__version__ = None
with open(os.path.join(here, 'eyeofcloud', 'version.py')) as _file:
    exec(_file.read())

with open(os.path.join(here, 'requirements', 'core.txt')) as _file:
    REQUIREMENTS = _file.read().splitlines()

with open(os.path.join(here, 'requirements', 'test.txt')) as _file:
    TEST_REQUIREMENTS = _file.read().splitlines()
    TEST_REQUIREMENTS = list(set(REQUIREMENTS + TEST_REQUIREMENTS))

with open(os.path.join(here, 'README.md')) as _file:
    README = _file.read()

with open(os.path.join(here, 'CHANGELOG.md')) as _file:
    CHANGELOG = _file.read()

about_text = (
    'Eyeofcloud X Full Stack is A/B testing and feature management for product development teams. '
    'Experiment in any application. Make every feature on your roadmap an opportunity to learn. '
    'Learn more at https://www.eyeofcloud.com/products/full-stack/ or see our documentation at '
    'https://docs.developers.eyeofcloud.com/full-stack/docs. '
)

setup(
    name='eyeofcloud-sdk',
    version=__version__,
    description='Python SDK for Eyeofcloud X Full Stack.',
    long_description=about_text + README + CHANGELOG,
    long_description_content_type='text/markdown',
    author='Eyeofcloud',
    author_email='developers@eyeofcloud.com',
    url='https://gitee.com/eyeofcloud/python-sdk',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    packages=find_packages(exclude=['docs', 'tests']),
    extras_require={'test': TEST_REQUIREMENTS},
    install_requires=REQUIREMENTS,
    tests_require=TEST_REQUIREMENTS,
    test_suite='tests',
)
