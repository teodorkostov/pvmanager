from setuptools import setup

setup(name='pvmanager',
      version='0.0.1',
      description='Python VM Manager',
      url='http://github.com/terusus/pvmanager',
      author='Teodor Kostov',
      license='GPLv3',
      packages=['pvmanager', 'pvmanager.templates', 'pvmanager.manager', 'pvmanager.manager.media'],
      package_data={
        '': ['*.m', '*.yaml'],
      },
      install_requires=[
        'cement',
        'humanfriendly',
        'pystache'
      ],
      scripts=['bin/pvmanager'],
      zip_safe=False)
