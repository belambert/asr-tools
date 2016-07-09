from setuptools import setup

setup(
    name='asr_tools',
    version='0.1',
    author='Ben Lambert',
    author_email='ben@benjaminlambert.com',
    packages=['asr_tools'],
    description='Automatic speech recognition tools.',
    url='https://github.com/belambert/asr-tools',
    keywords=['automatic speech recognition', 'speech recognition', 'asr'],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Programming Language :: Python",
        "Topic :: Scientific/Engineering",
        "License :: OSI Approved :: BSD License"],
    # install_requires=['edit_distance', 'asr_evaluation'],
    test_suite='test.test_main.Testing'
)
