from time import time
from io import BytesIO
from os import makedirs
from os.path import getmtime, isfile, join
from shutil import rmtree

from android.storage import app_storage_path
from jnius import autoclass, cast

from kivy.core.image import Image
from kivy.logger import Logger

__all__ = ('GetPackages', )

class GetPackages:
    def find_applications(self):
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
        context = cast('android.content.Context', PythonActivity.mActivity)
        pm = context.getPackageManager()
        domains = pm.queryIntentActivities(intent, 0).toArray()

        cache_folder = join(app_storage_path(), '.cache', 'icons')
        makedirs(cache_folder, exist_ok=True)
        self.amount_of_applications = len(domains)
        self.dispatch('on_busy', True)

        if time() - getmtime(cache_folder) >= self.expiration_time:
            rmtree(cache_folder)
            Logger.debug('[KivyHome] Removed cached icons for renewal')
            makedirs(cache_folder, exist_ok=True)

        Logger.debug('[KivyHome] Scanning the device for applications')

        for step, domain in enumerate(domains, 1):
            package = domain.activityInfo.packageName
            info = pm.getApplicationInfo(package, pm.GET_META_DATA)
            name = pm.getApplicationLabel(info)
            filename = join(cache_folder, f'{package}.png')

            if store_old_icon:= isfile(filename):
                image = Image(filename)
            else:
                drawable = domain.activityInfo.loadIcon(pm)
                bitmap = Bitmap.createBitmap(100, 100, BitmapConfig.ARGB_8888)
                stream, canvas = OutputStream(), Canvas(bitmap)
                drawable.setBounds(0, 0, canvas.getWidth(), canvas.getHeight())
                drawable.draw(canvas)
                bitmap.compress(CompressFormat.PNG, 100, stream)
                image = Image(BytesIO(bytes(stream.toByteArray())), ext='png')

            self.add_application(step, name=name, package=package, texture=image,
                                 use_old_icon=store_old_icon, path=filename)

        self.dispatch('on_busy', False)
