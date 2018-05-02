from setuptools import setup, find_packages

setup(name='b1tifi',
    version='1.3.2',
    description='SSH BOT management for distributed attacks',
    classifiers=[
        'License :: MIT License',
        'Programming Language :: Python :: 2.7',
    ],
    keywords='ssh botssh botnet management',
    url='http://github.com/mh4x0f/bitifi',
    author='Marcos Nesster @mh4x0f',
    author_email='mh4root@gmail.com',
    license='MIT',
    packages=find_packages(include=[
        'shell', 'shell.*'
    ]),
    install_requires=[
        'tabulate',
        'pexpect',
        'pysqlite',
      ],
    entry_points = {
        'console_scripts': ['b1tifi=shell.b1tifi:main',],
    },
    include_package_data=True,
    zip_safe=False)
