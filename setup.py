from setuptools import setup

setup(name='ficrawler',
      version='1.0.0',
      description='ficrawler',
      author='likunheng',
      author_email='624448574@qq.com',
      packages=['ficrawler'],
      entry_points={
          'console_scripts': [
              'ficrawl = ficrawler.crawl:main',
              'fiquery = ficrawler.query:main',
              'fitest = ficrawler.test:main',
          ]
      },
      )