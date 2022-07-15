from setuptools import setup

setup(
    name='apkmaker',
    version='0.1',
    py_modules=['apkmaker'],
    install_requires=[
        'Click',
    ],
    entry_points='''
        [console_scripts]
        apkmaker=apkmaker:apkmaker
    ''',
)
