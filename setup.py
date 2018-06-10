from setuptools import setup

setup(name='pvmanager',
      version='0.0.1',
      description='A VM manager written in Python.',
      url='http://github.com/terusus/pvmanager',
      author='Teodor Kostov',
      license='MIT',
      packages=['pvmanager', 'pvmanager.templates', 'pvmanager.manager', 'pvmanager.manager.media'],
      package_data = {
        '': ['*.m'],
      },
      install_requires=[
        'cement',
      ],
      scripts=['bin/pvmanager'],
      zip_safe=False)
