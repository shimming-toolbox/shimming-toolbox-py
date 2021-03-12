from setuptools import setup, find_packages

setup(
    # the name must begin with "fsleyes-plugin-"
    name='fsleyes-plugin-shimming-toolbox',

    # Views, controls, and tools must be exposed
    # as entry points within groups called
    # "fsleyes_views", "fsleyes_controls" and
    # "fsleyes_tools" respectively.
    entry_points={
        # 'fsleyes_views': [
        #     'My cool view = myplugin:MyView'
        # ],
        'fsleyes_controls': [
            'My cool control = fsleyes_plugin_shimming_toolbox.st_plugin:STControlPanel'
        ],
        # 'fsleyes_tools': [
        #     'My cool tool = myplugin:MyTool'
        # ]
    }
)
