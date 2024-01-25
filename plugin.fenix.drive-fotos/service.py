#-------------------------------------------------------------------------------
# Copyright (C) 2017 Carlos Guzman (cguZZman) carlosguzmang@protonmail.com
# 
# Este archivo es parte de Google Drive para Kodi
# 
# Google Drive para Kodi es un software gratuito: puedes redistribuirlo y/o modificarlo
# bajo los términos de la Licencia Pública General GNU publicada por
# la Free Software Foundation, ya sea la versión 3 de la Licencia, o
# (a su elección) cualquier versión posterior.
# 
# El módulo común Cloud Drive para Kodi se distribuye con la esperanza de que sea útil.
# pero SIN NINGUNA GARANTÍA; sin siquiera la garantía implícita de
# COMERCIABILIDAD o IDONEIDAD PARA UN PROPÓSITO PARTICULAR. Ver el
# Licencia pública general GNU para más detalles.
# 
# Deberías haber recibido una copia de la Licencia Pública General GNU
# junto con este programa. Si no, ver <http://www.gnu.org/licenses/>.
#-------------------------------------------------------------------------------

from clouddrive.common.service.download import DownloadService
from clouddrive.common.service.source import SourceService
from clouddrive.common.service.utils import ServiceUtil
from resources.lib.provider.googledrive import GoogleDrive
from clouddrive.common.service.export import ExportService
from clouddrive.common.service.player import PlayerService


if __name__ == '__main__':
    ServiceUtil.run([DownloadService(GoogleDrive), SourceService(GoogleDrive),
                     ExportService(GoogleDrive), PlayerService(GoogleDrive)])