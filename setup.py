from setuptools import setup

setup(name='ficrawler',
      version='1.0.0',
      description='ficrawler',
      author='likunheng',
      author_email='624448574@qq.com',
      # url='https://www.python.org/',
      # license='MIT',
      # keywords='ga nn',
      # project_urls={
      #       'Documentation': 'https://packaging.python.org/tutorials/distributing-packages/',
      #       'Funding': 'https://donate.pypi.org',
      #       'Source': 'https://github.com/pypa/sampleproject/',
      #       'Tracker': 'https://github.com/pypa/sampleproject/issues',
      # },
      packages=['ficrawler'],
      entry_points={
          'console_scripts': [
              'ficrawl = ficrawler.crawl:main',
              'fiquery = ficrawler.query:main',
          ]
      },
      )