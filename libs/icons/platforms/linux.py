from glob import glob
from os import listdir
from os.path import isfile, join
from re import split as splitter

from kivy.core.image import Image

__all__ = ('GetPackages', )

class GetPackages:
    def find_applications(self):
        applications = sorted([x for x in listdir(self.apps_path)
                               if x.endswith('.desktop')])
        self.amount_of_applications = len(applications)
        self.dispatch('on_busy', True)

        for step, application in enumerate(applications, 1):
            with open(join(self.apps_path, application), encoding='utf-8') as file:
                for fileline in file:
                    if fileline.startswith('Icon='):
                        line = fileline[5:-1]
                        name = " ".join([(nm.capitalize() if len(nm) > 3 else nm.upper())
                                         for nm in splitter('[.-]', line.split('.')[-1])])

                        if icon := glob(f"/usr/share/icons/*/128*/*/{line}.png"):
                            icon_path = icon[0]
                        elif line.endswith('.png') and isfile(line):
                            icon_path = line
                        else:
                            # Can't determine where this .desktop file is pointing at
                            # so we are skipping this application
                            continue

                        icon = Image(icon_path)
                        self.add_application(step, name=name, package=application,
                                             texture=icon, use_old_icon=True)

        self.dispatch('on_busy', False)
