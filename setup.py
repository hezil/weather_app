from setuptools import setup

setup(
    name='weather_click',
    version='0.1',
    py_modules=['weather_click'],
    include_package_data=True,
    install_requires=[
        'click',
        #'sys',
        'requests',
    ],
    entry_points='''
        [console_scripts]
        weather_click=weather_click:cli
    ''',
)
