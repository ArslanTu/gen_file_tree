from setuptools import setup

setup(
    name='gen_file_tree',
    version='1.0.0',
    packages=['gen_file_tree'],
    entry_points={
        'console_scripts': [
            'gft = gen_file_tree:main'
        ]
    },
    install_requires=[
        # 添加你的依赖库（如果有的话）
    ],
    author='ArslanTu',
    author_email='arslantu@arslantu.xyz',
    description='A script to generate file tree.',
    url='https://github.com/arslantu/gen_file_tree',
)
