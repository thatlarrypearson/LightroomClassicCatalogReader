from setuptools import setup, find_packages
setup(
    name="lr-reader",
    version="0.3",

    packages=find_packages('src'),
    py_modules=['lr_reader', ],
    install_requires=[],
    python_requires='>=3.6',

    # metadata to display on PyPI
    author="Larry Pearson",
    author_email="ThatLarryPearson@gmail.com",
    license='MIT',
    description="Extract and output image file data from Lightroom Classic databases",
    long_description_content_type="text/markdown",
    long_description=open('README.md').read(),
    keywords=[
        'Adobe Lightroom Classic', 'Lightroom',
        'Catalog', 'Database', '.lrcat', 'SQLite3',
        'Image', 'File', 'Reader',
    ],
    url="https://github.com/thatlarrypearson/LightRoomClassicCatalogReader",
    project_urls={
        "Bug Tracker": "https://github.com/thatlarrypearson/LightRoomClassicCatalogReader",
        "Documentation": "https://github.com/thatlarrypearson/LightRoomClassicCatalogReader",
        "Source Code": "https://github.com/thatlarrypearson/LightRoomClassicCatalogReader",
    },
    classifiers=[
        "License :: OSI Approved :: MIT License",
        'Programming Langauge :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
)