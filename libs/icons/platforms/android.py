import time
from functools import partial
from io import BytesIO
from os import makedirs
from os.path import getmtime, isfile, join
from shutil import rmtree
from threading import Thread

from android.storage import app_storage_path
from jnius import autoclass, cast
from kivy.clock import Clock, mainthread
from kivy.core.image import Image
from kivy.logger import Logger

from ..appicons import AppIcon
from ...base import KivyHome

__all__ = ('GetPackages', )


class GetPackages:
    def on_kv_post(self, _):
        Thread(target=self.ready, daemon=True).start()

    def ready(self):
        Intent = autoclass('android.content.Intent')
        PythonActivity = autoclass('org.kivy.android.PythonActivity')
        OutputStream = autoclass('java.io.ByteArrayOutputStream')
        Bitmap = autoclass("android.graphics.Bitmap")
        Canvas = autoclass("android.graphics.Canvas")
        BitmapConfig = autoclass("android.graphics.Bitmap$Config")
        CompressFormat = autoclass("android.graphics.Bitmap$CompressFormat")

        intent = Intent()
        intent.setAction(Intent.ACTION_MAIN)
        intent.addCategory(Intent.CATEGORY_LAUNCHER)
        context = cast('android.content.Context',
                       PythonActivity.mActivity)
        pm = context.getPackageManager()
        domains = pm.queryIntentActivities(intent, 0).toArray()
        cache_folder = join(app_storage_path(), '.cache', 'icons')
        makedirs(cache_folder, exist_ok=True)
        self.amount_of_applications = len(domains)
        Clock.schedule_once(partial(self.on_busy, True), 0)
        self._home = KivyHome()

        if time.time() - getmtime(cache_folder) >= 259200:
            rmtree(cache_folder)
            Logger.debug('Deleted cached icons')
            makedirs(cache_folder, exist_ok=True)

        for step, domain in enumerate(domains, 1):
            package = domain.activityInfo.packageName
            info = pm.getApplicationInfo(package, pm.GET_META_DATA)
            name = pm.getApplicationLabel(info)
            filename = join(cache_folder, f'{package}.png')
            image = None

            if not (old := isfile(filename)):
                Logger.debug('Rendering icon: %s', filename)
                drawable = domain.activityInfo.loadIcon(pm)
                bitmap = Bitmap.createBitmap(100, 100, BitmapConfig.ARGB_8888)
                stream, canvas = OutputStream(), Canvas(bitmap)
                drawable.setBounds(0, 0, canvas.getWidth(), canvas.getHeight())
                drawable.draw(canvas)
                bitmap.compress(CompressFormat.PNG, 100, stream)
                image = Image(BytesIO(bytes(stream.toByteArray())), ext='png')
            else:
                Logger.debug('Loading icon: %s', filename)
                image = Image(filename)

            self.add_one(step, name=name, package=package, texture=image, old=old, path=filename)

        Clock.schedule_once(partial(self.on_busy, False), 1)

    @mainthread
    def add_one(self, step, **kwargs):
        self.popup.children[0].set_value(step)

        if not kwargs['old']:
            kwargs['texture'].save(kwargs['path'], flipped=False)
        
        kwargs['arguments'] = kwargs

        if dtype :=  self._home.desktop_icons.get(kwargs['package'], {}).get('dtype'):
            kwargs['dtype'] = dtype
            instance = self._home.ids[kwargs['dtype']]
            instance.add_widget(AppIcon(**kwargs))

        self.add_widget(AppIcon(**kwargs))
 
    def on_busy(self, status, _):
        self.popup.children[0].max = self.amount_of_applications
        self.popup.isbusy = status
